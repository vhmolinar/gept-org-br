# Site Audit & Reconstruction Package - Grupo Espírita Paulo de Tarso (GEPT)

This repository contains the complete content extraction, site map, design tokens, media catalog, form schemas, and structural analysis of the **Grupo Espírita Paulo de Tarso (GEPT)** website ([https://gept.org.br](https://gept.org.br)), located in Uberlândia / MG, Brazil.

All extracted data is stored in a self-contained format inside the `current-state/` directory so that a developer or automated agent can rebuild the website from scratch without needing further web research.

---

## 🕊️ Overview of the Institution & Website Purpose

### 1. Purpose of the Website & Institution
The **Grupo Espírita Paulo de Tarso (GEPT)** is a Spiritist institution (*Casa Espírita*) in Uberlândia/MG dedicated to the study, practice, and dissemination of Spiritism (*Doutrina Espírita*) based on the Codification by Allan Kardec and the works of Chico Xavier, André Luiz, Auta de Souza, and Emmanuel.

The primary purpose of the website is to serve as an accessible, welcoming digital front door for:
- **Welcoming people seeking spiritual help, comfort, or guidance.**
- **Publishing weekly schedules for public lectures, spiritual treatments, and study groups.**
- **Enrolling children, youth, and adults in spiritist education and mediumship courses.**
- **Mobilizing volunteers and donations for social charity campaigns.**
- **Providing direct remote access (Zoom/Online)** to meetings and distant spiritual care.

---

### 2. Core Content & Areas Covered

The website is structured around five core pillars:

#### A. Institutos (Departments & Specialized Institutes)
- **Instituto da Caridade**: Coordinates social assistance, aid for vulnerable families, food/clothing distribution, and fraternal campaigns (*Auta de Souza*, *Chico Xavier*, *Madre Tereza de Calcutá*).
- **Instituto da Criança**: Manages *Evangelização Infantil* (spiritist moral education for children from early childhood onwards).
- **Instituto do Jovem**: Operates *Mocidade Espírita* (dynamic youth group for ages 12+ covering ethics, spirituality, and social bonding).
- **Instituto da Divulgação**: Handles Spiritist book sales/lending, library management, digital media, and doctrine dissemination.
- **Instituto do Esclarecimento e Família**: Offers guidance, family orientation, study circles, and doctrine foundation courses.
- **Instituto da Mediunidade**: Runs the *Escola de Médiuns* (mediumship education based on Kardec and André Luiz) and coordinates mediumistic support in spiritual treatment rooms.

#### B. Atividades & Cronograma Semanal (Activities & Schedules)
- **Segunda-feira (19h45)**: *Triagem Fraterna* — Welcoming and orientation for individuals seeking spiritual treatment or joining house activities.
- **Terça-feira (19h45)**: *Reunião Pública (Presencial e Online)* — Open lectures, prayers, collective vibrations, and magnetic passes (*auxílio magnético*).
- **Quarta-feira (19h45)**: *Tratamento Espiritual & Escola de Médiuns* — Scheduled spiritual treatment sessions and mediumship study classes.
- **Domingo (09h00 - 09h30)**: *Campanha Auta de Souza* (door-to-door food/clothes drive & messages of comfort) & *Mocidade Espírita*.
- **Sábado**: *Tratamento Infantil* (08h15), *Mocidade Espírita* (09h00), *Evangelização Infantil* (09h15), *Campanha Chico Xavier* (09h30 - book lending), and *Global Kardec* (17h15).

#### C. Special Campaigns & Social Projects
- **Campanha Madre Tereza de Calcutá ("Em Defesa da Vida")**: Support for pregnant women, mothers, and protection of life.
- **EFAS (Encontro Fraterno Auta de Souza)**: Regional spiritist gathering, fraternal training, and solidarity registration.
- **Escola CEEB**: Spiritist educational institution registration.
- **Rota Nacional Paulo de Tarso**: Educational and doctrinal thematic route.
- **Projeto Energia Limpa**: Institutional sustainability initiative.

#### D. Digital & Remote Services
- Dedicated Zoom rooms (*Conexão Zoom - Tratamento* & *Conexão Zoom - Cursos*).
- Online Public Meeting streaming links and archives.
- Forms for *Tratamento à Distância* (remote spiritual treatment requests).

---

### 3. What the Site Communicates to the Audience

- **Fraternity & Accessibility**: Communicates a warm, open invitation to anyone regardless of religious background, emphasizing that all activities and spiritual treatments are free of charge.
- **Clarity & Transparency**: Clearly details when and how to attend meetings, how spiritual treatments work (starting with *Triagem Fraterna* on Mondays), and how to register children for evangelization.
- **Active Social Responsibility**: Highlights active volunteer campaigns, encouraging community involvement in food drives, book lending, and helping families in need.
- **Continuity & Digital Inclusion**: Ensures that individuals who cannot attend physically can participate through online public meetings and remote spiritual treatment via Zoom.

---

## 📁 `current-state/` Directory Overview

```
geptorgbr/
├── README.md                          <-- You are here (Master overview)
└── current-state/                     <-- Self-contained snapshot & documentation
    ├── SITE_MAP.md                    <-- Visual map, taxonomy, header menu & 59 route catalog
    ├── DESIGN_AND_STRUCTURE.md        <-- Design tokens, CSS variables, typography & UI components
    ├── MEDIA_AND_RESOURCES.md         <-- Logos, image catalog, form schemas & external links
    ├── PAGES/                         <-- 58 markdown files with full page contents
    │   ├── 01_home.md
    │   ├── 02_instituto_da_mediunidade.md
    │   ├── 04_instituto_do_esclarecimento_e_familia.md
    │   ├── 06_instituto_da_divulgacao.md
    │   ├── 08_efas.md
    │   ├── 12_reuniao_publica.md
    │   ├── 13_instituto_do_jovem.md
    │   ├── 19_instituto_da_caridade.md
    │   ├── 25_campanha_madre_tereza_de_calcuta.md
    │   ├── 34_instituto_da_crianca.md
    │   ├── 36_reuniao_publica_online.md
    │   └── ... (all 58 pages mapped)
    ├── data/
    │   └── crawled_site_data.json     <-- Raw & structured JSON dataset (WP API + Live Crawl)
    ├── extract_site.py                <-- Python web crawler & REST API scraper
    └── generate_documentation.py      <-- Markdown & JSON generator script
```

---

## 📄 File Details & Usage Guide for Reconstruction Agents

### 1. [`current-state/SITE_MAP.md`](file:///data/dev/src/geptorgbr/current-state/SITE_MAP.md)
- **Purpose**: Defines the site structure, page routing, and navigation hierarchy.
- **Key Sections**:
  - **Header Navigation**: Primary menu items and nested dropdowns.
  - **Route Catalog**: Complete table of 59 URLs/slugs, WordPress page IDs, page titles, purpose/role, and menu status.
  - **Hierarchy Tree**: Complete content tree from Home down to Institutes, Activities, Events, Projects, and Zoom Room redirects.

### 2. [`current-state/DESIGN_AND_STRUCTURE.md`](file:///data/dev/src/geptorgbr/current-state/DESIGN_AND_STRUCTURE.md)
- **Purpose**: Specs for building the new UI/UX, CSS design tokens, and components.
- **Key Sections**:
  - **Color Palette & CSS Variables**: Hex values for headers, accents, backgrounds, text muted colors, and preset variables (`--wp--preset--color--*`).
  - **Typography**: Font families (`Roboto`, `Roboto Slab`, `Lato`), font sizes, and line height rules.
  - **UI Component Specs**: Banner carousels, weekly schedule tabbed widgets (Domingo to Sábado), card grids, and responsive containers.
  - **Layout Specs**: Topbar header, logo placement, main menu, and footer layout.

### 3. [`current-state/MEDIA_AND_RESOURCES.md`](file:///data/dev/src/geptorgbr/current-state/MEDIA_AND_RESOURCES.md)
- **Purpose**: Asset management and third-party integrations.
- **Key Sections**:
  - **Image Catalog**: Image URLs, alt attributes, and usage locations.
  - **Form Schemas**: Action URLs, submit methods, input names, input types, and labels for all interactive forms.
  - **External Links & Integrations**: Zoom virtual room links, YouTube channels, WhatsApp links, and Google Forms.

### 4. [`current-state/PAGES/`](file:///data/dev/src/geptorgbr/current-state/PAGES/)
- **Purpose**: Full extracted text and structure for every page on the site.
- **Each file includes**:
  - Page title, original URL, slug, meta description.
  - Interactive element extractions (Sliders, Accordion tabs, custom widgets).
  - Main body text in clean Markdown format.
  - Embedded image references and form field specifications.

### 5. [`current-state/data/crawled_site_data.json`](file:///data/dev/src/geptorgbr/current-state/data/crawled_site_data.json)
- **Purpose**: Machine-readable master JSON dataset containing raw WordPress REST API payloads (pages, media library, categories, tags) and parsed live crawl outputs. Useful for programmatic ingestion by code generators or CMS migration tools.

---

## 🚀 Recommended Rebuilding Instructions

When initiating the rebuild with a site generator agent:
1. Parse [`SITE_MAP.md`](file:///data/dev/src/geptorgbr/current-state/SITE_MAP.md) to initialize router/navigation links.
2. Read [`DESIGN_AND_STRUCTURE.md`](file:///data/dev/src/geptorgbr/current-state/DESIGN_AND_STRUCTURE.md) to set up CSS variables, theme config, and base layout components (Header, Topbar, Footer, Tabs, Carousels).
3. Populate each page route using the corresponding document inside [`PAGES/`](file:///data/dev/src/geptorgbr/current-state/PAGES/).
4. Wire up forms and external Zoom/YouTube integrations as specified in [`MEDIA_AND_RESOURCES.md`](file:///data/dev/src/geptorgbr/current-state/MEDIA_AND_RESOURCES.md).
