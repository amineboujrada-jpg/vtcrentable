// VTC Rentable : sites vitrines des chauffeurs sur <adresse>.vtcrentable.fr
// Programme Cloudflare (Worker). Il reçoit toutes les adresses *.vtcrentable.fr, lit le site du chauffeur dans la base
// (Supabase, sites en ligne seulement) et renvoie la page complète, prête pour Google.
//   <adresse>.vtcrentable.fr/      la page du chauffeur en français (réservation incluse)
//   <adresse>.vtcrentable.fr/en/   la même page en anglais (textes du chauffeur traduits automatiquement)
//   Langue : un visiteur dont le navigateur n'est pas en français est envoyé sur /en/ ; le bouton de langue
//   (globe, en haut de page) permet de changer, et ce choix est retenu.
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

// ---------- Langues : français (/) et anglais (/en/) ----------
const SERVICES_EN = {
  "Transferts aéroport": "Airport transfers", "Transferts gare": "Train station transfers", "Trajets longue distance": "Long-distance rides",
  "Mise à disposition": "Hourly hire with driver", "Déplacements professionnels": "Business travel", "Soirées et événements": "Evenings and events",
  "Siège enfant sur demande": "Child seat on request", "Courses médicales": "Medical appointments"
};
// Numéro au format international pour les visiteurs étrangers : 06 12 34 56 78 devient +33 6 12 34 56 78
const telIntl = t => { const n = telLien(t); return n.startsWith("00") ? "+" + n.slice(2) : n.startsWith("0") ? "+33" + n.slice(1) : n; };
const telIntlAff = t => { const n = telIntl(t); return n.startsWith("+33") && n.length === 12 ? "+33 " + n[3] + " " + n.slice(4).replace(/(\d{2})(?=\d)/g, "$1 ") : n; };
// Prix écrits par le chauffeur : seules les tournures courantes sont traduites, les montants ne changent pas
const prixEn = p => String(p || "").replace(/à partir de/gi, "from").replace(/sur (demande|devis)/gi, "on request").replace(/environ/gi, "approx.")
  .replace(/par heure|de l'heure|l'heure|\/ ?heure/gi, "per hour").replace(/par personne/gi, "per person").replace(/aller[- ]retour/gi, "return trip").replace(/aller simple/gi, "one way");

// Textes fixes de la page, dans chaque langue. x = { nom, ville, tel (déjà mis en forme), zones }
const TEXTES = {
  fr: x => {
    const ou = x.ville ? " à " + x.ville : "";
    return {
      html: "fr", og: "fr_FR", autre: "en", autreNom: "English", autreAria: "English version",
      titre: `VTC${x.ville ? " " + x.ville : ""} : ${x.nom}, chauffeur privé sur réservation`,
      desc: `${x.nom}, chauffeur VTC${ou}. ${x.zones ? "Zones desservies : " + x.zones + ". " : ""}Réservation en ligne 24 h/24, prix confirmé avant la course.`,
      accroche: `Réservez votre chauffeur privé${ou}, à l'avance et à prix fixe.`,
      presentation: `${x.nom} vous conduit${ou} et dans les environs, sur réservation. Vous indiquez votre trajet, le prix vous est confirmé avant le départ et votre chauffeur vous attend à l'heure convenue.`,
      faq: [
        [`Comment réserver un VTC${ou} ?`, `Remplissez le formulaire de réservation de cette page${x.tel ? " ou appelez le " + x.tel : ""}. ${x.nom} vous confirme la course et son prix avant le départ.`],
        ["Le prix est-il connu à l'avance ?", "Oui. Le prix de la course est fixé et confirmé avant la prise en charge : pas de compteur ni de majoration surprise."],
        ["Quelles zones sont desservies ?", `${x.nom} se déplace${ou}${x.zones ? " et dessert : " + x.zones : " et dans les communes voisines"}. Pour un trajet plus long, indiquez votre destination dans la demande.`],
        ["Peut-on réserver pour un aéroport ou une gare ?", "Oui. Indiquez votre numéro de vol ou de train dans la note de la réservation pour que le chauffeur adapte l'heure de prise en charge."]
      ],
      apercu: "Aperçu : ce site n'est pas encore en ligne. La réservation est désactivée.",
      eyebrow: "VTC sur réservation", h1: `Chauffeur VTC${ou}`, reserver: "Réserver une course", appeler: "Appeler le ",
      p1: "Prix fixé à l'avance", p1s: "confirmé avant le départ", p2: "Réservation en ligne", p2s: "24 h/24, 7 j/7",
      vehicule: "Véhicule confortable", pax: n => `jusqu'à ${n} passager${n > 1 ? "s" : ""}`, horaires: "Horaires",
      h2Pres: `Votre chauffeur privé${ou}`, h2Serv: "Services", h2Tarifs: `Tarifs${x.ville ? " VTC " + x.ville : ""}`, surDemande: "sur demande",
      tarifsNote: "Prix indicatifs. Le prix de votre course est confirmé avant le départ.",
      h2Zones: "Zones desservies", zones: `${x.nom} assure vos trajets${ou}${x.zones ? " et dans les secteurs suivants : " + x.zones + "." : " et dans les communes voisines."}`,
      zonesNote: "Aéroports, gares, hôtels, domicile ou lieu de travail : indiquez simplement votre adresse de départ.",
      h2Resa: `Réserver votre VTC${ou}`, resaIntro: `Votre demande arrive directement chez ${x.nom}, qui vous rappelle pour confirmer la course et son prix.`,
      fNom: "Votre nom", fTel: "Votre téléphone", fDate: "Date", fHeure: "Heure", fDepart: "Adresse de prise en charge", fArrivee: "Destination",
      fPax: "Passagers", fNote: "Note (vol, bagages, siège enfant…)", fPiege: "Ne pas remplir", envoyer: "Envoyer ma demande", envoi: "Envoi…",
      rgpd: "Vos coordonnées servent uniquement à traiter cette réservation.",
      okTitre: "Demande envoyée", ok: `Merci. ${x.nom} vous rappelle rapidement pour confirmer la course. Référence :`,
      h2Faq: "Questions fréquentes", exploitant: "Exploitant : ", registre: "Registre VTC n° ",
      cree: ["Site créé avec ", ", l'appli de gestion pour chauffeurs VTC."], barResa: "Réserver", barTel: "Appeler",
      eNom: "Indiquez votre nom.", eTel: "Vérifiez votre numéro de téléphone.", eDate: "Choisissez la date et l'heure de prise en charge.",
      eDepart: "Indiquez l'adresse de prise en charge.", eEnvoi: "L'envoi n'a pas marché. Réessayez ou appelez directement.", serveur: null, note: ""
    };
  },
  en: x => {
    const ou = x.ville ? " in " + x.ville : "";
    return {
      html: "en", og: "en_GB", autre: "fr", autreNom: "Français", autreAria: "Version française",
      titre: `Private driver${ou}: ${x.nom}, book your ride online`,
      desc: `${x.nom}, licensed private driver (VTC)${ou}. ${x.zones ? "Areas served: " + x.zones + ". " : ""}Book online 24/7, fixed price confirmed before your ride.`,
      accroche: `Book your private driver${ou} in advance, at a fixed price.`,
      presentation: `${x.nom} drives you${ou} and the surrounding area, by reservation only. Tell us your journey: the price is confirmed before departure and your driver is waiting for you at the agreed time.`,
      faq: [
        [`How do I book a private driver${ou}?`, `Fill in the booking form on this page${x.tel ? " or call " + x.tel : ""}. ${x.nom} confirms your ride and its price before departure.`],
        ["Is the price known in advance?", "Yes. The price of your ride is fixed and confirmed before pick-up: no meter and no surprise surcharge."],
        ["Which areas are served?", `${x.nom} operates${ou}${x.zones ? " and serves: " + x.zones : " and the neighbouring towns"}. For a longer journey, enter your destination in the request.`],
        ["Can I book a ride to or from an airport or a train station?", "Yes. Add your flight or train number in the booking note so the driver can adjust the pick-up time."],
        ["What is a VTC?", "VTC is the French licence for private-hire drivers. A VTC is always booked in advance, at a price agreed before the ride."]
      ],
      apercu: "Aperçu de la version anglaise : ce site n'est pas encore en ligne. La réservation est désactivée.",
      eyebrow: "Private driver · pre-booked rides", h1: `Private driver${ou}`, reserver: "Book a ride", appeler: "Call ",
      p1: "Fixed price", p1s: "confirmed before departure", p2: "Online booking", p2s: "24 hours a day, 7 days a week",
      vehicule: "Comfortable vehicle", pax: n => `up to ${n} passenger${n > 1 ? "s" : ""}`, horaires: "Hours",
      h2Pres: `Your private driver${ou}`, h2Serv: "Services", h2Tarifs: `Rates${ou}`, surDemande: "on request",
      tarifsNote: "Indicative prices. The price of your ride is confirmed before departure.",
      h2Zones: "Areas served", zones: `${x.nom} drives you${ou}${x.zones ? " and in the following areas: " + x.zones + "." : " and the neighbouring towns."}`,
      zonesNote: "Airports, train stations, hotels, home or workplace: simply enter your pick-up address.",
      h2Resa: `Book your private driver${ou}`, resaIntro: `Your request goes straight to ${x.nom}, who will call you back to confirm the ride and its price.`,
      fNom: "Your name", fTel: "Your phone number (with country code)", fDate: "Date", fHeure: "Time", fDepart: "Pick-up address", fArrivee: "Destination",
      fPax: "Passengers", fNote: "Note (flight, luggage, child seat…)", fPiege: "Leave empty", envoyer: "Send my request", envoi: "Sending…",
      rgpd: "Your contact details are used only to handle this booking.",
      okTitre: "Request sent", ok: `Thank you. ${x.nom} will call you back shortly to confirm the ride. Reference:`,
      h2Faq: "Frequently asked questions", exploitant: "Operator: ", registre: "VTC register no. ",
      cree: ["Website made with ", ", the management app for VTC drivers."], barResa: "Book", barTel: "Call",
      eNom: "Please enter your name.", eTel: "Please check your phone number.", eDate: "Please choose the pick-up date and time.",
      eDepart: "Please enter the pick-up address.", eEnvoi: "Your request could not be sent. Please try again or call directly.",
      // Messages renvoyés en français par la base, reconnus à leur début
      serveur: { "Indiquez votre nom": "Please enter your name.", "Vérifiez votre num": "Please check your phone number.", "Vérifiez la date": "Please check the pick-up date.",
        "Vérifiez l'heure": "Please check the pick-up time.", "Indiquez l'adresse": "Please enter the pick-up address.",
        "Trop de demandes": "Too many requests sent: please try again later or call the driver.", "Le chauffeur a reçu": "The driver has received many requests today: please call directly.",
        "Ce site n'est pas": "This website is not online." },
      note: "Client anglophone. " // ajouté au début de la note : le chauffeur sait que la demande vient de la version anglaise
    };
  }
};

// ---------- Traduction automatique des textes du chauffeur (français vers anglais) ----------
// Service de traduction de Cloudflare (Workers AI, modèle m2m100). Chaque phrase traduite est gardée 30 jours :
// elle n'est retraduite que si le chauffeur change son texte. Si la traduction ne répond pas, le texte français est gardé.
const MODELE_TRAD = "@cf/meta/m2m100-1.2b";
async function traduireTexte(texte, env, ctx) {
  const t = String(texte || "").trim();
  if (!t || !env || !env.AI) return t;
  const cache = typeof caches !== "undefined" && caches.default;
  let cle = null;
  try {
    const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t));
    cle = new Request("https://traduction.invalid/fr-en/" + [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, "0")).join(""));
    const vu = cache && await cache.match(cle);
    if (vu) return await vu.text();
  } catch (_) {}
  try {
    const r = await Promise.race([
      env.AI.run(MODELE_TRAD, { text: t, source_lang: "french", target_lang: "english" }),
      new Promise((_, non) => setTimeout(() => non(new Error("trop long")), 8000))
    ]);
    const en = String((r && r.translated_text) || "").trim();
    if (!en || en.length > t.length * 3 + 40) return t; // réponse vide ou manifestement fausse
    if (cache && cle) {
      const garde = cache.put(cle, new Response(en, { headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=2592000" } }));
      if (ctx && ctx.waitUntil) ctx.waitUntil(garde); else await garde;
    }
    return en;
  } catch (_) { return t; }
}
// Un texte long est traduit phrase par phrase (meilleur résultat), en gardant les paragraphes
async function traduireLong(texte, env, ctx) {
  const paras = String(texte || "").split(/\n+/).map(p => p.trim()).filter(Boolean);
  let morceaux = paras.map(p => p.split(/(?<=[.!?…])\s+/).filter(Boolean));
  if (morceaux.reduce((n, m) => n + m.length, 0) > 24) morceaux = paras.map(p => [p]);
  const out = await Promise.all(morceaux.map(m => Promise.all(m.map(x => traduireTexte(x, env, ctx)))));
  return out.map(m => m.join(" ")).join("\n");
}
// Contenu anglais d'un site : les textes anglais écrits par le chauffeur passent avant la traduction automatique
export async function traduireSite(d, env, ctx) {
  d = d || {};
  const services = Array.isArray(d.services) ? d.services.slice(0, 10) : [];
  const tarifs = Array.isArray(d.tarifs) ? d.tarifs.filter(t => t && t.label).slice(0, 8) : [];
  const [accroche, presentation, vehicule, horaires, servicesEn, labels] = await Promise.all([
    d.accroche_en || traduireTexte(d.accroche, env, ctx),
    d.presentation_en || traduireLong(d.presentation, env, ctx),
    traduireTexte(d.vehicule, env, ctx),
    traduireTexte(d.horaires, env, ctx),
    Promise.all(services.map(s => SERVICES_EN[s] || traduireTexte(s, env, ctx))),
    Promise.all(tarifs.map(t => traduireTexte(t.label, env, ctx)))
  ]);
  return { accroche, presentation, vehicule, horaires, services: servicesEn, tarifs: tarifs.map((t, i) => ({ label: labels[i], prix: prixEn(t.prix) })) };
}

// ---------- Page d'un chauffeur ----------
// site = { slug, modele, data } ; opt.lang = "fr" ou "en" ; opt.en = contenu anglais (traduireSite) pour la version anglaise ;
// opt.apercu = true pour l'aperçu (bandeau, pas de réservation, pas de référencement, pas de bouton de langue)
export function renderSite(site, opt = {}) {
  const en = opt.lang === "en", lang = en ? "en" : "fr";
  const brut = site.data || {}, d = en ? { ...brut, ...(opt.en || {}) } : brut;
  const m = MODELES[site.modele] || MODELES.nuit, apercu = !!opt.apercu;
  const nom = (d.nom || (en ? "Private driver" : "Chauffeur VTC")).trim(), ville = (d.ville || "").trim(), tel = (d.tel || "").trim();
  const telH = en ? telIntl(tel) : telLien(tel), telA = en ? telIntlAff(tel) : telAff(tel);
  const t = TEXTES[lang]({ nom, ville, tel: tel ? telA : "", zones: d.zones || "" });
  const base = `https://${site.slug}.${DOMAINE}/`, url = en ? base + "en/" : base;
  const titre = t.titre.slice(0, 70), desc = t.desc.slice(0, 160);
  const accroche = d.accroche || t.accroche;
  const servicesDef = en ? SERVICES_DEF.map(s => SERVICES_EN[s]) : SERVICES_DEF;
  const services = (Array.isArray(d.services) && d.services.length ? d.services : servicesDef).slice(0, 10);
  const tarifs = Array.isArray(d.tarifs) ? d.tarifs.filter(x => x && x.label).slice(0, 8) : [];
  const places = Number(d.places) || 4;
  const paras = String(d.presentation || t.presentation).split(/\n+/).map(p => p.trim()).filter(Boolean);
  const faq = t.faq;
  const ld = [{
    "@context": "https://schema.org", "@type": "TaxiService", name: nom, url, description: desc, inLanguage: lang,
    ...(tel ? { telephone: telIntl(tel) } : {}),
    ...(ville ? { areaServed: [ville].concat(String(d.zones || "").split(/[,;]/).map(z => z.trim()).filter(Boolean)).slice(0, 12) } : {}),
    provider: { "@type": "LocalBusiness", name: d.exploitant || nom, ...(tel ? { telephone: telIntl(tel) } : {}), ...(ville ? { address: { "@type": "PostalAddress", addressLocality: ville, addressCountry: "FR" } } : {}) }
  }, {
    "@context": "https://schema.org", "@type": "FAQPage", inLanguage: lang,
    mainEntity: faq.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } }))
  }];
  const mentions = [d.exploitant && t.exploitant + d.exploitant, d.siren && "SIREN " + d.siren, d.registre && t.registre + d.registre, d.email && d.email].filter(Boolean);
  const auj = new Date(Date.now() + 3600e3).toISOString().slice(0, 10);
  // Bouton de langue : un globe et la langue proposée. Le lien retient le choix (voir « ?lang= » plus bas).
  const globe = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/></svg>`;
  const bascule = apercu ? "" : `<a class="lang" href="${en ? "/?lang=fr" : "/en/?lang=en"}" hreflang="${t.autre}" lang="${t.autre}" aria-label="${esc(t.autreAria)}" title="${esc(t.autreAria)}">${globe}<span>${t.autre.toUpperCase()}</span></a>`;

  return `<!doctype html>
<html lang="${t.html}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(titre)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="${apercu ? "noindex, nofollow" : "index, follow"}">
<link rel="canonical" href="${esc(url)}">
<link rel="alternate" hreflang="fr" href="${esc(base)}">
<link rel="alternate" hreflang="en" href="${esc(base)}en/">
<link rel="alternate" hreflang="x-default" href="${esc(base)}">
<meta name="theme-color" content="${m.theme}">
<meta property="og:type" content="website">
<meta property="og:locale" content="${t.og}">
<meta property="og:locale:alternate" content="${en ? "fr_FR" : "en_GB"}">
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
.droite{display:flex;align-items:center;gap:10px;flex:none}
.lang{display:inline-flex;align-items:center;gap:6px;min-height:42px;padding:8px 12px;border-radius:12px;border:1px solid var(--line);font-weight:700;font-size:15px;text-decoration:none;color:var(--fg)}
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
${apercu ? `<div class="apercu" role="status" lang="fr">${esc(t.apercu)}</div>` : ""}
<header class="top"><div class="wrap">
  <a class="brand" href="#haut">${esc(nom)}</a>
  <div class="droite">
    ${bascule}
    ${tel ? `<a class="btn small" href="tel:${esc(telH)}">${esc(telA)}</a>` : ""}
  </div>
</div></header>
<main id="haut">
  <div class="hero"><div class="wrap">
    <p class="eyebrow">${esc(t.eyebrow)}${ville ? " · " + esc(ville) : ""}</p>
    <h1>${esc(t.h1)}</h1>
    <p class="lede">${esc(accroche)}</p>
    <div class="ctas">
      <a class="btn main" href="#reserver">${esc(t.reserver)}</a>
      ${tel ? `<a class="btn" href="tel:${esc(telH)}">${esc(t.appeler + telA)}</a>` : ""}
      ${tel && d.whatsapp ? `<a class="btn" href="https://wa.me/${esc(telWa(tel))}" rel="noopener">WhatsApp</a>` : ""}
    </div>
    <ul class="points">
      <li>${esc(t.p1)}<small>${esc(t.p1s)}</small></li>
      <li>${esc(t.p2)}<small>${esc(t.p2s)}</small></li>
      <li>${esc(d.vehicule || t.vehicule)}<small>${esc(t.pax(places))}</small></li>
      ${d.horaires ? `<li>${esc(t.horaires)}<small>${esc(d.horaires)}</small></li>` : ""}
    </ul>
  </div></div>

  <section><div class="wrap">
    <h2>${esc(t.h2Pres)}</h2>
    ${paras.map(p => `<p>${esc(p)}</p>`).join("\n    ")}
  </div></section>

  <section><div class="wrap">
    <h2>${esc(t.h2Serv)}</h2>
    <ul class="tags">${services.map(s => `<li>${esc(s)}</li>`).join("")}</ul>
  </div></section>

  ${tarifs.length ? `<section><div class="wrap">
    <h2>${esc(t.h2Tarifs)}</h2>
    <table><tbody>${tarifs.map(x => `<tr><td>${esc(x.label)}</td><td>${esc(x.prix || t.surDemande)}</td></tr>`).join("")}</tbody></table>
    <p class="muted" style="margin-top:14px">${esc(t.tarifsNote)}</p>
  </div></section>` : ""}

  ${ville || d.zones ? `<section><div class="wrap">
    <h2>${esc(t.h2Zones)}</h2>
    <p>${esc(t.zones)}</p>
    <p class="muted">${esc(t.zonesNote)}</p>
  </div></section>` : ""}

  <section id="reserver"><div class="wrap">
    <h2>${esc(t.h2Resa)}</h2>
    <p class="muted">${esc(t.resaIntro)}</p>
    <form id="resa" novalidate>
      <div class="two">
        <label>${esc(t.fNom)}<input name="nom" autocomplete="name" required maxlength="60"></label>
        <label>${esc(t.fTel)}<input name="tel" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20"${en ? ` placeholder="+44 …"` : ""}></label>
      </div>
      <div class="two">
        <label>${esc(t.fDate)}<input name="date" type="date" required min="${auj}"></label>
        <label>${esc(t.fHeure)}<input name="heure" type="time" required></label>
      </div>
      <label>${esc(t.fDepart)}<input name="depart" autocomplete="street-address" required maxlength="160"></label>
      <label>${esc(t.fArrivee)}<input name="arrivee" maxlength="160"></label>
      <div class="two">
        <label>${esc(t.fPax)}<select name="pax">${Array.from({ length: places }, (_, i) => `<option>${i + 1}</option>`).join("")}</select></label>
        <label>${esc(t.fNote)}<input name="note" maxlength="${200 - t.note.length}"></label>
      </div>
      <div class="piege" aria-hidden="true"><label>${esc(t.fPiege)}<input name="site_web" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn main" type="submit"${apercu ? " disabled" : ""}>${esc(t.envoyer)}</button>
      <p class="msg" id="resaMsg" role="alert"></p>
      <p class="muted" style="font-size:14px;margin:0">${esc(t.rgpd)}</p>
    </form>
    <div class="ok" id="resaOk" hidden tabindex="-1"><h3>${esc(t.okTitre)}</h3><p style="margin-top:10px">${esc(t.ok)} <b id="resaNum"></b></p></div>
  </div></section>

  <section><div class="wrap">
    <h2>${esc(t.h2Faq)}</h2>
    ${faq.map(([q, a]) => `<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join("\n    ")}
  </div></section>
</main>
<footer><div class="wrap">
  <p><b>${esc(nom)}</b>${ville ? " · VTC " + esc(ville) : ""}${tel ? ` · <a href="tel:${esc(telH)}">${esc(telA)}</a>` : ""}</p>
  ${mentions.length ? `<p>${mentions.map(esc).join(" · ")}</p>` : ""}
  <p>${esc(t.cree[0])}<a href="https://vtcrentable.com/">VTC Rentable</a>${esc(t.cree[1])}</p>
</div></footer>
<div class="bar">
  <a class="btn main" href="#reserver">${esc(t.barResa)}</a>
  ${tel ? `<a class="btn" href="tel:${esc(telH)}">${esc(t.barTel)}</a>` : ""}
</div>
${apercu ? "" : `<script>
(function(){
  var f=document.getElementById("resa"),msg=document.getElementById("resaMsg"),T=${jsonLd({ eNom: t.eNom, eTel: t.eTel, eDate: t.eDate, eDepart: t.eDepart, eEnvoi: t.eEnvoi, envoi: t.envoi, envoyer: t.envoyer, serveur: t.serveur, note: t.note })};
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var v=function(n){return (f.elements[n].value||"").trim()},b=f.querySelector("button");
    msg.className="msg";msg.textContent="";
    if(v("nom").length<2)return err(T.eNom);
    if(v("tel").replace(/[^0-9+]/g,"").length<8)return err(T.eTel);
    if(!v("date")||!v("heure"))return err(T.eDate);
    if(v("depart").length<3)return err(T.eDepart);
    b.disabled=true;b.textContent=T.envoi;
    fetch(${JSON.stringify(SB_URL + "/rest/v1/rpc/site_reserver")},{method:"POST",headers:{apikey:${JSON.stringify(SB_KEY)},"Content-Type":"application/json"},
      body:JSON.stringify({p_slug:${jsonLd(site.slug)},p_nom:v("nom"),p_tel:v("tel"),p_date:v("date"),p_heure:v("heure"),p_depart:v("depart"),p_arrivee:v("arrivee"),p_pax:Number(v("pax"))||1,p_note:(T.note+v("note")).trim(),p_piege:v("site_web")})})
    .then(function(r){return r.json().then(function(j){if(!r.ok)throw new Error(j&&j.message||"");return j})})
    .then(function(j){f.hidden=true;var ok=document.getElementById("resaOk");document.getElementById("resaNum").textContent=j.numero||"";ok.hidden=false;ok.focus()})
    .catch(function(x){b.disabled=false;b.textContent=T.envoyer;err(dire(x.message))});
  });
  function dire(m){
    if(!m)return T.eEnvoi;
    if(!T.serveur)return m;
    for(var k in T.serveur)if(m.indexOf(k)===0)return T.serveur[k];
    return T.eEnvoi;
  }
  function err(t){msg.className="msg err";msg.textContent=t}
})();
</script>`}
</body>
</html>`;
}

// ---------- Petites pages : adresse inconnue, erreur ----------
const PETITES = {
  inconnue: { fr: ["Adresse inconnue", "Cette adresse ne correspond à aucun site."], en: ["Unknown address", "This address does not match any website."] },
  absent: { fr: ["Ce site n'existe pas ou n'est plus en ligne", "L'adresse est peut-être mal recopiée."], en: ["This website does not exist or is no longer online", "The address may have been mistyped."] },
  panne: { fr: ["Site momentanément indisponible", "Réessayez dans quelques instants."], en: ["Website temporarily unavailable", "Please try again in a moment."] },
  apercu: { fr: ["Aperçu indisponible", "Retourne dans l'appli et relance l'aperçu."] }
};
function pageSimple(quoi, statut, lang) {
  const en = lang === "en" && PETITES[quoi].en, [titre, texte] = en || PETITES[quoi].fr;
  return new Response(`<!doctype html><html lang="${en ? "en" : "fr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${esc(titre)}</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0f1116;color:#f1f2f5;font:17px/1.6 -apple-system,"Segoe UI",Roboto,sans-serif;padding:24px}main{max-width:32em}h1{font-size:32px;line-height:1.1;margin:0 0 12px}p{color:#a2a9b7;margin:0 0 18px}a{display:inline-block;background:#f2a614;color:#1d1400;font-weight:700;padding:13px 20px;border-radius:12px;text-decoration:none}</style></head>
<body><main><h1>${esc(titre)}</h1><p>${esc(texte)}</p><a href="${OFFRE}" lang="fr">Créer mon site de chauffeur VTC</a></main></body></html>`,
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

// ---------- Choix de la langue ----------
// 1. le choix fait avec le bouton de langue (retenu un an) ; 2. sinon la langue du navigateur : français = français,
// toute autre langue = anglais ; 3. sans indication (Google, robots) : français.
export function langueVisiteur(request) {
  const choix = /(?:^|;\s*)lang=(fr|en)(?:;|$)/.exec(request.headers.get("Cookie") || "");
  if (choix) return choix[1];
  let mieux = "", note = -1;
  for (const part of (request.headers.get("Accept-Language") || "").split(",")) {
    const [code, ...reste] = part.trim().split(";");
    const q = reste.map(r => /^\s*q=([\d.]+)\s*$/.exec(r)).filter(Boolean).map(r => Number(r[1]))[0];
    const n = q === undefined || isNaN(q) ? 1 : q;
    if (code && code !== "*" && n > note) { mieux = code.toLowerCase(); note = n; }
  }
  return !mieux || mieux === "fr" || mieux.startsWith("fr-") ? "fr" : "en";
}
// Renvoi vers une autre adresse du même site, jamais gardé en mémoire (il dépend du visiteur)
function renvoi(vers, cookie) {
  const h = new Headers({ Location: vers, "Cache-Control": "private, no-store", Vary: "Accept-Language, Cookie" });
  if (cookie) h.set("Set-Cookie", `lang=${cookie}; Path=/; Max-Age=31536000; SameSite=Lax; Secure`);
  return new Response(null, { status: 302, headers: h });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url), host = url.hostname.toLowerCase();
    if (host === DOMAINE || host === "www." + DOMAINE) return Response.redirect(OFFRE, 301);
    if (!host.endsWith("." + DOMAINE)) return pageSimple("inconnue", 404, langueVisiteur(request));
    const slug = host.slice(0, -DOMAINE.length - 1);

    // Aperçu demandé par l'appli : le contenu arrive dans la requête, rien n'est lu ni écrit dans la base
    if (slug === "apercu") {
      if (request.method !== "POST") return Response.redirect(OFFRE, 302);
      try {
        const form = await request.formData(), brut = String(form.get("site") || "");
        if (brut.length > 30000) throw new Error("trop long");
        const s = JSON.parse(brut), lang = form.get("lang") === "en" ? "en" : "fr";
        const site = { slug: /^[a-z0-9-]{3,30}$/.test(s.slug || "") ? s.slug : "mon-site", modele: s.modele, data: s.data && typeof s.data === "object" ? s.data : {} };
        const en = lang === "en" ? await traduireSite(site.data, env, ctx) : null;
        return new Response(renderSite(site, { apercu: true, lang, en }), { headers: enTetes("no-store") });
      } catch (_) { return pageSimple("apercu", 400); }
    }

    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Méthode non autorisée", { status: 405 });
    if (url.pathname === "/robots.txt") return new Response(`User-agent: *\nAllow: /\nDisallow: /*?lang=\n\nSitemap: https://${host}/sitemap.xml\n`, { headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
    if (!/^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$/.test(slug)) return pageSimple("inconnue", 404, langueVisiteur(request));

    // Langue : /en/ est toujours en anglais. Sur /, le bouton de langue (« ?lang= ») ou la langue du navigateur décide.
    const chemin = url.pathname === "/en" ? "/en/" : url.pathname, pageFr = chemin === "/", pageEn = chemin === "/en/";
    if (pageFr || pageEn) {
      const choix = url.searchParams.get("lang");
      if (choix === "fr" || choix === "en") return renvoi(`https://${host}${choix === "en" ? "/en/" : "/"}`, choix);
      if (pageFr && langueVisiteur(request) === "en") return renvoi(`https://${host}/en/`);
      if (url.pathname === "/en") return Response.redirect(`https://${host}/en/`, 301);
    }
    const lang = pageEn ? "en" : "fr";

    // Copie gardée 1 minute par Cloudflare, une par langue : une modification du chauffeur apparaît en une minute au plus
    const cle = new Request(`https://${host}${pageEn ? "/en/" : "/"}`, { method: "GET" });
    const cache = typeof caches !== "undefined" && caches.default;
    let site = null, page = cache && (pageFr || pageEn) ? await cache.match(cle) : null;
    if (page) return page;
    try { site = await lireSite(slug); }
    catch (_) { return pageSimple("panne", 503, pageEn ? "en" : langueVisiteur(request)); }
    if (!site) return pageSimple("absent", 404, pageEn ? "en" : langueVisiteur(request));

    if (url.pathname === "/sitemap.xml") {
      const maj = String(site.updated_at || "").slice(0, 10);
      const liens = `<xhtml:link rel="alternate" hreflang="fr" href="https://${host}/"/><xhtml:link rel="alternate" hreflang="en" href="https://${host}/en/"/><xhtml:link rel="alternate" hreflang="x-default" href="https://${host}/"/>`;
      return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml"><url><loc>https://${host}/</loc><lastmod>${maj}</lastmod>${liens}</url><url><loc>https://${host}/en/</loc><lastmod>${maj}</lastmod>${liens}</url></urlset>\n`,
        { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
    }
    if (!pageFr && !pageEn) return Response.redirect(`https://${host}/`, 301);
    const en = pageEn ? await traduireSite(site.data, env, ctx) : null;
    page = new Response(renderSite(site, { lang, en }), { headers: enTetes("public, max-age=60") });
    if (cache && ctx && ctx.waitUntil) ctx.waitUntil(cache.put(cle, page.clone()));
    return page;
  }
};
