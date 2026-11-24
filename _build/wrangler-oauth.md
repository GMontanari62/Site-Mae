# Login do painel /admin no Cloudflare (sem Netlify)

Usa o projeto aberto `sveltia-cms-auth` (Worker gratuito) para o login com GitHub.

1. GitHub > Settings > Developer settings > OAuth Apps > New OAuth App
   - Homepage URL: https://cmgenge.com.br
   - Authorization callback URL: https://NOME-DO-WORKER.SUBDOMINIO.workers.dev/callback
2. Guardar o Client ID e gerar um Client Secret.
3. Cloudflare > Workers & Pages > Create > "Deploy from a template/Clone repository" com
   https://github.com/sveltia/sveltia-cms-auth
4. No Worker, Settings > Variables and Secrets: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET (secret),
   ALLOWED_DOMAINS = cmgenge.com.br
5. Em admin/config.yml: `base_url: https://NOME-DO-WORKER.SUBDOMINIO.workers.dev` (e remover `auth_endpoint`).
