// Login do painel /admin (Sveltia CMS) com GitHub: passo 1, manda o navegador para a tela de autorização do GitHub.
// Variáveis no Cloudflare: GITHUB_CLIENT_ID (texto) e GITHUB_CLIENT_SECRET (secret).
export async function onRequestGet({ request, env }) {
  if (!env.GITHUB_CLIENT_ID) return new Response("GITHUB_CLIENT_ID ausente", { status: 500 });
  const url = new URL(request.url);
  const state = crypto.randomUUID();
  const gh = new URL("https://github.com/login/oauth/authorize");
  gh.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  gh.searchParams.set("scope", "repo,user");
  gh.searchParams.set("state", state);
  gh.searchParams.set("redirect_uri", `${url.origin}/callback`);
  return new Response(null, {
    status: 302,
    headers: {
      Location: gh.toString(),
      "Set-Cookie": `oauth_state=${state}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=600`,
      "Cache-Control": "no-store",
    },
  });
}
