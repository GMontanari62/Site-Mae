// Login do painel /admin: passo 2, o GitHub volta aqui com um código; trocamos por um token e entregamos ao painel (janela aberta pelo /admin).
const resposta = (status, mensagem, token) => {
  const payload = token
    ? `authorization:github:success:${JSON.stringify({ token, provider: "github" })}`
    : `authorization:github:error:${JSON.stringify({ message: mensagem })}`;
  // O painel conversa com esta janela por postMessage; só aceitamos mensagens vindas do próprio site.
  const html = `<!doctype html><meta charset="utf-8"><title>Login</title><p>${token ? "Conectado. Esta janela vai fechar." : "Não foi possível entrar."}</p>
<script>
(function(){
  var payload = ${JSON.stringify(payload)};
  var okOrigin = location.origin;
  window.addEventListener("message", function(e){
    if (e.origin !== okOrigin) return;
    window.opener.postMessage(payload, e.origin);
    window.close();
  });
  window.opener.postMessage("authorizing:github", okOrigin);
})();
</script>`;
  return new Response(html, {
    status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "Set-Cookie": "oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0",
    },
  });
};

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const cookie = (request.headers.get("Cookie") || "").match(/(?:^|; )oauth_state=([^;]+)/);
  if (!code || !state || !cookie || cookie[1] !== state) return resposta(400, "Pedido de login inválido ou expirado. Tente de novo.");

  const r = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "content-type": "application/json", Accept: "application/json", "User-Agent": "cmg-cms-auth" },
    body: JSON.stringify({ client_id: env.GITHUB_CLIENT_ID, client_secret: env.GITHUB_CLIENT_SECRET, code }),
  });
  const d = await r.json().catch(() => ({}));
  if (!d.access_token) return resposta(400, "O GitHub recusou o login.");
  return resposta(200, "", d.access_token);
}
