# Guia de trabalho do repositório GEPT

Este repositório contém o site do Grupo Espírita Paulo de Tarso (GEPT). Mantenha as alterações pequenas, focadas na solicitação e compatíveis com a estrutura existente.

## Estrutura do projeto

- `app/`: frontend estático em Astro e Tailwind CSS.
  - `src/pages/`: rotas e páginas do site.
  - `src/components/`: componentes reutilizáveis.
  - `src/layouts/`: layouts compartilhados.
  - `public/`: arquivos estáticos servidos diretamente.
- `functions/`: Cloud Functions do Firebase, em Node.js.
- `firebase.json`: configuração de Hosting, Functions, Storage e emuladores.
- `.firebaserc`: define `gept-org-br` como projeto Firebase padrão.
- `current-state/`: material histórico do site anterior; consulte-o apenas como referência de conteúdo e não o altere em mudanças rotineiras do site atual.

## Desenvolvimento

O frontend requer Node.js `>=22.12.0`. Para trabalhar nele:

```bash
cd app
npm install
npm run dev
```

Antes de concluir uma alteração no frontend, valide a compilação:

```bash
cd app
npm run build
```

Para alterações nas funções, use Node.js 20 e instale as dependências dentro de `functions/`:

```bash
cd functions
npm install
npm test
```

Quando for necessário testar integrações Firebase localmente, execute `firebase emulators:start` a partir da raiz. As portas configuradas são 5000 (Hosting), 5001 (Functions) e 8080 (Firestore).

## Convenções de alteração

- Preserve o idioma português em textos destinados aos visitantes.
- Reutilize os componentes e os estilos Tailwind já existentes antes de criar novas soluções.
- Evite alterar rotas, URLs externas, regras do Firebase ou Cloud Functions quando a demanda for exclusivamente visual ou de conteúdo.
- Não inclua arquivos gerados, `node_modules/`, arquivos de diagnóstico do Firebase ou credenciais no Git.
- O arquivo `.env` é local e confidencial. Nunca exiba, registre, versione ou cole o valor de suas variáveis em mensagens, código ou documentação pública.
- Respeite mudanças existentes no diretório de trabalho que não façam parte da tarefa atual.

## Deploy no Firebase

O projeto de destino padrão é `gept-org-br`, definido em `.firebaserc`. O Hosting publica os arquivos de `app/dist`.

No laptop, a credencial para deploy já está na variável `FIREBASE_TOKEN` do arquivo `.env` da raiz. Carregue essa variável sem imprimir seu conteúdo e informe-a ao Firebase CLI. Não é necessário executar `firebase login` para esse fluxo.

```bash
set -a
source .env
set +a

cd app
npm run build
cd ..

firebase deploy --only hosting --project gept-org-br --token "$FIREBASE_TOKEN"
```

Para publicar apenas as funções, mantenha a raiz como diretório atual e execute:

```bash
firebase deploy --only functions --project gept-org-br --token "$FIREBASE_TOKEN"
```

Use `firebase deploy --only hosting,functions --project gept-org-br --token "$FIREBASE_TOKEN"` somente quando a tarefa exigir ambos. Revise o `git diff` e execute as validações aplicáveis antes de qualquer deploy.
