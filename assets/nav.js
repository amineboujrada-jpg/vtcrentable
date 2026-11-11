/* Menu mobile : en dessous de 820 px, un bouton « Menu » affiche les liens de navigation. */
(function () {
  var nav = document.querySelector("nav.top");
  if (!nav) return;
  var ul = nav.querySelector("ul");
  var wrap = nav.querySelector(".wrap");
  if (!ul || !wrap) return;
  var st = document.createElement("style");
  st.textContent =
    "nav.top .nav-btn{display:none;background:transparent;color:inherit;border:1px solid currentColor;border-radius:10px;padding:9px 12px;font:600 14px/1 inherit;cursor:pointer;opacity:.9}" +
    "@media (max-width:820px){nav.top .nav-btn{display:inline-flex;align-items:center;gap:6px}" +
    "nav.top .wrap{flex-wrap:wrap}" +
    "nav.top.open ul{display:flex!important;flex-direction:column;gap:0;order:5;flex-basis:100%;padding:6px 0 10px;font-size:16px}" +
    "nav.top.open ul a{display:block;padding:12px 4px;border-top:1px solid rgba(255,255,255,.12)}}";
  document.head.appendChild(st);
  if (!ul.id) ul.id = "nav-liens";
  var b = document.createElement("button");
  b.type = "button"; b.className = "nav-btn"; b.textContent = "Menu";
  b.setAttribute("aria-expanded", "false"); b.setAttribute("aria-controls", ul.id);
  var cta = wrap.querySelector(".btn");
  wrap.insertBefore(b, cta || null);
  function set(o) { nav.classList.toggle("open", o); b.setAttribute("aria-expanded", o ? "true" : "false"); b.textContent = o ? "Fermer" : "Menu"; }
  b.addEventListener("click", function () { set(!nav.classList.contains("open")); });
  ul.addEventListener("click", function (e) { if (e.target.closest("a")) set(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
})();
