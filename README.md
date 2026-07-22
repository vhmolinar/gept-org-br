# Grupo Espírita Paulo de Tarso (GEPT) - Website

Este é o repositório oficial do website do **Grupo Espírita Paulo de Tarso (GEPT)**, localizado em Uberlândia / MG.

O site foi completamente reconstruído utilizando tecnologias modernas para oferecer uma experiência rápida, acessível e esteticamente agradável aos usuários que buscam informações sobre a Casa Espírita, suas atividades, cursos, campanhas de caridade e opções de contato.

---

## 🛠️ Stack Tecnológico

O projeto foi desenvolvido com foco em alta performance e escalabilidade, utilizando as seguintes tecnologias:

- **Frontend:** [Astro](https://astro.build/) - Framework web ultra-rápido focado na entrega de conteúdo estático e interativo apenas quando necessário.
- **Estilização:** [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utilitário para um design moderno, fluido e responsivo (utilizando paleta de cores institucional, *glassmorphism* e micro-animações).
- **Backend & Cloud:** [Firebase](https://firebase.google.com/)
  - **Hosting:** Hospedagem global rápida e segura para os arquivos estáticos gerados pelo Astro.
  - **Cloud Functions:** (Node.js) Funções serverless para processamento de formulários.
  - **Firestore:** Banco de dados NoSQL para armazenamento seguro de contatos, inscrições em cursos e engajamento em campanhas.

---

## 🚀 Funcionalidades e Estrutura

- **Institucional:** Páginas dedicadas aos Institutos da casa (Caridade, Criança, Jovem, Divulgação, Esclarecimento e Mediunidade).
- **Cursos de Espiritismo:** Formulário dinâmico de inscrição para novos alunos (`/cursos-espiritismo`).
- **Campanhas de Fraternidade:** Páginas de engajamento e formulários de cadastro de voluntários para as campanhas *Auta de Souza*, *Chico Xavier* e *Madre Tereza*.
- **Contato:** Página dedicada (`/contato`) com validação de formulário em tempo real e captura de mensagens integrada diretamente com o Firestore.
- **Atividades:** Cronograma completo das reuniões públicas (presenciais e online) e de tratamentos espirituais.

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
- Node.js (versão 20+)
- Firebase CLI instalado globalmente (`npm install -g firebase-tools`)

### 1. Frontend (Astro)

```bash
# Entre na pasta do frontend
cd app

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```
O site estará disponível em `http://localhost:4321`.

### 2. Backend (Firebase Functions)

```bash
# Entre na pasta de funções
cd functions

# Instale as dependências
npm install

# (Opcional) Inicie o emulador do Firebase para testar as funções localmente
firebase emulators:start
```

---

## 📦 Deploy para Produção

O processo de deploy envolve a compilação (*build*) do site estático e o envio das novas funções e arquivos para o Firebase.

Para realizar um deploy completo (Frontend + Backend), execute na raiz do projeto:

```bash
# 1. Faça o deploy das Funções
firebase deploy --only functions

# 2. Construa a versão otimizada do Frontend
cd app
npm run build
cd ..

# 3. Faça o deploy do Hosting
firebase deploy --only hosting
```

A URL de produção é: **[https://gept-org-br.web.app](https://gept-org-br.web.app)** (e domínios customizados configurados).

---

## 📁 Estrutura de Diretórios

- `/app/` - Código-fonte do frontend Astro (páginas, componentes, layouts e assets públicos).
- `/functions/` - Código do backend em Node.js contendo as regras e validações das Firebase Cloud Functions (`saveCourseLead`, `saveCampaignLeads`, `saveContactMessage`).
- `/current-state/` - Diretório legado contendo o mapeamento e extração do site antigo em WordPress (utilizado para consulta de conteúdo, imagens e estrutura originais).
