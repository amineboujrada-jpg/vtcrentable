// VTC Rentable : sites vitrines des chauffeurs sur <adresse>.vtcrentable.fr
// Programme Cloudflare (Worker). Il reçoit toutes les adresses *.vtcrentable.fr, lit le site du chauffeur dans la base
// (Supabase, sites en ligne seulement) et renvoie la page complète, prête pour Google.
//   <adresse>.vtcrentable.fr/      la page du chauffeur (réservation incluse)
//   apercu.vtcrentable.fr (POST)    aperçu envoyé par l'appli avant la mise en ligne (jamais référencé)
//   vtcrentable.fr, www             renvoi vers la présentation de l'offre sur vtcrentable.com
// Aucune clé secrète ici : la clé ci-dessous est la clé publique, la base ne laisse lire que les sites en ligne.

const DOMAINE = "vtcrentable.fr";
const SB_URL = "https://izjwblfezffiksoyapwa.supabase.co";
const SB_KEY = "sb_publishable_oHSTBBoFqNQEBLQWgrOTgA_d5sACoZU";
const OFFRE = "https://vtcrentable.com/site-vitrine-chauffeur-vtc/";

// ---------- Les 3 modèles : mêmes rubriques, couleurs et caractères différents ----------
const MODELES = {
  nuit: { nom: "Nuit", bg: "#0f1116", bg2: "#191c24", fg: "#f1f2f5", muted: "#a2a9b7", line: "#2c3140", accent: "#f2a614", accentFg: "#1d1400", titre: "-apple-system, 'Segoe UI', Roboto, sans-serif", theme: "#0f1116" },
  clair: { nom: "Clair", bg: "#ffffff", bg2: "#f3f6fb", fg: "#131a2a", muted: "#566176", line: "#d9e0ec", accent: "#1d4ed8", accentFg: "#ffffff", titre: "-apple-system, 'Segoe UI', Roboto, sans-serif", theme: "#ffffff" },
  prestige: { nom: "Prestige", bg: "#0b0b0c", bg2: "#161617", fg: "#f4efe6", muted: "#b3ab9c", line: "#34302a", accent: "#c9a45c", accentFg: "#171204", titre: "Georgia, 'Times New Roman', serif", theme: "#0b0b0c" }
};
const SERVICES_DEF = ["Transferts aéroport", "Transferts gare", "Trajets longue distance", "Mise à disposition", "Déplacements professionnels", "Soirées et événements"];

const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const jsonLd = o => JSON.stringify(o).replace(/</g, "\\u003c");
const telLien = t => String(t || "").replace(/[^\d+]/g, "");
const telWa = t => { const n = telLien(t).replace(/^\+/, "").replace(/^00/, ""); return n.startsWith("0") ? "33" + n.slice(1) : n; };
const telAff = t => String(t || "").replace(/\s+/g, "").replace(/^(\+33|0033)/, "0").replace(/(\d{2})(?=\d)/g, "$1 ").trim();

// ---------- Page d'un chauffeur ----------
// site = { slug, modele, data } ; opt.apercu = true pour l'aperçu (bandeau, pas de réservation, pas de référencement)
export function renderSite(site, opt = {}) {
  const d = site.data || {}, m = MODELES[site.modele] || MODELES.nuit, apercu = !!opt.apercu;
  const nom = (d.nom || "Chauffeur VTC").trim(), ville = (d.ville || "").trim(), tel = (d.tel || "").trim();
  const url = `https://${site.slug}.${DOMAINE}/`;
  const ou = ville ? " à " + ville : "";
  const titre = `VTC${ville ? " " + ville : ""} : ${nom}, chauffeur privé sur réservation`.slice(0, 70);
  const accroche = d.accroche || `Réservez votre chauffeur privé${ou}, à l'avance et à prix fixe.`;
  const desc = `${nom}, chauffeur VTC${ou}. ${d.zones ? "Zones desservies : " + d.zones + ". " : ""}Réservation en ligne 24 h/24, prix confirmé avant la course.`.slice(0, 160);
  const services = (Array.isArray(d.services) && d.services.length ? d.services : SERVICES_DEF).slice(0, 10);
  const tarifs = Array.isArray(d.tarifs) ? d.tarifs.filter(t => t && t.label).slice(0, 8) : [];
  const places = Number(d.places) || 4;
  const paras = String(d.presentation || `${nom} vous conduit${ou} et dans les environs, sur réservation. Vous indiquez votre trajet, le prix vous est confirmé avant le départ et votre chauffeur vous attend à l'heure convenue.`)
    .split(/\n+/).map(p => p.trim()).filter(Boolean);
  const faq = [
    [`Comment réserver un VTC${ou} ?`, `Remplissez le formulaire de réservation de cette page${tel ? " ou appelez le " + telAff(tel) : ""}. ${nom} vous confirme la course et son prix avant le départ.`],
    ["Le prix est-il connu à l'avance ?", "Oui. Le prix de la course est fixé et confirmé avant la prise en charge : pas de compteur ni de majoration surprise."],
    ["Quelles zones sont desservies ?", `${nom} se déplace${ou}${d.zones ? " et dessert : " + d.zones : " et dans les communes voisines"}. Pour un trajet plus long, indiquez votre destination dans la demande.`],
    ["Peut-on réserver pour un aéroport ou une gare ?", "Oui. Indiquez votre numéro de vol ou de train dans la note de la réservation pour que le chauffeur adapte l'heure de prise en charge."]
  ];
  const ld = [{
    "@context": "https://schema.org", "@type": "TaxiService", name: nom, url, description: desc,
    ...(tel ? { telephone: telLien(tel) } : {}),
    ...(ville ? { areaServed: [ville].concat(String(d.zones || "").split(/[,;]/).map(z => z.trim()).filter(Boolean)).slice(0, 12) } : {}),
    provider: { "@type": "LocalBusiness", name: d.exploitant || nom, ...(tel ? { telephone: telLien(tel) } : {}), ...(ville ? { address: { "@type": "PostalAddress", addressLocality: ville, addressCountry: "FR" } } : {}) }
  }, {
    "@context": "https://schema.org", "@type": "FAQPage",
    mainEntity: faq.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } }))
  }];
  const mentions = [d.exploitant && "Exploitant : " + d.exploitant, d.siren && "SIREN " + d.siren, d.registre && "Registre VTC n° " + d.registre, d.email && d.email].filter(Boolean);
  const auj = new Date(Date.now() + 3600e3).toISOString().slice(0, 10);

  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(titre)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="${apercu ? "noindex, nofollow" : "index, follow"}">
<link rel="canonical" href="${esc(url)}">
<meta name="theme-color" content="${m.theme}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="${esc(titre)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${esc(url)}">
<link rel="icon" href="data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="${m.bg}"/><text x="32" y="42" font-family="Arial" font-weight="700" font-size="26" text-anchor="middle" fill="${m.accent}">VTC</text></svg>`)}">
<script type="application/ld+json">${jsonLd(ld)}</script>
<style>
:root{--bg:${m.bg};--bg2:${m.bg2};--fg:${m.fg};--muted:${m.muted};--line:${m.line};--accent:${m.accent};--accent-fg:${m.accentFg}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,"Segoe UI",Roboto,sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:${m.titre};line-height:1.15;margin:0}
h1{font-size:clamp(34px,7vw,54px);letter-spacing:-.01em}
h2{font-size:clamp(24px,4.5vw,32px);margin-bottom:16px}
p{margin:0 0 14px}
a{color:inherit}
.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px}
.brand{font-weight:800;font-size:18px;text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:12px 20px;border-radius:12px;border:1px solid var(--line);font-weight:700;font-size:16px;text-decoration:none;color:var(--fg);background:transparent;cursor:pointer;font-family:inherit}
.btn.main{background:var(--accent);color:var(--accent-fg);border-color:transparent}
.btn.small{min-height:42px;padding:8px 14px;font-size:15px;white-space:nowrap}
.hero{padding:56px 0 44px}
.eyebrow{color:var(--accent);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px}
.lede{font-size:20px;color:var(--muted);margin:18px 0 26px;max-width:34em}
.ctas{display:flex;flex-wrap:wrap;gap:12px}
.points{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:34px;padding:0;list-style:none}
.points li{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:14px 16px;font-weight:600}
.points small{display:block;color:var(--muted);font-weight:400;font-size:14px}
section{padding:44px 0;border-top:1px solid var(--line)}
.muted{color:var(--muted)}
.tags{display:flex;flex-wrap:wrap;gap:10px;padding:0;margin:0;list-style:none}
.tags li{border:1px solid var(--line);background:var(--bg2);border-radius:999px;padding:8px 16px;font-weight:600;font-size:15px}
table{width:100%;border-collapse:collapse}
td{padding:14px 0;border-bottom:1px solid var(--line);vertical-align:top}
td:last-child{text-align:right;font-weight:700;white-space:nowrap;padding-left:16px}
form{display:grid;gap:14px;background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:22px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:grid;gap:6px;font-weight:600;font-size:15px}
input,select,textarea{width:100%;min-height:48px;padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg);font:inherit}
input:focus,select:focus,textarea:focus,.btn:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.piege{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.msg{font-weight:600;min-height:1.4em}
.msg.err{color:#e5484d}
.ok{background:var(--bg2);border:1px solid var(--accent);border-radius:18px;padding:22px}
details{border-bottom:1px solid var(--line);padding:14px 0}
summary{font-weight:700;cursor:pointer}
details p{margin:10px 0 0;color:var(--muted)}
footer{border-top:1px solid var(--line);padding:28px 0 96px;color:var(--muted);font-size:14px}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:6;display:none;gap:10px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));background:var(--bg);border-top:1px solid var(--line)}
.bar .btn{flex:1}
.apercu{background:#b45309;color:#fff;text-align:center;font-weight:700;padding:10px 14px;font-size:15px}
@media (max-width:640px){.two{grid-template-columns:1fr}.bar{display:flex}.top .btn{display:none}.hero{padding:40px 0 32px}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style>
</head>
<body>
${apercu ? `<div class="apercu" role="status">Aperçu : ce site n'est pas encore en ligne. La réservation est désactivée.</div>` : ""}
<header class="top"><div class="wrap">
  <a class="brand" href="#haut">${esc(nom)}</a>
  ${tel ? `<a class="btn small" href="tel:${esc(telLien(tel))}">${esc(telAff(tel))}</a>` : ""}
</div></header>
<main id="haut">
  <div class="hero"><div class="wrap">
    <p class="eyebrow">VTC sur réservation${ville ? " · " + esc(ville) : ""}</p>
    <h1>Chauffeur VTC${esc(ou)}</h1>
    <p class="lede">${esc(accroche)}</p>
    <div class="ctas">
      <a class="btn main" href="#reserver">Réserver une course</a>
      ${tel ? `<a class="btn" href="tel:${esc(telLien(tel))}">Appeler le ${esc(telAff(tel))}</a>` : ""}
      ${tel && d.whatsapp ? `<a class="btn" href="https://wa.me/${esc(telWa(tel))}" rel="noopener">WhatsApp</a>` : ""}
    </div>
    <ul class="points">
      <li>Prix fixé à l'avance<small>confirmé avant le départ</small></li>
      <li>Réservation en ligne<small>24 h/24, 7 j/7</small></li>
      <li>${esc(d.vehicule || "Véhicule confortable")}<small>jusqu'à ${places} passager${places > 1 ? "s" : ""}</small></li>
      ${d.horaires ? `<li>Horaires<small>${esc(d.horaires)}</small></li>` : ""}
    </ul>
  </div></div>

  <section><div class="wrap">
    <h2>Votre chauffeur privé${esc(ou)}</h2>
    ${paras.map(p => `<p>${esc(p)}</p>`).join("\n    ")}
  </div></section>

  <section><div class="wrap">
    <h2>Services</h2>
    <ul class="tags">${services.map(s => `<li>${esc(s)}</li>`).join("")}</ul>
  </div></section>

  ${tarifs.length ? `<section><div class="wrap">
    <h2>Tarifs${ville ? " VTC " + esc(ville) : ""}</h2>
    <table><tbody>${tarifs.map(t => `<tr><td>${esc(t.label)}</td><td>${esc(t.prix || "sur demande")}</td></tr>`).join("")}</tbody></table>
    <p class="muted" style="margin-top:14px">Prix indicatifs. Le prix de votre course est confirmé avant le départ.</p>
  </div></section>` : ""}

  ${ville || d.zones ? `<section><div class="wrap">
    <h2>Zones desservies</h2>
    <p>${esc(nom)} assure vos trajets${esc(ou)}${d.zones ? " et dans les secteurs suivants : " + esc(d.zones) + "." : " et dans les communes voisines."}</p>
    <p class="muted">Aéroports, gares, hôtels, domicile ou lieu de travail : indiquez simplement votre adresse de départ.</p>
  </div></section>` : ""}

  <section id="reserver"><div class="wrap">
    <h2>Réserver votre VTC${esc(ou)}</h2>
    <p class="muted">Votre demande arrive directement chez ${esc(nom)}, qui vous rappelle pour confirmer la course et son prix.</p>
    <form id="resa" novalidate>
      <div class="two">
        <label>Votre nom<input name="nom" autocomplete="name" required maxlength="60"></label>
        <label>Votre téléphone<input name="tel" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20"></label>
      </div>
      <div class="two">
        <label>Date<input name="date" type="date" required min="${auj}"></label>
        <label>Heure<input name="heure" type="time" required></label>
      </div>
      <label>Adresse de prise en charge<input name="depart" autocomplete="street-address" required maxlength="160"></label>
      <label>Destination<input name="arrivee" maxlength="160"></label>
      <div class="two">
        <label>Passagers<select name="pax">${Array.from({ length: places }, (_, i) => `<option>${i + 1}</option>`).join("")}</select></label>
        <label>Note (vol, bagages, siège enfant…)<input name="note" maxlength="200"></label>
      </div>
      <div class="piege" aria-hidden="true"><label>Ne pas remplir<input name="site_web" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn main" type="submit"${apercu ? " disabled" : ""}>Envoyer ma demande</button>
      <p class="msg" id="resaMsg" role="alert"></p>
      <p class="muted" style="font-size:14px;margin:0">Vos coordonnées servent uniquement à traiter cette réservation.</p>
    </form>
    <div class="ok" id="resaOk" hidden tabindex="-1"><h3>Demande envoyée</h3><p style="margin-top:10px">Merci. ${esc(nom)} vous rappelle rapidement pour confirmer la course. Référence : <b id="resaNum"></b></p></div>
  </div></section>

  <section><div class="wrap">
    <h2>Questions fréquentes</h2>
    ${faq.map(([q, a]) => `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join("\n    ")}
  </div></section>
</main>
<footer><div class="wrap">
  <p><b>${esc(nom)}</b>${ville ? " · VTC " + esc(ville) : ""}${tel ? ` · <a href="tel:${esc(telLien(tel))}">${esc(telAff(tel))}</a>` : ""}</p>
  ${mentions.length ? `<p>${mentions.map(esc).join(" · ")}</p>` : ""}
  <p>Site créé avec <a href="https://vtcrentable.com/">VTC Rentable</a>, l'appli de gestion pour chauffeurs VTC.</p>
</div></footer>
<div class="bar">
  <a class="btn main" href="#reserver">Réserver</a>
  ${tel ? `<a class="btn" href="tel:${esc(telLien(tel))}">Appeler</a>` : ""}
</div>
${apercu ? "" : `<script>
(function(){
  var f=document.getElementById("resa"),msg=document.getElementById("resaMsg");
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var v=function(n){return (f.elements[n].value||"").trim()},b=f.querySelector("button");
    msg.className="msg";msg.textContent="";
    if(v("nom").length<2)return err("Indiquez votre nom.");
    if(v("tel").replace(/[^0-9+]/g,"").length<8)return err("Vérifiez votre numéro de téléphone.");
    if(!v("date")||!v("heure"))return err("Choisissez la date et l'heure de prise en charge.");
    if(v("depart").length<3)return err("Indiquez l'adresse de prise en charge.");
    b.disabled=true;b.textContent="Envoi…";
    fetch(${JSON.stringify(SB_URL + "/rest/v1/rpc/site_reserver")},{method:"POST",headers:{apikey:${JSON.stringify(SB_KEY)},"Content-Type":"application/json"},
      body:JSON.stringify({p_slug:${jsonLd(site.slug)},p_nom:v("nom"),p_tel:v("tel"),p_date:v("date"),p_heure:v("heure"),p_depart:v("depart"),p_arrivee:v("arrivee"),p_pax:Number(v("pax"))||1,p_note:v("note"),p_piege:v("site_web")})})
    .then(function(r){return r.json().then(function(j){if(!r.ok)throw new Error(j&&j.message||"");return j})})
    .then(function(j){f.hidden=true;var ok=document.getElementById("resaOk");document.getElementById("resaNum").textContent=j.numero||"";ok.hidden=false;ok.focus()})
    .catch(function(x){b.disabled=false;b.textContent="Envoyer ma demande";err(x.message||"L'envoi n'a pas marché. Réessayez ou appelez directement.")});
  });
  function err(t){msg.className="msg err";msg.textContent=t}
})();
</script>`}
</body>
</html>`;
}

// ---------- Petites pages : adresse inconnue, erreur ----------
function pageSimple(titre, texte, statut) {
  return new Response(`<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${esc(titre)}</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0f1116;color:#f1f2f5;font:17px/1.6 -apple-system,"Segoe UI",Roboto,sans-serif;padding:24px}main{max-width:32em}h1{font-size:32px;line-height:1.1;margin:0 0 12px}p{color:#a2a9b7;margin:0 0 18px}a{display:inline-block;background:#f2a614;color:#1d1400;font-weight:700;padding:13px 20px;border-radius:12px;text-decoration:none}</style></head>
<body><main><h1>${esc(titre)}</h1><p>${esc(texte)}</p><a href="${OFFRE}">Créer mon site de chauffeur VTC</a></main></body></html>`,
    { status: statut, headers: enTetes("no-store") });
}
function enTetes(cache) {
  return {
    "Content-Type": "text/html; charset=utf-8", "Cache-Control": cache, "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src ${SB_URL}; img-src data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`
  };
}
async function lireSite(slug) {
  const r = await fetch(SB_URL + "/rest/v1/rpc/site_public", {
    method: "POST", headers: { apikey: SB_KEY, "Content-Type": "application/json" }, body: JSON.stringify({ p_slug: slug })
  });
  if (!r.ok) throw new Error("Base indisponible (" + r.status + ")");
  return r.json(); // null si le site n'existe pas ou n'est pas en ligne
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url), host = url.hostname.toLowerCase();
    if (host === DOMAINE || host === "www." + DOMAINE) return Response.redirect(OFFRE, 301);
    if (!host.endsWith("." + DOMAINE)) return pageSimple("Adresse inconnue", "Cette adresse ne correspond à aucun site.", 404);
    const slug = host.slice(0, -DOMAINE.length - 1);

    // Aperçu demandé par l'appli : le contenu arrive dans la requête, rien n'est lu ni écrit dans la base
    if (slug === "apercu") {
      if (request.method !== "POST") return Response.redirect(OFFRE, 302);
      try {
        const form = await request.formData(), brut = String(form.get("site") || "");
        if (brut.length > 30000) throw new Error("trop long");
        const s = JSON.parse(brut);
        const site = { slug: /^[a-z0-9-]{3,30}$/.test(s.slug || "") ? s.slug : "mon-site", modele: s.modele, data: s.data && typeof s.data === "object" ? s.data : {} };
        return new Response(renderSite(site, { apercu: true }), { headers: enTetes("no-store") });
      } catch (_) { return pageSimple("Aperçu indisponible", "Retourne dans l'appli et relance l'aperçu.", 400); }
    }

    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Méthode non autorisée", { status: 405 });
    if (url.pathname === "/robots.txt") return new Response(`User-agent: *\nAllow: /\n\nSitemap: https://${host}/sitemap.xml\n`, { headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
    if (!/^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$/.test(slug)) return pageSimple("Adresse inconnue", "Cette adresse ne correspond à aucun site.", 404);

    // Copie gardée 1 minute par Cloudflare : une modification du chauffeur apparaît en une minute au plus
    const cle = new Request(`https://${host}/`, { method: "GET" });
    const cache = typeof caches !== "undefined" && caches.default;
    let site = null, page = cache && url.pathname === "/" ? await cache.match(cle) : null;
    if (page) return page;
    try { site = await lireSite(slug); }
    catch (_) { return pageSimple("Site momentanément indisponible", "Réessayez dans quelques instants.", 503); }
    if (!site) return pageSimple("Ce site n'existe pas ou n'est plus en ligne", "L'adresse est peut-être mal recopiée.", 404);

    if (url.pathname === "/sitemap.xml") {
      return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://${host}/</loc><lastmod>${String(site.updated_at || "").slice(0, 10)}</lastmod></url></urlset>\n`,
        { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
    }
    if (url.pathname !== "/") return Response.redirect(`https://${host}/`, 301);
    page = new Response(renderSite(site), { headers: enTetes("public, max-age=60") });
    if (cache && ctx && ctx.waitUntil) ctx.waitUntil(cache.put(cle, page.clone()));
    return page;
  }
};
