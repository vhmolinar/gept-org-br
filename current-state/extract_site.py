import urllib.request
import urllib.parse
import json
import re
import os
from bs4 import BeautifulSoup
import html2text

BASE_URL = "https://gept.org.br"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get('Content-Type', '')
            if 'text' in content_type or 'json' in content_type or 'xml' in content_type:
                return resp.read().decode('utf-8', errors='replace')
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_json(url):
    raw = fetch_url(url)
    if raw:
        try:
            return json.loads(raw)
        except Exception as e:
            print(f"JSON decode error for {url}: {e}")
    return None

def main():
    print("=== Starting Crawl & Extraction for gept.org.br ===")
    
    # 1. Fetch WP API pages, posts, media
    print("1. Fetching WP API pages...")
    wp_pages = fetch_json(f"{BASE_URL}/wp-json/wp/v2/pages?per_page=100") or []
    print(f"Found {len(wp_pages)} pages in WP REST API.")

    print("2. Fetching WP API posts...")
    wp_posts = fetch_json(f"{BASE_URL}/wp-json/wp/v2/posts?per_page=100") or []
    print(f"Found {len(wp_posts)} posts in WP REST API.")

    print("3. Fetching WP API media...")
    wp_media = fetch_json(f"{BASE_URL}/wp-json/wp/v2/media?per_page=100") or []
    print(f"Found {len(wp_media)} media items in WP REST API.")

    print("4. Fetching WP API categories & tags...")
    wp_categories = fetch_json(f"{BASE_URL}/wp-json/wp/v2/categories?per_page=100") or []
    wp_tags = fetch_json(f"{BASE_URL}/wp-json/wp/v2/tags?per_page=100") or []

    # Map of URL -> page data
    all_urls = set()
    for p in wp_pages:
        if isinstance(p, dict) and p.get('link'):
            all_urls.add(p['link'])
    for p in wp_posts:
        if isinstance(p, dict) and p.get('link'):
            all_urls.add(p['link'])
            
    # Always include homepage & main sections
    all_urls.add(f"{BASE_URL}/")

    print(f"Total initial target URLs to crawl: {len(all_urls)}")

    crawled_pages = {}
    discovered_urls = set(all_urls)

    # HTML to Markdown converter setup
    h2t = html2text.HTML2Text()
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.body_width = 0

    # Crawl loop
    queue = list(discovered_urls)
    visited = set()

    global_design_info = {
        "colors": set(),
        "fonts": set(),
        "css_variables": {},
        "header_menu": [],
        "footer_content": "",
        "footer_links": [],
        "contact_info": {}
    }

    while queue:
        url = queue.pop(0)
        # Normalize URL
        url_clean = url.split('#')[0]
        if url_clean in visited:
            continue
        visited.add(url_clean)

        print(f"Crawling ({len(visited)}/{len(visited)+len(queue)}): {url_clean}")
        html_raw = fetch_url(url_clean)
        if not html_raw:
            continue

        soup = BeautifulSoup(html_raw, 'html.parser')

        # Discover internal links
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_link = urllib.parse.urljoin(url_clean, href).split('#')[0]
            if full_link.startswith(BASE_URL) and not any(full_link.endswith(ext) for ext in ['.jpg', '.png', '.pdf', '.zip', '.mp3', '.mp4', '.jpeg', '.gif', '.svg']):
                # Avoid wp-admin, wp-login, etc.
                if not any(x in full_link for x in ['/wp-admin', '/wp-login', '/wp-content', '/feed', '/xmlrpc.php']):
                    if full_link not in visited and full_link not in queue:
                        queue.append(full_link)

        # Extract Meta
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ""

        meta_desc = ""
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc_tag:
            meta_desc = meta_desc_tag.get('content', '')

        og_tags = {}
        for m in soup.find_all('meta'):
            prop = m.get('property') or m.get('name')
            if prop and (prop.startswith('og:') or prop.startswith('twitter:')):
                og_tags[prop] = m.get('content', '')

        # Extract Header Menu (if home or first time)
        if not global_design_info["header_menu"]:
            nav_main = soup.find('nav', class_=re.compile('elementor-nav-menu--main|nav-menu'))
            if nav_main:
                menu_items = []
                for li in nav_main.find_all('li', recursive=False):
                    a_elem = li.find('a')
                    if a_elem:
                        item = {"title": a_elem.get_text(strip=True), "url": a_elem.get('href'), "children": []}
                        sub_ul = li.find('ul', class_=re.compile('sub-menu|dropdown'))
                        if sub_ul:
                            for sub_li in sub_ul.find_all('li'):
                                sub_a = sub_li.find('a')
                                if sub_a:
                                    item["children"].append({"title": sub_a.get_text(strip=True), "url": sub_a.get('href')})
                        menu_items.append(item)
                global_design_info["header_menu"] = menu_items

        # Extract Footer
        footer_elem = soup.find('footer') or soup.find('div', class_=re.compile('elementor-location-footer'))
        if footer_elem and not global_design_info["footer_content"]:
            global_design_info["footer_content"] = h2t.handle(str(footer_elem))
            for fa in footer_elem.find_all('a', href=True):
                global_design_info["footer_links"].append({"text": fa.get_text(strip=True), "href": fa['href']})

        # Extract CSS root variables & colors/fonts
        for style in soup.find_all('style'):
            style_text = style.get_text()
            if '--wp--preset--color--' in style_text or ':root' in style_text:
                for line in style_text.split(';'):
                    if '--wp--preset--color--' in line or '--wp--' in line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            k, v = parts[0].strip(), parts[1].strip()
                            global_design_info["css_variables"][k] = v

        # Extract main page content
        content_elem = soup.find('div', class_=re.compile('elementor-page|entry-content|site-main|content')) or soup.find('body')
        
        # Extract structured widgets / tabs / accordions / slides
        tabs_data = []
        for tab_container in soup.find_all('div', class_=re.compile('elementor-widget-tabs|elementor-tabs')):
            tab_titles = [t.get_text(strip=True) for t in tab_container.find_all('div', class_=re.compile('elementor-tab-title'))]
            tab_contents = [h2t.handle(str(c)).strip() for c in tab_container.find_all('div', class_=re.compile('elementor-tab-content'))]
            tabs_data.append(list(zip(tab_titles, tab_contents)))

        slides_data = []
        for slide in soup.find_all('div', class_=re.compile('swiper-slide|elementor-repeater-item')):
            slide_heading = slide.find('div', class_=re.compile('elementor-slide-heading'))
            slide_desc = slide.find('div', class_=re.compile('elementor-slide-description'))
            slide_btn = slide.find('a', class_=re.compile('elementor-button'))
            if slide_heading or slide_desc:
                slides_data.append({
                    "heading": slide_heading.get_text(strip=True) if slide_heading else "",
                    "description": slide_desc.get_text(strip=True) if slide_desc else "",
                    "button_text": slide_btn.get_text(strip=True) if slide_btn else "",
                    "button_url": slide_btn.get('href') if slide_btn else ""
                })

        # Images on this page
        images = []
        if content_elem:
            for img in content_elem.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    images.append({
                        "src": src,
                        "alt": img.get('alt', ''),
                        "title": img.get('title', '')
                    })

        # Forms on this page
        forms = []
        for form in soup.find_all('form'):
            form_info = {
                "action": form.get('action', ''),
                "method": form.get('method', 'GET'),
                "id": form.get('id', ''),
                "class": form.get('class', []),
                "inputs": []
            }
            for inp in form.find_all(['input', 'textarea', 'select', 'button']):
                form_info["inputs"].append({
                    "name": inp.get('name', ''),
                    "type": inp.get('type', inp.name),
                    "placeholder": inp.get('placeholder', ''),
                    "value": inp.get('value', ''),
                    "label": inp.find_parent('label').get_text(strip=True) if inp.find_parent('label') else ''
                })
            forms.append(form_info)

        # Links on page
        page_links = []
        if content_elem:
            for a in content_elem.find_all('a', href=True):
                page_links.append({
                    "text": a.get_text(strip=True),
                    "href": a['href']
                })

        # Clean body html to markdown
        body_markdown = h2t.handle(str(content_elem)) if content_elem else ""

        # Remove excessive blank lines
        body_markdown = re.sub(r'\n{3,}', '\n\n', body_markdown)

        crawled_pages[url_clean] = {
            "url": url_clean,
            "title": title,
            "meta_description": meta_desc,
            "og_tags": og_tags,
            "slides": slides_data,
            "tabs": tabs_data,
            "images": images,
            "forms": forms,
            "links": page_links,
            "markdown": body_markdown
        }

    # Save raw crawled data as JSON artifact
    os.makedirs('/data/dev/src/geptorgbr/data', exist_ok=True)
    with open('/data/dev/src/geptorgbr/data/crawled_site_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            "wp_pages_api": wp_pages,
            "wp_posts_api": wp_posts,
            "wp_media_api": wp_media,
            "wp_categories": wp_categories,
            "wp_tags": wp_tags,
            "global_design": {
                "css_variables": global_design_info["css_variables"],
                "header_menu": global_design_info["header_menu"],
                "footer_content": global_design_info["footer_content"],
                "footer_links": global_design_info["footer_links"]
            },
            "pages": crawled_pages
        }, f, ensure_ascii=False, indent=2)

    print(f"=== Extraction Complete! Total pages crawled: {len(crawled_pages)} ===")

if __name__ == "__main__":
    main()
