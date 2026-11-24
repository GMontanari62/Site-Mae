// Cloudflare Pages Function: recebe o formulário de orçamento e envia por e-mail via Resend.
// Variável secreta necessária no Cloudflare (Settings > Variables and Secrets): RESEND_API_KEY
// Opcional: DESTINO (padrão carla@cmgenge.com.br) e REMETENTE (padrão onboarding@resend.dev).

const MAX_TOTAL = 20 * 1024 * 1024; // 20 MB de anexos no total (o formulário já avisa até 5 MB por arquivo)

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function paraBase64(buf) {
  const bytes = new Uint8Array(buf);
  let bin = "";
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin);
}

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

export async function onRequestPost({ request, env }) {
  if (!env.RESEND_API_KEY) return json({ ok: false, erro: "servidor sem chave de e-mail" }, 500);

  let fd;
  try { fd = await request.formData(); } catch { return json({ ok: false, erro: "formulário inválido" }, 400); }

  const campo = (n) => String(fd.get(n) ?? "").trim().slice(0, 5000);
  const nome = campo("nome"), email = campo("email"), mensagem = campo("mensagem");
  if (!nome || !mensagem || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ ok: false, erro: "campos obrigatórios" }, 400);

  const linhas = [
    ["Nome", nome], ["Telefone", campo("telefone")], ["E-mail", email], ["Empresa", campo("empresa")],
    ["Serviço", campo("servico")], ["Localização", campo("localizacao")], ["Descrição", mensagem],
  ].filter(([, v]) => v);

  const anexos = [];
  let total = 0;
  for (const f of fd.getAll("attachment")) {
    if (typeof f === "string" || !f.size) continue;
    total += f.size;
    if (total > MAX_TOTAL) return json({ ok: false, erro: "anexos grandes demais" }, 413);
    anexos.push({ filename: (f.name || "anexo").slice(0, 120), content: paraBase64(await f.arrayBuffer()) });
  }

  const html =
    `<h2>Novo pedido de orçamento pelo site</h2><table cellpadding="6" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:15px">` +
    linhas.map(([k, v]) => `<tr><td style="vertical-align:top"><b>${esc(k)}</b></td><td>${esc(v).replace(/\n/g, "<br>")}</td></tr>`).join("") +
    `</table>` + (anexos.length ? `<p>${anexos.length} anexo(s) neste e-mail.</p>` : "");

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({
      from: `Site CMG <${env.REMETENTE || "onboarding@resend.dev"}>`,
      to: [env.DESTINO || "carla@cmgenge.com.br"],
      reply_to: email,
      subject: `Novo pedido de orçamento: ${nome}`.slice(0, 150),
      html,
      attachments: anexos.length ? anexos : undefined,
    }),
  });
  if (!r.ok) return json({ ok: false, erro: "falha ao enviar e-mail" }, 502);
  return json({ ok: true });
}

// Qualquer outro método
export const onRequest = () => json({ ok: false, erro: "método não permitido" }, 405);
