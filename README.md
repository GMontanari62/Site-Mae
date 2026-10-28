# Site Mãe

Site da CMG Projetos & Consultoria / Engenharia & Consultoria (Belo Horizonte, MG), da engenheira Carla Montanari. É um site de uma página só, com `index.html` e a pasta `assets/` (imagens). Não precisa instalar nada nem compilar.

## Como publicar no Netlify
1. Entre em [app.netlify.com/drop](https://app.netlify.com/drop).
2. Arraste esta pasta (com `index.html` e `assets/`) para a área indicada.
3. O Netlify gera o endereço do site. O formulário de contato só envia mensagens de verdade quando o site está publicado em `cmgenge.com.br` ou em um endereço `netlify.app`.

## Como editar
- Textos e páginas: tudo está em `index.html`. Cada página é um bloco `<div class="view" id="v-...">`.
- Estilos: bloco `<style>` no início do `index.html`.
- Comportamento (menu, troca de páginas, animações, formulário e fundo 3D): bloco `<script>` no final do `index.html`.
- Imagens: pasta `assets/` (logo e foto).

Depois de editar, publique de novo arrastando a pasta no Netlify.
