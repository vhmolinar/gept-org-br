import json
import os
import re

def main():
    json_path = '/data/dev/src/geptorgbr/data/crawled_site_data.json'
    if not os.path.exists(json_path):
        print("Data file not found yet!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pages = data.get("pages", {})
    wp_pages = data.get("wp_pages_api", [])
    wp_media = data.get("wp_media_api", [])
    global_design = data.get("global_design", {})

    print(f"Loaded {len(pages)} pages from crawl data.")

    base_dir = '/data/dev/src/geptorgbr'
    pages_dir = os.path.join(base_dir, 'PAGES')
    os.makedirs(pages_dir, exist_ok=True)

    # 1. Generate SITE_MAP.md
    sitemap_md = []
    sitemap_md.append("# Map do Site - Grupo Espírita Paulo de Tarso (GEPT)\n")
    sitemap_md.append("> **Visão Geral**: Documentação completa da estrutura de navegação, taxonomia, rotas e hierarquia do site original (gept.org.br).\n")
    
    sitemap_md.append("## 1. Menu Principal (Header Navigation)\n")
    for item in global_design.get("header_menu", []):
        sitemap_md.append(f"- **[{item['title']}]({item['url']})**")
        for sub in item.get("children", []):
            sitemap_md.append(f"  - [{sub['title']}]({sub['url']})")
    sitemap_md.append("\n")

    sitemap_md.append("## 2. Catálogo Completo de Rotas\n")
    sitemap_md.append("| ID WP | Título da Página | URL / Slug | Finalidade / Tipo | Menu |")
    sitemap_md.append("|-------|------------------|------------|-------------------|------|")

    # Map WP pages for easy lookup
    wp_map = {p['id']: p for p in wp_pages if isinstance(p, dict)}

    # Categorize pages
    route_catalog = []
    for url, page in sorted(pages.items()):
        slug = url.replace("https://gept.org.br", "").strip('/')
        if not slug:
            slug = "/"
        
        # Find WP ID
        wp_id = "N/A"
        for p in wp_pages:
            if isinstance(p, dict) and p.get('link') and p['link'].rstrip('/') == url.rstrip('/'):
                wp_id = p.get('id')
                break

        title = page.get('title', slug).split(' – ')[0].split(' - ')[0]
        
        # Determine purpose
        purpose = "Página de Conteúdo"
        if slug in ["/", "home"]:
            purpose = "Página Inicial (Landing Page)"
        elif "instituto" in slug:
            purpose = "Instituto / Departamento"
        elif "reuniao-publica" in slug:
            purpose = "Atividade / Reunião"
        elif "conexao-zoom" in slug or "zoom" in slug or "redirecionamento" in slug:
            purpose = "Redirecionamento / Sala Zoom"
        elif "privacidade" in slug or "termos" in slug:
            purpose = "Legal / Institucional"
        elif "efas" in slug:
            purpose = "Evento / EFAS"
        elif "rota" in slug:
            purpose = "Projeto / Rota Nacional"

        in_menu = "Sim" if any(item['url'].rstrip('/') == url.rstrip('/') or any(sub['url'].rstrip('/') == url.rstrip('/') for sub in item.get('children', [])) for item in global_design.get("header_menu", [])) else "Não (Link Interno/Direto)"

        sitemap_md.append(f"| {wp_id} | {title} | `{slug}` | {purpose} | {in_menu} |")
        route_catalog.append({"wp_id": wp_id, "title": title, "slug": slug, "url": url, "purpose": purpose, "in_menu": in_menu})

    sitemap_md.append("\n## 3. Hierarquia do Conteúdo\n")
    sitemap_md.append("```\ngept.org.br/")
    sitemap_md.append("├── Início (/)")
    sitemap_md.append("├── Institutos (/institutos/)")
    sitemap_md.append("│   ├── Instituto da Caridade (/instituto-da-caridade/)")
    sitemap_md.append("│   ├── Instituto da Criança (/instituto-da-crianca/)")
    sitemap_md.append("│   ├── Instituto da Divulgação (/instituto-da-divulgacao/)")
    sitemap_md.append("│   ├── Instituto do Esclarecimento e Família (/instituto-do-esclarecimento-e-familia/)")
    sitemap_md.append("│   ├── Instituto do Jovem (/instituto-do-jovem/)")
    sitemap_md.append("│   └── Instituto da Mediunidade (/instituto-da-mediunidade/)")
    sitemap_md.append("├── Atividades (/atividades/)")
    sitemap_md.append("│   ├── Reunião Pública Presencial (/reuniao-publica/)")
    sitemap_md.append("│   ├── Reunião Pública Online (/reuniao-publica-online/)")
    sitemap_md.append("│   └── Tratamento Espiritual / Triagem (/tratamento-espiritual/ & /tratamento-a-distancia/)")
    sitemap_md.append("├── Projetos & Eventos")
    sitemap_md.append("│   ├── Campanha Madre Tereza de Calcutá (/campanha-madre-tereza-de-calcuta/)")
    sitemap_md.append("│   ├── EFAS - Encontro Fraterno Auta de Souza (/efas/)")
    sitemap_md.append("│   ├── CEEB - Escola (/escola/)")
    sitemap_md.append("│   ├── Rota Nacional Paulo de Tarso (/rota/)")
    sitemap_md.append("│   └── Projeto Energia Sustentável (/energia-limpa/)")
    sitemap_md.append("├── Notícias e Eventos (/noticias-e-eventos/)")
    sitemap_md.append("├── Contato (/contato/)")
    sitemap_md.append("└── Links Úteis & Redirecionamentos Zoom (/conexao-zoom-..., /gept-tad-zoom, etc.)")
    sitemap_md.append("```\n")

    with open(os.path.join(base_dir, 'SITE_MAP.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_md))

    # 2. Generate DESIGN_AND_STRUCTURE.md
    design_md = []
    design_md.append("# Guia de Design e Estrutura Visual (Design System)\n")
    design_md.append("> **Objetivo**: Fornecer a especificação completa da identidade visual, componentes de interface, layout e regras estruturais para reconstrução do site.\n")
    
    design_md.append("## 1. Paleta de Cores e Variáveis CSS\n")
    design_md.append("| Nome / Token | Valor Extraído | Aplicação Sugerida |")
    design_md.append("|--------------|----------------|--------------------|")
    design_md.append("| Primary / Header Top | `#54595F` / `#333333` | Topbar, cabeçalho e elementos secundários |")
    design_md.append("| Accent / Highlights | `#0073AA` / `#0693e3` | Botões, links ativos e destaques |")
    design_md.append("| Background Light | `#FFFFFF` / `#F9F9F9` | Fundo principal das seções |")
    design_md.append("| Text Dark | `#333333` / `#222222` | Textos principais, títulos |")
    design_md.append("| Text Muted | `#777777` / `#666666` | Descrições secundárias, metadados |")
    design_md.append("\n### Variáveis CSS Extraídas:\n```css\n")
    for k, v in global_design.get("css_variables", {}).items():
        design_md.append(f"{k}: {v};")
    design_md.append("```\n")

    design_md.append("## 2. Tipografia\n")
    design_md.append("- **Fonte Primária (Textos)**: `Roboto`, `Open Sans`, `sans-serif`\n")
    design_md.append("- **Fonte de Títulos**: `Roboto Slab`, `Lato`, `serif` / `sans-serif`\n")
    design_md.append("- **Hierarquia de Tamanhos**:\n")
    design_md.append("  - H1 / Hero Headings: `32px - 42px` (Bold)\n")
    design_md.append("  - H2 / Section Headings: `24px - 32px` (Semi-bold)\n")
    design_md.append("  - H3 / Card Titles: `18px - 22px` (Medium)\n")
    design_md.append("  - Body Text: `15px - 16px` (Regular, line-height 1.6)\n")

    design_md.append("\n## 3. Componentes de UI Recorrentes\n")
    design_md.append("### A. Banner / Hero Slider\n")
    design_md.append("- Presente na Página Inicial (`/`). Contém slides carrossel com título, descrição breve e botão de call-to-action (CTA).\n")
    design_md.append("### B. Abas de Cronograma Semanal (Tabs Widget)\n")
    design_md.append("- Utilizado na Home e em Atividades. Abas interativas organizadas por dias da semana (Domingo, Segunda, Terça, Quarta, Sábado) com horário e descrição do trabalho espírita.\n")
    design_md.append("### C. Cards de Institutos\n")
    design_md.append("- Grid de cards com ícone/imagem, título do instituto, breve resumo e botão 'Saiba Mais'.\n")
    design_md.append("### D. Formulários\n")
    design_md.append("- Formulários de contato, inscrição e triagem com campos textuais, email, telefone, mensagem e botão de envio.\n")

    design_md.append("\n## 4. Estrutura do Cabeçalho e Rodapé\n")
    design_md.append("### Topbar Header\n")
    design_md.append("- Texto: `Boas vindas ao Grupo Espírita Paulo de Tarso! Uberlândia/MG`\n")
    design_md.append("### Main Header\n")
    design_md.append("- Logo: `Logos-GEPT-Quadrada-500x500-1.png` (link para Home)\n")
    design_md.append("- Menu de Navegação Horizontal com dropdown para Institutos e Atividades.\n")
    design_md.append("### Rodapé (Footer)\n")
    design_md.append(f"{global_design.get('footer_content', '')}\n")

    with open(os.path.join(base_dir, 'DESIGN_AND_STRUCTURE.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(design_md))

    # 3. Generate MEDIA_AND_RESOURCES.md
    media_md = []
    media_md.append("# Catálogo de Mídias, Formulários e Recursos Externos\n")
    media_md.append("> **Objetivo**: Mapear todas as imagens, logotipos, vídeos, formulários e links externos (Zoom, YouTube, WhatsApp) presentes no site.\n")

    media_md.append("## 1. Logotipos e Imagens Principais\n")
    all_images = set()
    for url, p in pages.items():
        for img in p.get('images', []):
            if img.get('src'):
                all_images.add((img['src'], img.get('alt', ''), img.get('title', '')))

    media_md.append("| Imagem URL | Texto Alternativo (Alt) | Título / Origem |")
    media_md.append("|------------|-------------------------|-----------------|")
    for img_url, alt, title in sorted(all_images):
        media_md.append(f"| `{img_url}` | {alt or 'N/A'} | {title or 'N/A'} |")

    media_md.append("\n## 2. Media Library WP (REST API)\n")
    media_md.append(f"Total de itens de mídia registrados no WordPress: {len(wp_media)}\n")

    media_md.append("\n## 3. Formatos e Inscrições (Formulários Mapeados)\n")
    for url, p in pages.items():
        if p.get('forms'):
            media_md.append(f"### Página: [{p['title']}]({url})\n")
            for idx, form in enumerate(p['forms']):
                media_md.append(f"**Formulário #{idx+1}** (Action: `{form['action']}`, Method: `{form['method']}`):\n")
                for inp in form.get('inputs', []):
                    media_md.append(f"- Campo: `{inp['name']}` | Tipo: `{inp['type']}` | Label/Placeholder: `{inp['label'] or inp['placeholder']}`")
                media_md.append("\n")

    media_md.append("## 4. Integracões Externas e Links (Zoom, YouTube, WhatsApp)\n")
    external_links = set()
    for url, p in pages.items():
        for link in p.get('links', []):
            href = link.get('href', '')
            if any(domain in href for domain in ['zoom.us', 'youtube.com', 'youtu.be', 'wa.me', 'whatsapp.com', 'forms.gle', 'google.com/maps']):
                external_links.add((link.get('text', ''), href, p.get('title', '')))

    media_md.append("| Texto do Link | URL Destino | Página de Origem |")
    media_md.append("|---------------|-------------|------------------|")
    for text, href, page_title in sorted(external_links):
        media_md.append(f"| {text or 'Link'} | `{href}` | {page_title} |")

    with open(os.path.join(base_dir, 'MEDIA_AND_RESOURCES.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(media_md))

    # 4. Generate Individual Page Documentation in PAGES/
    page_counter = 1
    for url, p in pages.items():
        slug = url.replace("https://gept.org.br", "").strip('/')
        if not slug:
            clean_filename = "01_home.md"
        else:
            clean_slug = re.sub(r'[^a-zA-Z0-9_]', '_', slug)
            clean_filename = f"{page_counter:02d}_{clean_slug}.md"
            page_counter += 1

        filepath = os.path.join(pages_dir, clean_filename)
        p_md = []
        p_md.append(f"# {p.get('title', 'Página')}\n")
        p_md.append(f"- **URL Original**: {url}")
        p_md.append(f"- **Slug**: `{slug or '/'}`")
        p_md.append(f"- **Descrição Meta**: {p.get('meta_description', 'N/A')}\n")

        if p.get('slides'):
            p_md.append("## Carrossel / Banner Sliders\n")
            for s in p['slides']:
                p_md.append(f"### Slide: {s['heading']}")
                p_md.append(f"- **Descrição**: {s['description']}")
                p_md.append(f"- **Botão**: [{s['button_text']}]({s['button_url']})\n")

        if p.get('tabs'):
            p_md.append("## Conteúdo em Abas / Accordion\n")
            for tab_group in p['tabs']:
                for tab_title, tab_content in tab_group:
                    p_md.append(f"### Aba: {tab_title}\n{tab_content}\n")

        p_md.append("## Conteúdo Principal (Markdown Extraído)\n")
        p_md.append(p.get('markdown', ''))

        if p.get('forms'):
            p_md.append("\n## Formulários Presentes\n")
            for idx, form in enumerate(p['forms']):
                p_md.append(f"**Formulário #{idx+1}**:")
                for inp in form.get('inputs', []):
                    p_md.append(f"- `{inp['name']}` ({inp['type']}): {inp['label'] or inp['placeholder']}")

        if p.get('images'):
            p_md.append("\n## Imagens na Página\n")
            for img in p['images']:
                p_md.append(f"- ![{img.get('alt', 'imagem')}]({img['src']})")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(p_md))

    print(f"Generated all documentation files in {base_dir}!")

if __name__ == "__main__":
    main()
