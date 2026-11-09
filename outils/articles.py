import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-05"
DATE_FR = "5 novembre 2026"
APP = "https://app.vtcrentable.com/"
SITE = "https://vtcrentable.com"

# Les articles du blog sont dans content/blog/<slug>.html : un en-tête « clé: valeur », une ligne ---, puis le corps en HTML.
# Clés : slug, date (AAAA-MM-JJ), categorie, title, desc, h1, short, lede, card ; « faq: question || réponse » et « source: titre || url » répétables.
def lire_article(chemin):
    brut = open(chemin, encoding="utf-8").read()
    entete, corps = brut.split("\n---\n", 1)
    a = {"faq": [], "sources": [], "body": corps}
    for ligne in entete.splitlines():
        if not ligne.strip():
            continue
        cle, val = ligne.split(":", 1)
        cle, val = cle.strip(), val.strip()
        if cle == "faq":
            a["faq"].append(tuple(x.strip() for x in val.split("||", 1)))
        elif cle == "source":
            a["sources"].append(tuple(x.strip() for x in val.split("||", 1)))
        else:
            a[cle] = val
    for cle in ("slug", "date", "categorie", "title", "desc", "h1", "short", "lede", "card"):
        assert cle in a, f"{chemin} : clé « {cle} » manquante"
    assert a["slug"] == os.path.basename(chemin)[:-5], f"{chemin} : le slug doit être le nom du fichier"
    return a

ARTS = sorted((lire_article(os.path.join(ROOT, "content", "blog", f)) for f in os.listdir(os.path.join(ROOT, "content", "blog")) if f.endswith(".html")),
              key=lambda a: (a["date"], a["slug"]), reverse=True)
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
def date_fr(d):
    an, m, j = d.split("-")
    return f"{int(j)} {MOIS[int(m) - 1]} {an}"
# anciennes adresses des articles (avant le blog) : on garde une redirection
ANCIENS = ["bon-de-commande-vtc", "charges-chauffeur-vtc-auto-entrepreneur", "calcul-revenu-net-vtc", "devenir-chauffeur-vtc"]

def e(s): return html.escape(s, quote=True)

def head(title, desc, url, extra_ld, cur="blog", og="article", css=""):
    def li(href, label, key):
        c = ' aria-current="page"' if key == cur else ""
        return f'<li><a href="{href}"{c}>{label}</a></li>'
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f1116">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="{og}">
<meta property="og:site_name" content="VTC Rentable">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://app.vtcrentable.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,700..900&family=Public+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@600&display=swap">
<link rel="stylesheet" href="/assets/article.css">{css}
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
<script src="/assets/analytics.js" defer></script>
</head>
<body>
<nav class="top" aria-label="Navigation principale">
  <div class="wrap">
    <a class="logo" href="/"><img src="/icon-192.png" alt="" width="30" height="30">VTC <span>Rentable</span></a>
    <ul>
      <li><a href="/">L'appli</a></li>
      {li("/calculateurs/", "Calculateurs", "calc")}
      {li("/blog/", "Blog", "blog")}
      {li("/qui-sommes-nous/", "Qui sommes-nous", "qui-sommes-nous")}
    </ul>
    <a class="btn" href="{APP}">Ouvrir l'appli</a>
  </div>
</nav>
'''

FOOT = f'''<footer>
  <div class="wrap">
    <span>© 2026 VTC Rentable</span>
    <nav aria-label="Liens utiles">
      <a href="/">Accueil</a>
      <a href="/calculateurs/">Calculateurs</a>
      <a href="/blog/">Blog</a>
      <a href="/modeles/">Modèles gratuits</a>
      <a href="/examen-blanc-vtc/">Examen blanc VTC</a>
      <a href="/application-vtc/">Application VTC</a>
      <a href="/qui-sommes-nous/">Qui sommes-nous</a>
      <a href="{APP}">Ouvrir l'appli</a>
      <a href="https://app.vtcrentable.com/mentions-legales.html">Mentions légales</a>
      <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com · réponse sous 24 h</a>
    </nav>
  </div>
</footer>
</body>
</html>
'''

def cards(exclude=None, limit=None):
    choix = [a for a in ARTS if a["slug"] != exclude]
    if exclude and limit:   # d'abord la même catégorie, puis les plus récents
        cat = next(x["categorie"] for x in ARTS if x["slug"] == exclude)
        choix = sorted(choix, key=lambda a: a["categorie"] != cat)[:limit]
    return "\n".join(f'<a class="card" href="/blog/{a["slug"]}/" data-cat="{e(a["categorie"])}"><small class="cat">{e(a["categorie"])} · {date_fr(a["date"])}</small><b>{e(a["h1"])}</b><span>{e(a["card"])}</span></a>' for a in choix)

ORG = {"@type": "Organization", "name": "VTC Rentable", "url": SITE + "/", "logo": SITE + "/icon-192.png"}
AUTEUR = {"@type": "Person", "name": "Mohamed Amine", "jobTitle": "Chauffeur VTC et fondateur de VTC Rentable", "url": SITE + "/qui-sommes-nous/", "worksFor": ORG}
for a in ARTS:
    url = f"{SITE}/blog/{a['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": a["h1"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"],
         "inLanguage": "fr-FR", "mainEntityOfPage": url, "image": "https://app.vtcrentable.com/og-image.png", "author": AUTEUR, "publisher": ORG},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": a["short"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faq"]]}]}
    faqhtml = "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(r)}</p>" for q, r in a["faq"])
    src = "\n".join(f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in a["sources"])
    page = head(a["title"], a["desc"], url, ld) + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li><a href="/blog/">Blog</a></li><li>{e(a["short"])}</li></ol>
    <h1>{e(a["h1"])}</h1>
    <p class="lede">{e(a["lede"])}</p>
    <p class="meta">Par <a href="/qui-sommes-nous/">Mohamed Amine</a>, chauffeur VTC · {e(a["categorie"])} · Mis à jour le {date_fr(a["date"])}</p>
  </div>
</header>
<main>
<article class="read">
{a["body"]}
<div class="cta">
  <strong>Essaie VTC Rentable, c'est gratuit.</strong>
  <p>Note ta journée en une minute et vois ton revenu net, ton € / heure et ton € / km.</p>
  <a class="btn" href="{APP}">Créer mon compte gratuit</a>
</div>
<h2>En bref</h2>
{faqhtml}
<div class="src"><p><strong>Sources</strong></p><ul>
{src}
</ul></div>
</article>
<section class="more read" aria-labelledby="more-t">
  <h2 id="more-t">À lire aussi</h2>
  <div class="cards">
{cards(a["slug"], 6)}
  </div>
</section>
</main>
''' + FOOT
    os.makedirs(f"{ROOT}/blog/{a['slug']}", exist_ok=True)
    open(f"{ROOT}/blog/{a['slug']}/index.html", "w", encoding="utf-8").write(page)

# index du blog
url = SITE + "/blog/"
cats = sorted({a["categorie"] for a in ARTS})
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Blog", "name": "Blog VTC Rentable", "url": url, "inLanguage": "fr-FR", "publisher": ORG,
     "blogPost": [{"@type": "BlogPosting", "headline": a["h1"], "url": f"{SITE}/blog/{a['slug']}/", "datePublished": a["date"]} for a in ARTS]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]}]}
chips = '<button type="button" class="chip" aria-pressed="true" data-f="">Tout</button>' + "".join(f'<button type="button" class="chip" aria-pressed="false" data-f="{e(c)}">{e(c)}</button>' for c in cats)
page = head("Blog VTC Rentable : guides et conseils pour chauffeurs VTC", "Réglementation, charges, statut, rentabilité : le blog des chauffeurs VTC qui veulent savoir ce qu'ils gagnent vraiment, avec des guides clairs et à jour.", url, ld, og="website") + f'''
<style>
.chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 18px; }}
.chip {{ font: 600 14px/1 var(--f-body); border: 1px solid var(--line); background: var(--surface); color: var(--fg); padding: 9px 13px; border-radius: 999px; cursor: pointer; }}
.chip[aria-pressed=true] {{ background: var(--night); color: var(--night-fg); border-color: var(--night); }}
.card[hidden] {{ display: none; }}
</style>
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li>Blog</li></ol>
    <h1>Le blog des chauffeurs VTC</h1>
    <p class="lede">Des réponses claires aux questions qu'on se pose en roulant : réglementation, charges, statut, et comment savoir ce qu'on gagne vraiment.</p>
  </div>
</header>
<main>
<section class="more read" style="padding-top:30px" aria-label="Tous les articles">
  <div class="chips" role="group" aria-label="Filtrer par catégorie">{chips}</div>
  <div class="cards" id="liste">
{cards()}
  </div>
  <p style="color:var(--muted);margin-top:22px">Pour passer aux chiffres, essaie nos <a href="/calculateurs/">calculateurs gratuits</a> ou télécharge les <a href="/modeles/">modèles gratuits</a>.</p>
</section>
</main>
<script>
(function () {{
  var chips = document.querySelectorAll(".chip"), cards = document.querySelectorAll("#liste .card");
  chips.forEach(function (b) {{ b.addEventListener("click", function () {{
    chips.forEach(function (x) {{ x.setAttribute("aria-pressed", String(x === b)); }});
    cards.forEach(function (c) {{ c.hidden = !!b.dataset.f && c.dataset.cat !== b.dataset.f; }});
  }}); }});
}})();
</script>
''' + FOOT
os.makedirs(f"{ROOT}/blog", exist_ok=True)
open(f"{ROOT}/blog/index.html", "w", encoding="utf-8").write(page)

# redirections des anciennes adresses /articles/ vers /blog/ (GitHub Pages n'a pas de redirection côté serveur)
def redirection(vers):
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Page déplacée | VTC Rentable</title>
<link rel="canonical" href="{SITE}{vers}"><meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={vers}">
<script>location.replace("{vers}" + location.hash);</script></head>
<body><p>Cette page a déménagé : <a href="{vers}">continuer vers le blog</a>.</p></body></html>
'''
os.makedirs(f"{ROOT}/articles", exist_ok=True)
open(f"{ROOT}/articles/index.html", "w", encoding="utf-8").write(redirection("/blog/"))
for slug in ANCIENS:
    os.makedirs(f"{ROOT}/articles/{slug}", exist_ok=True)
    open(f"{ROOT}/articles/{slug}/index.html", "w", encoding="utf-8").write(redirection(f"/blog/{slug}/"))

# ---------- calculateurs ----------
CSS_CALC = '\n<link rel="stylesheet" href="/assets/calc.css">'
CALCS = [dict(slug="revenu-net-vtc", short="Revenu net VTC", h1="Calculateur de revenu net VTC",
              card="Ce qu'il te reste vraiment après commissions, charges de ton statut et frais, avec ton € / heure et ton € / km."),
         dict(slug="prix-minimum-course-vtc", short="Prix minimum d'une course", h1="Prix minimum d'une course VTC",
              card="Le montant en dessous duquel une course ne vaut pas le coup, trajet à vide compris, et le test d'une offre."),
         dict(slug="cout-voiture-km-vtc", short="Coût de la voiture au km", h1="Coût de la voiture VTC au kilomètre",
              card="Ce que te coûte vraiment ta voiture par km et par mois : perte de valeur ou location, assurance, carburant, entretien."),
         dict(slug="achat-ou-location-voiture-vtc", short="Achat ou location", h1="Voiture VTC : acheter ou louer ?",
              card="Compare le coût total d'une voiture achetée et d'une voiture louée sur la même durée, km supplémentaires compris."),
         dict(slug="comparateur-statut-vtc", short="Comparateur de statuts", h1="Quel statut pour un chauffeur VTC ?",
              card="Auto-entrepreneur, société ou rattachement : compare ce qu'il te reste chaque mois avec les mêmes chiffres."),
         dict(slug="objectif-chiffre-affaires-vtc", short="Objectif de chiffre d'affaires", h1="Objectif de chiffre d'affaires VTC",
              card="Le chiffre d'affaires à faire par semaine, par jour et par heure pour gagner le net que tu veux."),
         dict(slug="seuil-tva-vtc", short="Seuils de TVA", h1="Seuils de TVA du chauffeur VTC",
              card="Vas-tu dépasser la franchise de TVA cette année ? Projection de ton chiffre d'affaires et date de passage."),
         dict(slug="comparateur-plateformes-vtc", short="Comparateur des plateformes", h1="Comparateur des plateformes VTC",
              card="Uber, Bolt, Heetch, FreeNow : ce qu'il te reste sur une même course selon la commission de chaque plateforme."),
         dict(slug="indemnites-kilometriques-vtc", short="Indemnités kilométriques", h1="Calcul des indemnités kilométriques VTC",
              card="Le barème kilométrique 2026 selon ta voiture et tes km, et ce qu'il te fait gagner selon ton statut.")]

def calc_cards():
    return "\n".join(f'<a class="card" href="/calculateurs/{c["slug"]}/"><b>{e(c["h1"])}</b><span>{e(c["card"])}</span></a>' for c in CALCS)

def num_field(id_, label, value="", hint="", step="1"):
    h = f"<small>{hint}</small>" if hint else ""
    return f'<label for="{id_}"><span>{label}</span>{h}<input id="{id_}" type="number" inputmode="decimal" min="0" step="{step}" value="{value}"></label>'

def write_calc(c, title, desc, lede, faq, form, method, js):
    url = f"{SITE}/calculateurs/{c['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": c["h1"], "url": url, "description": desc, "applicationCategory": "FinanceApplication",
         "operatingSystem": "Navigateur web", "inLanguage": "fr-FR", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": ORG},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Calculateurs", "item": SITE + "/calculateurs/"},
            {"@type": "ListItem", "position": 3, "name": c["short"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}]}
    faqhtml = "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(r)}</p>" for q, r in faq)
    others = "\n".join(f'<a class="card" href="/calculateurs/{o["slug"]}/"><b>{e(o["h1"])}</b><span>{e(o["card"])}</span></a>' for o in CALCS if o["slug"] != c["slug"])
    others_html = f'''<section class="more read" aria-labelledby="calc-t">
  <h2 id="calc-t">Autres calculateurs</h2>
  <div class="cards">
{others}
  </div>
</section>
''' if others else ""
    page = head(title, desc, url, ld, cur="calc", og="website", css=CSS_CALC) + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li><a href="/calculateurs/">Calculateurs</a></li><li>{e(c["short"])}</li></ol>
    <h1>{e(c["h1"])}</h1>
    <p class="lede">{lede}</p>
    <p class="meta">Taux 2026 · Mis à jour le {DATE_FR}</p>
  </div>
</header>
<main>
<article class="read" style="padding-top:8px">
{form}
{method}
<h2>Questions fréquentes</h2>
{faqhtml}
</article>
{others_html}<section class="more read" aria-labelledby="more-t">
  <h2 id="more-t">À lire aussi</h2>
  <div class="cards">
{cards()}
  </div>
</section>
</main>
<script src="/assets/{js}" defer></script>
''' + FOOT
    os.makedirs(f"{ROOT}/calculateurs/{c['slug']}", exist_ok=True)
    open(f"{ROOT}/calculateurs/{c['slug']}/index.html", "w", encoding="utf-8").write(page)

# --- revenu net ---
c = CALCS[0]
url = f"{SITE}/calculateurs/{c['slug']}/"
title = "Calculateur revenu net VTC 2026 : gratuit, sans inscription"
desc = "Calcule ton revenu net de chauffeur VTC en 2026 : auto-entrepreneur, société ou rattachement, avec ACRE, versement libératoire, € / heure et € / km."
faq = [("Comment calculer son revenu net de chauffeur VTC ?",
        "Pars de ce que tu encaisses (plateformes, courses privées, pourboires), retire les charges de ton statut, tes frais de la période et tes charges mensuelles ramenées à la période (× 12 ÷ 52 pour une semaine). Le calculateur fait ces étapes pour toi."),
       ("Quel taux de cotisations pour un chauffeur VTC auto-entrepreneur en 2026 ?",
        "21,2 % du chiffre d'affaires, plus environ 0,1 % de formation professionnelle. L'ACRE réduit les cotisations de 50 % pour une activité créée avant le 1er juillet 2026, et de 25 % depuis. Le versement libératoire ajoute 1,7 %."),
       ("Faut-il saisir le montant avant ou après la commission Uber ou Bolt ?",
        "Le plus simple est de saisir ce que la plateforme te verse, donc après commission. Si tu connais le prix payé par les clients, choisis « avant commission » et indique le taux : le calculateur retire la commission pour toi."),
       ("Le résultat comprend-il l'impôt sur le revenu ?",
        "Seulement si tu as coché le versement libératoire en auto-entrepreneur, ou si ton pourcentage en société inclut l'impôt. Sinon, l'impôt sur le revenu reste à prévoir en plus.")]
form = f'''
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec l'exemple de notre article : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <div class="seg" role="group" aria-label="Période">
    <button type="button" data-p="semaine" aria-pressed="true">Semaine</button>
    <button type="button" data-p="mois" aria-pressed="false">Mois</button>
  </div>
  <fieldset>
    <legend>Ce que tu encaisses</legend>
    <div class="row">
      {num_field("ca", 'Chiffre d\'affaires sur <span data-per>la semaine</span> (€)', "1150", "Plateformes, courses privées, cash et pourboires")}
      <label for="saisie">Ce montant est
        <select id="saisie"><option value="apres">versé par les plateformes (après commission)</option><option value="avant">payé par les clients (avant commission)</option></select></label>
      <div id="opt-com" class="hide">{num_field("com", "Commission moyenne des plateformes (%)", "25")}</div>
    </div>
  </fieldset>
  <fieldset>
    <legend>Ton statut</legend>
    <div class="row">
      <label for="statut">Statut
        <select id="statut"><option value="ae">Auto-entrepreneur</option><option value="societe">Société (SASU, EURL…)</option><option value="ratt">Salarié en rattachement</option></select></label>
      <div id="opt-ae" style="display:grid;gap:12px">
        <label for="acre">ACRE
          <select id="acre"><option value="0">Pas d'ACRE</option><option value="0.5">Oui, activité créée avant le 1er juillet 2026 (− 50 %)</option><option value="0.25">Oui, activité créée depuis le 1er juillet 2026 (− 25 %)</option></select></label>
        <label class="check" for="vl"><input id="vl" type="checkbox"> Versement libératoire de l'impôt (1,7 %)</label>
      </div>
      <div id="opt-soc" class="hide">{num_field("soc", "Part du CA mise de côté pour charges et impôt (%)", "25", "Souvent autour de 25 % : fixe-la avec ton comptable")}</div>
      <div id="opt-ratt" class="hide">{num_field("ratt", "Prix du rattachement par semaine (€)", "50")}</div>
    </div>
  </fieldset>
  <fieldset>
    <legend>Tes frais sur <span data-per>la semaine</span></legend>
    <div class="row">
      {num_field("carburant", "Carburant ou recharge (€)", "105", "Souvent 8 à 10 % du CA")}
      {num_field("entretien", "Entretien et pneus (€)", "0")}
      {num_field("peage", "Péages, parking, lavage (€)", "36")}
      {num_field("repas", "Repas et cafés (€)", "45")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Tes charges mensuelles</legend>
    <div class="row">
      {num_field("voiture", "Voiture : crédit, location ou perte de valeur (€ / mois)", "0")}
      {num_field("assurance", "Assurance (€ / mois)", "160")}
      {num_field("abos", "Téléphone, comptable, abonnements (€ / mois)", "0")}
    </div>
    <p class="note">En mode semaine, elles sont ramenées à la semaine (× 12 ÷ 52).</p>
  </fieldset>
  <fieldset>
    <legend>Pour aller plus loin <small style="font:400 14px var(--f-body);color:var(--muted)">(facultatif)</small></legend>
    <div class="row">
      {num_field("heures", 'Heures travaillées sur <span data-per>la semaine</span>', "48")}
      {num_field("km", 'Kilomètres parcourus sur <span data-per>la semaine</span>', "1340")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Résultat</p>
    <p id="r-net" class="big">—</p>
    <p id="r-per" class="sub">de revenu net</p>
    <div id="r-kpis" class="kpis"></div>
    <div id="r-bar" class="bar" role="img" aria-label="Répartition du chiffre d'affaires"></div>
    <ul class="legend">
      <li style="--c:#8b93a7">Commissions</li><li style="--c:#e8743b">Charges du statut</li><li style="--c:#f7b267">Frais</li><li style="--c:#3ccf7d">Revenu net</li>
    </ul>
    <table><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Ce calcul, VTC Rentable le fait chaque semaine pour toi, à partir de ta journée notée en une minute.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif, calculé avec les taux connus en novembre 2026 ; il ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
'''
method = '''
<h2>Comment le calcul est fait</h2>
<p>Le calculateur suit la méthode détaillée dans notre article <a href="/blog/calcul-revenu-net-vtc/">Comment calculer son revenu net de chauffeur VTC</a> :</p>
<ol>
  <li><strong>Ce que tu encaisses :</strong> le montant versé par les plateformes, plus tes courses privées et tes pourboires. Si tu saisis le prix payé par les clients, la commission est retirée d'abord.</li>
  <li><strong>Les charges de ton statut :</strong> pour un auto-entrepreneur, 21,2 % du CA plus la formation professionnelle, avec l'ACRE et le versement libératoire si tu les as (détails dans <a href="/blog/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>). En société, le pourcentage que tu mets de côté. En rattachement, le prix payé chaque semaine.</li>
  <li><strong>Tes frais de la période :</strong> carburant, entretien, péages, parking, lavage et repas.</li>
  <li><strong>Tes charges mensuelles</strong>, ramenées à la semaine si besoin : voiture, assurance, téléphone, comptable.</li>
</ol>
<p>Le revenu net est ce qu'il reste. Le € / heure et le € / km se calculent sur ce net, pour voir si tes heures et tes kilomètres valent le coup.</p>
<div class="box warn"><p>L'impôt sur le revenu n'est compris que si tu as coché le versement libératoire, ou s'il est inclus dans ton pourcentage en société. Les taux changent chaque année : vérifie-les sur ton espace URSSAF.</p></div>
'''
write_calc(c, title, desc, 'Combien te reste-t-il vraiment ? Entre ce que tu encaisses, tes frais et ton statut, le calculateur te donne ton net, ton € / heure et ton € / km.', faq, form, method, "calc-revenu-net.js")

# --- prix minimum d'une course ---
c = CALCS[1]
title = "Prix minimum d'une course VTC : le calculateur gratuit 2026"
desc = "Calcule le prix minimum d'une course VTC : carburant, trajet à vide, commission, charges et objectif horaire. Teste une offre Uber ou Bolt avant d'accepter."
faq = [("Comment savoir si une course VTC est rentable ?",
        "Additionne ce que la course te coûte (carburant et entretien sur tous les kilomètres, à vide compris, et une part de tes charges fixes pour le temps passé), ajoute le revenu net que tu veux gagner, puis divise par la part qui te reste après les charges de ton statut. Si l'offre est en dessous, la course ne vaut pas le coup."),
       ("Pourquoi compter les kilomètres à vide ?",
        "Pour aller chercher le client, et parfois pour revenir d'une zone sans demande, tu roules sans être payé. Ces kilomètres coûtent autant que ceux de la course : les oublier fait paraître rentables des courses qui ne le sont pas."),
       ("Quel taux de charges indiquer ?",
        "En auto-entrepreneur, environ 21,3 % du CA en 2026 (21,2 % de cotisations URSSAF et 0,1 % de formation), 23 % avec le versement libératoire. En société, le pourcentage que tu mets de côté, souvent autour de 25 %. En rattachement, mets 0 et ajoute le prix du rattachement à tes charges fixes mensuelles."),
       ("Le montant affiché est-il avant ou après la commission ?",
        "Le résultat principal est le montant versé par la plateforme, après commission : c'est celui que tu vois sur l'offre. Le prix client minimum, avant commission, est affiché à côté.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>La course</legend>
    <div class="row">
      {num_field("kmc", "Distance de la course (km)", "12", step="0.1")}
      {num_field("minc", "Durée de la course (min)", "25")}
      {num_field("kmv", "Km à vide : approche et retour (km)", "4", "Pour aller chercher le client ou revenir en zone", step="0.1")}
      {num_field("minv", "Temps d'approche (min)", "8")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Ta voiture</legend>
    <div class="row">
      {num_field("conso", "Consommation (L ou kWh / 100 km)", "5", step="0.1")}
      {num_field("prixcarb", "Prix du carburant ou de l'électricité (€ / L ou kWh)", "1.75", step="0.01")}
      {num_field("entretien", "Entretien et pneus (€ / km)", "0.05", "Souvent entre 0,03 et 0,08 €", step="0.01")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Tes charges et ton objectif</legend>
    <div class="row">
      {num_field("fixes", "Charges fixes par mois (€)", "600", "Voiture, assurance, téléphone, rattachement…")}
      {num_field("heuresmois", "Heures travaillées par mois", "200")}
      {num_field("com", "Commission de la plateforme (%)", "25", "0 pour une course privée")}
      {num_field("stat", "Charges de ton statut (% du CA)", "21.3", "Auto-entrepreneur : 21,2 % URSSAF + 0,1 % formation = 21,3 % ; avec versement libératoire : 23 %", step="0.1")}
      {num_field("objh", "Revenu net visé (€ / heure)", "15")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Tester une offre <small style="font:400 14px var(--f-body);color:var(--muted)">(facultatif)</small></legend>
    <div class="row">
      {num_field("offre", "Montant proposé par la plateforme (€)", "14", "Le montant versé, affiché sur l'offre", step="0.01")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Minimum à accepter</p>
    <p id="r-net" class="big">—</p>
    <p class="sub">versés par la plateforme, pour atteindre ton objectif horaire</p>
    <div id="r-verdict" class="verdict"></div>
    <div id="r-kpis" class="kpis"></div>
    <table><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Avec VTC Rentable, tu vois chaque semaine ton vrai € / heure et ton € / km, pour savoir quelles courses te rapportent vraiment.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif ; il ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment le calcul est fait</h2>
<ol>
  <li><strong>Le coût de la route :</strong> carburant et entretien sur tous les kilomètres, ceux de la course et ceux faits à vide.</li>
  <li><strong>La part de tes charges fixes :</strong> tes charges du mois divisées par tes heures travaillées, multipliées par le temps de la course et de l'approche.</li>
  <li><strong>Ton objectif :</strong> le revenu net que tu veux gagner par heure, sur ce même temps.</li>
  <li><strong>Les charges de ton statut :</strong> le total est divisé par la part qui te reste après les charges (par exemple 78,7 % en auto-entrepreneur), pour que l'objectif soit atteint une fois l'URSSAF payée.</li>
</ol>
<p>On obtient le montant minimum que la plateforme doit te verser. Divisé par la part qui te reste après sa commission, il donne le prix minimum payé par le client.</p>
<p>Pour suivre ces chiffres sur toute ta semaine, et pas seulement course par course, utilise le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net VTC</a> ou lis <a href="/blog/calcul-revenu-net-vtc/">comment calculer son revenu net</a>.</p>
<div class="box warn"><p>Les montants proposés par les plateformes changent selon l'heure et la demande. Le calculateur donne un repère pour décider ; c'est à toi de juger si une course mal payée te place bien pour la suivante.</p></div>"""
write_calc(c, title, desc, "Une course qui paie peu, avec du trajet à vide, peut te coûter de l'argent. Calcule le montant en dessous duquel elle ne vaut pas le coup, et teste une offre avant d'accepter.", faq, form, method, "calc-prix-minimum.js")

# --- coût de la voiture au km ---
c = CALCS[2]
title = "Coût de la voiture VTC au km : calculateur gratuit 2026"
desc = "Calcule le coût réel de ta voiture VTC au kilomètre et par mois : perte de valeur ou location, crédit, assurance, carburant, entretien et pneus."
faq = [("Comment calculer le coût au kilomètre d'une voiture VTC ?",
        "Additionne tout ce que la voiture te coûte sur un an (perte de valeur ou location, intérêts du crédit, assurance, carburant, entretien, pneus, contrôle technique) et divise par le nombre de kilomètres parcourus dans l'année."),
       ("Comment compter le prix d'achat de la voiture ?",
        "Ce n'est pas le prix d'achat qui compte, mais ce que tu perds : prix d'achat moins prix de revente prévu, divisé par la durée pendant laquelle tu la gardes. Une voiture achetée 15 000 € et revendue 4 000 € après 3 ans coûte environ 3 667 € par an."),
       ("Pourquoi mon coût au km baisse-t-il quand je roule plus ?",
        "Une partie du coût est fixe : l'assurance, la location ou la perte de valeur se paient même quand la voiture ne roule pas. Plus tu fais de kilomètres, plus ces coûts sont répartis, et plus le coût de chaque kilomètre baisse."),
       ("Les kilomètres à vide comptent-ils ?",
        "Oui. Indique tous les kilomètres de l'année, y compris ceux faits sans client : ils usent la voiture et consomment du carburant comme les autres.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ta voiture</legend>
    <div class="row">
      <label for="mode">Tu es
        <select id="mode"><option value="achat">propriétaire (achat, avec ou sans crédit)</option><option value="location">en location (LLD, LOA, loueur VTC)</option></select></label>
      {num_field("kman", "Kilomètres par an", "50000", "Tous les km, à vide compris")}
    </div>
    <div id="opt-achat" class="row" style="margin-top:14px">
      {num_field("achat", "Prix d'achat (€)", "15000")}
      {num_field("revente", "Prix de revente prévu (€)", "4000")}
      {num_field("mois", "Durée d'utilisation (mois)", "36")}
      {num_field("interets", "Intérêts du crédit, au total (€)", "0", "0 si achat comptant")}
    </div>
    <div id="opt-loc" class="row hide" style="margin-top:14px">
      {num_field("loyer", "Loyer mensuel (€)", "650")}
      <label class="check" for="assinc"><input id="assinc" type="checkbox"> Assurance incluse dans le loyer</label>
    </div>
  </fieldset>
  <fieldset>
    <legend>Assurance et carburant</legend>
    <div class="row">
      <div id="f-ass">{num_field("assurance", "Assurance VTC (€ / mois)", "160")}</div>
      {num_field("conso", "Consommation (L ou kWh / 100 km)", "5", step="0.1")}
      {num_field("prixcarb", "Prix du carburant ou de l'électricité (€ / L ou kWh)", "1.75", step="0.01")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Entretien, par an</legend>
    <div class="row">
      {num_field("entretien", "Révisions et réparations (€ / an)", "1500")}
      {num_field("pneus", "Pneus (€ / an)", "600")}
      {num_field("divers", "Contrôle technique, lavage, divers (€ / an)", "200")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Coût réel de ta voiture</p>
    <p id="r-net" class="big">—</p>
    <p class="sub">par kilomètre, tout compris</p>
    <div id="r-kpis" class="kpis"></div>
    <div id="r-bar" class="bar" role="img" aria-label="Répartition du coût de la voiture"></div>
    <ul class="legend"><li style="--c:#e8743b">Coûts fixes</li><li style="--c:#f7b267">Coûts liés aux km</li></ul>
    <table><thead><tr><th>Poste</th><th class="n">Par mois</th><th class="n">Par km</th></tr></thead><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>VTC Rentable compte le coût de ta voiture chaque semaine, avec la perte de valeur, pour que ton revenu net soit le vrai.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment le calcul est fait</h2>
<ol>
  <li><strong>La voiture elle-même :</strong> si tu l'as achetée, ce que tu perds (prix d'achat moins prix de revente) réparti sur ta durée d'utilisation, plus les intérêts du crédit. Si tu la loues, le loyer.</li>
  <li><strong>L'assurance</strong>, sauf si elle est comprise dans la location.</li>
  <li><strong>Le carburant :</strong> tes kilomètres de l'année × ta consommation × le prix du litre ou du kWh.</li>
  <li><strong>L'entretien :</strong> révisions, réparations, pneus, contrôle technique et lavage.</li>
</ol>
<p>Le total de l'année, divisé par tes kilomètres, donne le coût au kilomètre. Les coûts fixes sont ceux que tu paies même sans rouler : c'est pour ça qu'une voiture peu utilisée revient cher au kilomètre.</p>
<p>Salarié en rattachement ou président de SASU avec ta propre voiture ? Compare ce coût réel au barème officiel avec le <a href="/calculateurs/indemnites-kilometriques-vtc/">calculateur des indemnités kilométriques</a>.</p>
<p>Ce coût au km sert à savoir si une course vaut le coup : reprends-le dans le <a href="/calculateurs/prix-minimum-course-vtc/">calculateur du prix minimum d'une course</a>, ou suis ton net complet avec le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net</a>.</p>"""
write_calc(c, title, desc, "Carburant, assurance, perte de valeur ou location, entretien : calcule ce que ta voiture te coûte vraiment par kilomètre et par mois.", faq, form, method, "calc-cout-voiture.js")

# --- achat ou location ---
c = CALCS[3]
title = "Voiture VTC : acheter ou louer ? Le comparateur gratuit 2026"
desc = "Acheter ou louer sa voiture VTC ? Compare le coût total sur la durée : perte de valeur, crédit, assurance, entretien, loyers et km supplémentaires."
faq = [("Vaut-il mieux acheter ou louer sa voiture VTC ?",
        "Ça dépend de tes chiffres. L'achat revient souvent moins cher sur plusieurs années si tu revends bien, mais il faut avancer l'argent et assumer les pannes. La location coûte parfois plus, mais tout est prévisible et souvent inclus. Le comparateur fait le calcul sur la même durée."),
       ("Faut-il compter le carburant dans la comparaison ?",
        "Non, tant que tu compares la même voiture : le carburant est le même dans les deux cas. Le comparateur ne retient que ce qui change entre l'achat et la location."),
       ("Comment compter le prix d'achat ?",
        "Ce qui compte, c'est ce que tu perds : prix d'achat moins prix de revente au bout de la durée, plus les intérêts du crédit si tu en as un. Le montant à financer est affiché à part, car il pèse sur ta trésorerie."),
       ("Que signifie le forfait de kilomètres ?",
        "Beaucoup de contrats de location limitent les kilomètres par an et facturent chaque km en plus. En VTC on roule beaucoup : indique ce forfait et le prix du km supplémentaire, ou 0 si le kilométrage est illimité.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ton usage</legend>
    <div class="row">
      {num_field("mois", "Durée à comparer (mois)", "36")}
      {num_field("kman", "Kilomètres par an", "50000")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Si tu achètes</legend>
    <div class="row">
      {num_field("achat", "Prix d'achat (€)", "15000")}
      {num_field("revente", "Prix de revente à la fin (€)", "4000")}
      {num_field("interets", "Intérêts du crédit, au total (€)", "1200", "0 si achat comptant")}
      {num_field("assachat", "Assurance VTC (€ / mois)", "160")}
      {num_field("entachat", "Entretien et pneus (€ / an)", "2100")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Si tu loues</legend>
    <div class="row">
      {num_field("loyer", "Loyer (€ / mois)", "650")}
      {num_field("frais", "Frais de mise en route (€)", "0", "Frais de dossier, premier loyer majoré…")}
      {num_field("kminclus", "Km inclus par an", "0", "0 si kilométrage illimité")}
      {num_field("prixkm", "Prix du km supplémentaire (€)", "0.10", step="0.01")}
      <label class="check" for="assinc"><input id="assinc" type="checkbox" checked> Assurance incluse</label>
      <label class="check" for="entinc"><input id="entinc" type="checkbox" checked> Entretien et pneus inclus</label>
      <div id="f-assloc" class="hide">{num_field("assloc", "Assurance (€ / mois)", "160")}</div>
      <div id="f-entloc" class="hide">{num_field("entloc", "Entretien et pneus (€ / an)", "1500")}</div>
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">L'option la moins chère</p>
    <p id="r-net" class="big">—</p>
    <p id="r-sub" class="sub"></p>
    <div id="r-kpis" class="kpis"></div>
    <table><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Achat ou location, VTC Rentable compte le coût de ta voiture chaque semaine dans ton revenu net.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif : le carburant n'est pas compté, car il est le même dans les deux cas. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment le calcul est fait</h2>
<p>Le comparateur additionne, sur la même durée, ce que chaque option te coûte vraiment :</p>
<ul>
  <li><strong>À l'achat :</strong> la perte de valeur (prix d'achat moins prix de revente), les intérêts du crédit, l'assurance et l'entretien.</li>
  <li><strong>En location :</strong> les loyers, les frais de mise en route, l'assurance et l'entretien s'ils ne sont pas inclus, et les kilomètres au-delà du forfait.</li>
</ul>
<p>Le carburant n'est pas compté, puisqu'il est le même dans les deux cas. Pour connaître le coût complet de ta voiture au kilomètre, carburant compris, utilise le <a href="/calculateurs/cout-voiture-km-vtc/">calculateur du coût de la voiture au km</a>.</p>
<div class="box warn"><p>Le coût n'est pas le seul critère. L'achat demande d'avancer de l'argent et te fait porter le risque d'une panne ou d'une revente difficile. La location est prévisible, mais le contrat peut limiter les kilomètres ou imposer une durée. Lis bien ce qui est inclus avant de signer.</p></div>"""
write_calc(c, title, desc, "Perte de valeur, crédit et entretien d'un côté, loyers et kilomètres en plus de l'autre : compare le vrai coût des deux options sur la même durée.", faq, form, method, "calc-achat-location.js")

# --- comparateur de statuts ---
c = CALCS[4]
title = "Statut VTC : auto-entrepreneur, société ou rattachement ?"
desc = "Compare ton revenu net de chauffeur VTC en auto-entrepreneur, en société ou en rattachement, avec les mêmes chiffres. Plafond micro et TVA inclus."
faq = [("Quel est le meilleur statut pour un chauffeur VTC ?",
        "Il n'y a pas de réponse unique : tout dépend de ton chiffre d'affaires, de tes frais et de tes projets. L'auto-entreprise est simple et adaptée au démarrage, dans la limite de 83 600 € de CA par an. La société permet de déduire les frais et de grossir. Le rattachement évite les démarches, contre un prix chaque semaine."),
       ("Pourquoi l'auto-entrepreneur paie-t-il des charges sur tout le chiffre d'affaires ?",
        "En micro-entreprise, les cotisations se calculent sur le CA encaissé, pas sur le bénéfice : 21,2 % en 2026 plus la formation professionnelle. Si tes frais sont élevés, une société, qui calcule ses charges après les frais, peut devenir plus intéressante."),
       ("Le pourcentage indiqué pour la société est-il exact ?",
        "Non, c'est une estimation. En société, ce que tu paies dépend de la rémunération que tu te verses, des dividendes et de ta situation fiscale. Le comparateur utilise un pourcentage du CA mis de côté, souvent autour de 25 % : fais-le fixer par ton comptable."),
       ("Que compter pour le rattachement ?",
        "Le prix payé chaque semaine à la société de rattachement. Si elle retient aussi des cotisations ou un pourcentage sur ce qu'elle te verse, indique-le dans le champ des retenues.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, la comparaison se met à jour toute seule.</p>
  <fieldset>
    <legend>Ton activité</legend>
    <div class="row">
      {num_field("ca", "Chiffre d'affaires par semaine (€)", "1150", "Ce que les plateformes te versent, plus tes courses privées")}
      {num_field("frais", "Frais par semaine (€)", "291", "Carburant, repas, péages, parking, lavage")}
      {num_field("charges", "Charges mensuelles de la voiture (€)", "460", "Assurance, location ou crédit, téléphone")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Auto-entrepreneur</legend>
    <div class="row">
      <label for="acre">ACRE
        <select id="acre"><option value="0">Pas d'ACRE</option><option value="0.5">Activité créée avant le 1er juillet 2026 (− 50 %)</option><option value="0.25">Activité créée depuis le 1er juillet 2026 (− 25 %)</option></select></label>
      <label class="check" for="vl"><input id="vl" type="checkbox"> Versement libératoire de l'impôt (1,7 %)</label>
    </div>
  </fieldset>
  <fieldset>
    <legend>Société (SASU, EURL…)</legend>
    <div class="row">
      {num_field("soc", "Part du CA pour charges et impôt (%)", "25", "Estimation : à fixer avec ton comptable")}
      {num_field("compta", "Comptable et banque pro (€ / mois)", "100")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Rattachement</legend>
    <div class="row">
      {num_field("ratt", "Prix du rattachement (€ / semaine)", "50")}
      {num_field("rattpct", "Retenues supplémentaires (% du CA)", "0", "Si ta société retient des cotisations ou un pourcentage", step="0.1")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Le statut qui te laisse le plus</p>
    <p id="r-net" class="big">—</p>
    <p id="r-sub" class="sub"></p>
    <div id="r-kpis" class="kpis"></div>
    <p id="r-base" class="sub" style="margin:0 0 6px"></p>
    <table class="small"><thead><tr><th>Statut</th><th class="n">Charges</th><th class="n">Net</th></tr></thead><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Quel que soit ton statut, VTC Rentable calcule chaque semaine tes charges et ton vrai revenu net.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Comparaison indicative avec les taux connus en novembre 2026 ; l'impôt sur le revenu n'est compris que si tu coches le versement libératoire ou s'il est inclus dans ton pourcentage en société. Elle ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment la comparaison est faite</h2>
<p>Les trois statuts partent du même chiffre d'affaires, des mêmes frais et des mêmes charges de voiture, ramenés au mois (× 52 ÷ 12). Seules les charges du statut changent :</p>
<ul>
  <li><strong>Auto-entrepreneur :</strong> 21,2 % du CA et la formation professionnelle, réduits par l'ACRE, plus 1,7 % avec le versement libératoire. Détails dans <a href="/blog/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>.</li>
  <li><strong>Société :</strong> la part du CA mise de côté pour les charges et l'impôt, plus le comptable et la banque.</li>
  <li><strong>Rattachement :</strong> le prix payé chaque semaine, et les retenues éventuelles.</li>
</ul>
<p>Le comparateur signale aussi quand ton CA annuel dépasse la franchise de TVA (37 500 €) ou le plafond de la micro-entreprise (83 600 €).</p>
<div class="box warn"><p>Le choix d'un statut ne se résume pas au net du mois : protection sociale, retraite, démarches, possibilité d'embaucher ou d'acheter une voiture au nom de la société comptent aussi. Prends conseil auprès d'un comptable avant de changer.</p></div>"""
write_calc(c, title, desc, "Avec le même chiffre d'affaires et les mêmes frais, compare ce qu'il te reste chaque mois en auto-entrepreneur, en société et en rattachement.", faq, form, method, "calc-statuts.js")

# --- objectif de chiffre d'affaires ---
c = CALCS[5]
title = "Chiffre d'affaires VTC : combien faire pour gagner 2 000 € ?"
desc = "Calcule le chiffre d'affaires VTC à faire par semaine, par jour et par heure pour gagner le net que tu veux, selon ton statut, tes frais et tes congés."
faq = [("Quel chiffre d'affaires faire en VTC pour gagner 2 000 € nets par mois ?",
        "Ça dépend de ton statut et de tes frais. Avec l'exemple du calculateur (auto-entrepreneur, frais variables de 25 % du CA, 460 € de charges fixes par mois et 47 semaines travaillées par an), il faut environ 4 580 € de CA par mois, soit près de 1 170 € par semaine travaillée."),
       ("Pourquoi compter les semaines de congés ?",
        "Tes charges fixes tombent tous les mois, même quand tu ne roules pas. Si tu prends cinq semaines de congés, ton chiffre d'affaires de l'année doit être fait en 47 semaines : chaque semaine travaillée doit donc rapporter un peu plus."),
       ("Que mettre dans les frais variables ?",
        "Ce qui augmente quand tu roules plus : carburant, entretien, péages, repas, lavage. Exprime-les en pourcentage de ton chiffre d'affaires : par exemple 291 € de frais pour 1 150 € encaissés, c'est environ 25 %."),
       ("Le net calculé est-il avant ou après impôt ?",
        "Avant l'impôt sur le revenu, sauf si tu coches le versement libératoire en auto-entrepreneur, ou si ton pourcentage en société comprend l'impôt.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ton objectif</legend>
    <div class="row">
      {num_field("net", "Revenu net voulu (€ / mois)", "2000")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Ton statut</legend>
    <div class="row">
      <label for="statut">Statut
        <select id="statut"><option value="ae">Auto-entrepreneur</option><option value="societe">Société (SASU, EURL…)</option><option value="ratt">Salarié en rattachement</option></select></label>
      <div id="opt-ae" style="display:grid;gap:12px">
        <label for="acre">ACRE
          <select id="acre"><option value="0">Pas d'ACRE</option><option value="0.5">Activité créée avant le 1er juillet 2026 (− 50 %)</option><option value="0.25">Activité créée depuis le 1er juillet 2026 (− 25 %)</option></select></label>
        <label class="check" for="vl"><input id="vl" type="checkbox"> Versement libératoire de l'impôt (1,7 %)</label>
      </div>
      <div id="opt-soc" class="hide" style="display:grid;gap:12px">{num_field("soc", "Part du CA pour charges et impôt (%)", "25", "Estimation : à fixer avec ton comptable")}{num_field("compta", "Comptable et banque pro (€ / mois)", "100")}</div>
      <div id="opt-ratt" class="hide">{num_field("ratt", "Prix du rattachement (€ / semaine)", "50")}</div>
    </div>
  </fieldset>
  <fieldset>
    <legend>Tes frais</legend>
    <div class="row">
      {num_field("var", "Frais variables (% du CA)", "25", "Carburant, entretien, péages, repas", step="0.5")}
      {num_field("fixes", "Charges fixes (€ / mois)", "460", "Assurance, voiture, téléphone")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Ton rythme</legend>
    <div class="row">
      {num_field("semaines", "Semaines travaillées par an", "47", "52 moins tes congés")}
      {num_field("jours", "Jours travaillés par semaine", "6")}
      {num_field("heures", "Heures par jour", "9", step="0.5")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Ton objectif</p>
    <p id="r-net" class="big">—</p>
    <p id="r-sub" class="sub"></p>
    <div id="r-kpis" class="kpis"></div>
    <table><tbody id="r-tab"></tbody></table>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Fixe ton objectif dans VTC Rentable et vois chaque jour où tu en es.</p>
      <a class="btn" href="{APP}">Suivre mon objectif gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif avec les taux connus en novembre 2026 ; il ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment le calcul est fait</h2>
<p>Le calculateur part du net que tu veux et remonte au chiffre d'affaires :</p>
<ol>
  <li>Il ajoute à ton objectif tes <strong>charges fixes</strong> du mois (et le rattachement ou le comptable selon ton statut).</li>
  <li>Il divise ce total par la <strong>part qui te reste sur chaque euro encaissé</strong>, une fois retirés les frais variables et les charges de ton statut. En auto-entrepreneur sans ACRE, avec 25 % de frais variables, il reste environ 54 centimes par euro.</li>
  <li>Il répartit le chiffre d'affaires de l'année sur tes <strong>semaines travaillées</strong>, puis sur tes jours et tes heures.</li>
</ol>
<p>Pour vérifier où tu en es, compare ce rythme à ton chiffre réel avec le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net</a>, et vérifie qu'une course précise vaut le coup avec le <a href="/calculateurs/prix-minimum-course-vtc/">prix minimum d'une course</a>.</p>"""
write_calc(c, title, desc, "Tu vises un certain revenu net par mois ? Calcule le chiffre d'affaires à faire par semaine, par jour et par heure pour l'atteindre, congés compris.", faq, form, method, "calc-objectif-ca.js")

# --- seuils de TVA ---
c = CALCS[6]
title = "Seuil de TVA VTC 2026 : vas-tu dépasser la franchise ?"
desc = "Franchise de TVA 2026 pour un chauffeur VTC : seuils de 37 500 € et 41 250 €, projection de ton chiffre d'affaires et date de dépassement, TVA à 10 %."
faq = [("Quels sont les seuils de TVA pour un chauffeur VTC en 2026 ?",
        "Pour les prestations de services, la franchise en base s'applique jusqu'à 37 500 € de chiffre d'affaires hors taxes par an, avec un seuil majoré de 41 250 €. Le projet de baisse à 25 000 € a été abandonné."),
       ("Que se passe-t-il si je dépasse 37 500 € ?",
        "Si tu restes sous 41 250 €, tu gardes la franchise jusqu'à la fin de l'année, et la TVA s'applique à partir du 1er janvier suivant. Si tu dépasses 41 250 €, la franchise cesse dès le jour du dépassement."),
       ("Quel taux de TVA pour une course VTC ?",
        "Le transport de personnes relève du taux réduit de 10 %. Une course facturée uniquement à la durée, comme une mise à disposition à l'heure, peut relever du taux de 20 %."),
       ("Faut-il compter le prix payé par le client ou ce que verse Uber ?",
        "Le prix total de la course, payé par le client, commission comprise : c'est ce chiffre qui se compare aux seuils. Si tu ne connais que les montants versés par les plateformes, le calculateur les convertit avec ta commission moyenne.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ton chiffre d'affaires</legend>
    <div class="row">
      {num_field("caan", "Chiffre depuis le 1er janvier (€)", "25000", "Plateformes, courses privées et pourboires")}
      {num_field("mois", "Nombre de mois écoulés", "10", "Mois complets depuis janvier")}
      {num_field("caprec", "Chiffre de l'an dernier (€)", "28000", "0 si tu as commencé cette année")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Base du calcul</legend>
    <div class="row">
      <label for="base">Les montants saisis sont
        <select id="base"><option value="verse">ce que versent les plateformes (après commission)</option><option value="prix">le prix total des courses (avant commission)</option></select></label>
      <div id="f-com">{num_field("com", "Commission moyenne des plateformes (%)", "25", "Pour retrouver le prix total des courses")}</div>
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Ton chiffre d'affaires de l'année, au rythme actuel</p>
    <p id="r-net" class="big">—</p>
    <p class="sub">projection sur 12 mois</p>
    <div id="r-verdict" class="verdict"></div>
    <div id="r-kpis" class="kpis"></div>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>VTC Rentable suit ton chiffre d'affaires de l'année et te montre où tu en es par rapport aux seuils.</p>
      <a class="btn" href="{APP}">Suivre mon chiffre gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif avec les seuils connus en novembre 2026 ; il ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Comment le calcul est fait</h2>
<ol>
  <li><strong>L'année dernière :</strong> si ton chiffre a dépassé 37 500 €, la franchise ne s'applique plus cette année.</li>
  <li><strong>Cette année :</strong> le calculateur prend ton chiffre depuis janvier, le divise par les mois écoulés et le projette sur 12 mois.</li>
  <li><strong>Le verdict :</strong> sous 37 500 €, tu restes en franchise ; entre 37 500 € et 41 250 €, la TVA s'applique au 1er janvier suivant ; au-delà de 41 250 €, dès le jour du dépassement, dont il estime le mois.</li>
</ol>
<p>La TVA estimée correspond à 10 % du prix hors taxe sur une année au même rythme. Ce que tu reverses vraiment est plus bas, car tu récupères la TVA payée sur tes dépenses professionnelles.</p>
<div class="box warn"><p><strong>Attention à la base :</strong> le chiffre qui se compare aux seuils est le prix total des courses payé par les clients, commission comprise, et non ce qui arrive sur ton compte. Avec 25 % de commission, l'écart est d'environ un tiers : beaucoup de chauffeurs dépassent la franchise sans le savoir. La commission facturée depuis l'étranger peut aussi entraîner une autoliquidation de TVA : fais le point avec ton comptable.</p></div>
<p>Pour voir l'effet sur ce qu'il te reste, utilise le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a> et lis <a href="/blog/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>.</p>
<div class="src"><p><strong>Sources</strong></p><ul>
<li><a href="https://www.superindep.fr/blog/2024/nouveautes-tva-2025/" rel="noopener">Seuils de TVA en microentreprise 2026 (SuperIndep)</a></li>
<li><a href="https://pro.credit-agricole.fr/tva/vtc" rel="noopener">Quelle TVA s'applique aux chauffeurs VTC (Crédit Agricole Pro)</a></li>
<li><a href="https://hayot-expertise.fr/blog/vtc-tva-commission-uber-deduction-vehicule-2026" rel="noopener">VTC : TVA 10 %, commission Uber et déduction du véhicule (Hayot Expertise)</a></li>
</ul></div>"""
write_calc(c, title, desc, "Vas-tu dépasser la franchise de TVA cette année ? À partir de ton chiffre depuis janvier, le calculateur projette ton année et te dit quand la TVA s'appliquera.", faq, form, method, "calc-seuil-tva.js")

# --- comparateur des plateformes ---
c = CALCS[7]
title = "Commission Uber, Bolt, Heetch, FreeNow : comparateur 2026"
desc = "Compare ce qu'il te reste sur une course VTC selon la plateforme : commissions Uber, Bolt, Heetch et FreeNow en 2026, modifiables, et écart par mois."
faq = [("Quelle commission prend Uber sur un chauffeur VTC ?",
        "Depuis fin 2024, Uber applique une commission variable selon la course, entre environ 3 % et 45 % d'après les chiffres rapportés, avec une moyenne annoncée autour de 25 %. Le plus fiable est de calculer ta moyenne à partir de tes propres relevés."),
       ("Quelle plateforme VTC prend le moins de commission ?",
        "Parmi les grandes plateformes, Heetch annonce les commissions les plus basses pour les indépendants, autour de 18 %. Bolt et FreeNow se situent autour de 20 à 24 %. Mais une commission plus basse ne fait pas forcément gagner plus si tu as moins de courses."),
       ("La commission est-elle hors taxe ou TTC ?",
        "Ça dépend de la plateforme. FreeNow annonce par exemple 20 % hors taxe, soit 24 % une fois la TVA ajoutée. Compare toujours des taux sur la même base."),
       ("Les chiffres de ce comparateur sont-ils à jour ?",
        "Les taux préremplis sont des repères publics relevés en novembre 2026. Ils changent souvent et varient selon la ville : remplace-les par ceux de tes relevés de paiement.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Taux préremplis avec des repères publics de novembre 2026 : remplace-les par ceux de tes relevés.</p>
  <fieldset>
    <legend>La course</legend>
    <div class="row">
      {num_field("prix", "Prix payé par le client (€)", "30", step="0.5")}
      {num_field("cout", "Coût de la course pour toi (€)", "4", "Carburant, entretien, temps à vide : voir le calculateur du prix minimum", step="0.1")}
      {num_field("stat", "Charges de ton statut (% du CA)", "21.3", "Auto-entrepreneur : 21,2 % URSSAF + 0,1 % formation = 21,3 %", step="0.1")}
      {num_field("courses", "Courses par semaine", "60", "Pour estimer l'écart sur un mois")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Commission de chaque plateforme (%)</legend>
    <div class="row">
      {num_field("c-uber", "Uber", "25", "Variable selon la course ; moyenne annoncée", step="0.1")}
      {num_field("c-bolt", "Bolt", "24", "24 % en Île-de-France et grandes villes", step="0.1")}
      {num_field("c-heetch", "Heetch", "18", "Indépendants, en évolution en 2026", step="0.1")}
      {num_field("c-freenow", "FreeNow", "24", "20 % hors taxe, 24 % TTC", step="0.1")}
      <label for="nomautre"><span>Autre plateforme ou ta clientèle</span><small>Facultatif : LeCab, Allocab, courses privées…</small><input id="nomautre" type="text" value="" maxlength="30" placeholder="Nom"></label>
      {num_field("c-autre", "Sa commission", "0", step="0.1")}
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">La plateforme qui te laisse le plus</p>
    <p id="r-net" class="big">—</p>
    <p id="r-sub" class="sub"></p>
    <div id="r-bars"></div>
    <ul class="legend"><li style="--c:#3ccf7d">Ce qu'il te reste</li><li style="--c:#f7b267">Charges et coût de la course</li></ul>
    <div id="r-kpis" class="kpis"></div>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>VTC Rentable sépare tes recettes par plateforme et te montre laquelle te rapporte vraiment le plus chaque semaine.</p>
      <a class="btn" href="{APP}">Comparer mes plateformes gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Les repères de novembre 2026</h2>
<p>Ces chiffres viennent de sources publiques et varient selon la ville, le type de course et le contrat. Ils servent de point de départ, pas de vérité.</p>
<div class="tbl"><table>
  <thead><tr><th>Plateforme</th><th>Commission annoncée</th><th>Ce qu'on en dit</th></tr></thead>
  <tbody>
    <tr><td><strong>Uber</strong></td><td>Variable par course depuis fin 2024 (environ 3 % à 45 %), moyenne annoncée autour de 25 %</td><td>Clientèle d'affaires, aéroports, majorations fortes ; critères d'entrée stricts</td></tr>
    <tr><td><strong>Bolt</strong></td><td>Environ 19 à 24 % selon la ville, 24 % en Île-de-France</td><td>Bonus d'inscription, concurrence sur les prix, majorations plus faibles</td></tr>
    <tr><td><strong>Heetch</strong></td><td>Autour de 18 % pour les indépendants, modèle en évolution en 2026</td><td>Courses de nuit et en périphérie, inscription plus simple</td></tr>
    <tr><td><strong>FreeNow</strong></td><td>20 % hors taxe, soit 24 % TTC</td><td>Forfaits aéroports, courses réservées à l'avance</td></tr>
  </tbody>
</table></div>
<div class="box"><p><strong>À savoir :</strong> en octobre et novembre 2026, Uber, Bolt, FreeNow, Heetch et LeCab ont relevé temporairement leur garantie de revenu minimum de 30 à 32 € par heure d'activité. Elle ne change pas le prix de chaque course.</p></div>
<h2>Comment le calcul est fait</h2>
<p>Pour chaque plateforme, le comparateur part du prix payé par le client, retire la commission pour obtenir le montant versé, puis les charges de ton statut et le coût de la course. Le coût de la course, tu peux l'obtenir avec le <a href="/calculateurs/prix-minimum-course-vtc/">calculateur du prix minimum d'une course</a>.</p>
<p>Une commission plus basse ne vaut que si tu as autant de courses. Le meilleur juge reste ton net de la semaine par plateforme : suis-le avec le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net</a>.</p>
<div class="src"><p><strong>Sources</strong></p><ul>
<li><a href="https://www.keobiz.fr/fiches-pratiques/creer-activite-vtc/plateformes-vtc-uber-bolt-heetch/" rel="noopener">Plateformes VTC Uber, Bolt, Heetch (Keobiz, septembre 2026)</a></li>
<li><a href="https://up-cab.com/commission-vtc-uber-bolt-heetch" rel="noopener">Commission Uber, Bolt, Heetch 2026 (Up!, plateforme concurrente, octobre 2026)</a></li>
<li><a href="https://www.portail-autoentrepreneur.fr/academie/comparatifs/plateformes/choix-plateforme-vtc" rel="noopener">Choisir sa plateforme VTC (Portail Auto-Entrepreneur)</a></li>
<li><a href="https://lautomobiliste.fr/30/09/2026/vtc-frevalorisation-revenu-minimum-chauffeurs-octobre-novembre-2026/" rel="noopener">Revalorisation du revenu minimum des chauffeurs (L'Automobiliste, septembre 2026)</a></li>
</ul></div>"""
write_calc(c, title, desc, "Sur une même course, combien te reste-t-il avec Uber, Bolt, Heetch ou FreeNow ? Compare avec les repères de 2026 ou avec tes propres taux.", faq, form, method, "calc-plateformes.js")

# --- indemnités kilométriques ---
c = CALCS[8]
title = "Calcul indemnités kilométriques VTC 2026 : barème officiel"
desc = "Calcule tes indemnités kilométriques de chauffeur VTC avec le barème 2026 : salarié en rattachement, SASU, auto-entrepreneur, électrique + 20 %."
faq = [("Un chauffeur VTC a-t-il droit aux indemnités kilométriques ?",
        "Ça dépend du statut. Le salarié en rattachement qui utilise sa propre voiture peut déduire ses frais avec le barème en optant pour les frais réels. Le président de SASU peut se faire verser des indemnités par sa société s'il roule avec sa voiture personnelle. L'auto-entrepreneur n'y a pas droit : son abattement forfaitaire couvre déjà tous ses frais."),
       ("Quel est le barème kilométrique 2026 ?",
        "Le barème utilisé en 2026 pour déclarer les revenus de 2025 n'a pas été revalorisé : il est identique à celui de 2024 et 2025. Pour une 5 CV au-delà de 20 000 km par an, il donne 0,427 € par km. Il est majoré de 20 % pour une voiture 100 % électrique."),
       ("Peut-on ajouter le carburant ou l'assurance aux indemnités kilométriques ?",
        "Non. Le barème couvre la perte de valeur de la voiture, l'entretien, les réparations, les pneus, le carburant et l'assurance. Si la voiture est louée, le loyer est aussi couvert. Les péages et le stationnement peuvent en revanche s'ajouter, avec justificatifs."),
       ("Une voiture de plus de 7 CV donne-t-elle plus d'indemnités ?",
        "Non. Le barème s'arrête à la ligne « 7 CV et plus » : une voiture de 8 ou 11 CV est comptée comme une 7 CV.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ton statut</legend>
    <div class="row">
      <label for="statut">Tu roules en tant que
        <select id="statut"><option value="ratt">Salarié en rattachement, avec ta voiture</option><option value="sasu">Président de SASU, avec ta voiture personnelle</option><option value="ae">Auto-entrepreneur</option><option value="ei">Entreprise individuelle au réel</option></select></label>
    </div>
  </fieldset>
  <fieldset>
    <legend>Ta voiture et tes kilomètres</legend>
    <div class="row">
      <label for="cv">Puissance fiscale (carte grise, case P.6)
        <select id="cv"><option value="3">3 CV et moins</option><option value="4">4 CV</option><option value="5" selected>5 CV</option><option value="6">6 CV</option><option value="7">7 CV et plus</option></select></label>
      <label for="elec">Motorisation
        <select id="elec"><option value="0">Essence, diesel ou hybride</option><option value="1">100 % électrique (+ 20 %)</option></select></label>
      {num_field("km", "Kilomètres professionnels sur l'année", "45000", "Courses, approches et trajets entre deux courses")}
    </div>
  </fieldset>
  <fieldset id="f-ratt">
    <legend>Ta déclaration de revenus</legend>
    <div class="row">
      {num_field("sal", "Salaire net imposable de l'année (€)", "15000", "Sur tes bulletins de paie ou ta déclaration préremplie")}
      {num_field("indem", "Frais déjà remboursés par l'employeur (€)", "8000", "Indemnités non imposables versées par la société de rattachement")}
      {num_field("autres", "Autres frais réels (€)", "1500", "Péages, parking, repas sur la route, téléphone")}
      <label for="tmi">Ta tranche d'imposition
        <select id="tmi"><option value="0">0 % (non imposable)</option><option value="0.11" selected>11 %</option><option value="0.30">30 %</option><option value="0.41">41 %</option></select></label>
    </div>
  </fieldset>
  <fieldset id="f-sasu" class="hide">
    <legend>Ta société</legend>
    <div class="row">
      {num_field("cout", "Coût réel de ta voiture sur l'année (€)", "0", "Facultatif : pour comparer, voir le calculateur du coût au km")}
      <label for="is">Taux d'impôt sur les sociétés
        <select id="is"><option value="0.15">15 % (bénéfice jusqu'à 42 500 €)</option><option value="0.25">25 %</option></select></label>
    </div>
  </fieldset>

  <div class="res" aria-live="polite">
    <p class="k">Tes indemnités kilométriques sur l'année</p>
    <p id="r-net" class="big">—</p>
    <p id="r-sub" class="sub"></p>
    <div id="r-verdict" class="verdict"></div>
    <div id="r-kpis" class="kpis"></div>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>VTC Rentable enregistre tes kilomètres jour après jour : tu as ton total de l'année prêt pour ta déclaration.</p>
      <a class="btn" href="{APP}">Suivre mes kilomètres gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif avec le barème publié en avril 2026 ; il ne remplace pas l'avis d'un comptable. Tes chiffres restent sur ton appareil. <button type="button" id="raz" style="font:inherit;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline">Revenir à l'exemple</button></p>
</form>
"""
method = """<h2>Le barème kilométrique 2026</h2>
<p>C'est le barème publié en avril 2026 pour déclarer les revenus de 2025. Il n'a pas été revalorisé depuis 2023. Il sert aussi d'estimation pour les kilomètres de 2026, en attendant le barème de 2027. <em>d</em> représente la distance professionnelle parcourue dans l'année.</p>
<div class="tbl"><table>
  <thead><tr><th>Puissance</th><th>Jusqu'à 5 000 km</th><th>De 5 001 à 20 000 km</th><th>Au-delà de 20 000 km</th></tr></thead>
  <tbody>
    <tr><td><strong>3 CV et moins</strong></td><td>d × 0,529</td><td>(d × 0,316) + 1 065</td><td>d × 0,370</td></tr>
    <tr><td><strong>4 CV</strong></td><td>d × 0,606</td><td>(d × 0,340) + 1 330</td><td>d × 0,407</td></tr>
    <tr><td><strong>5 CV</strong></td><td>d × 0,636</td><td>(d × 0,357) + 1 395</td><td>d × 0,427</td></tr>
    <tr><td><strong>6 CV</strong></td><td>d × 0,665</td><td>(d × 0,374) + 1 457</td><td>d × 0,447</td></tr>
    <tr><td><strong>7 CV et plus</strong></td><td>d × 0,697</td><td>(d × 0,394) + 1 515</td><td>d × 0,470</td></tr>
  </tbody>
</table></div>
<p>Pour une voiture 100 % électrique, le résultat est majoré de 20 %. Un chauffeur VTC dépasse presque toujours 20 000 km par an : c'est la dernière colonne qui s'applique.</p>
<h2>Comment le calcul est fait</h2>
<ol>
  <li><strong>Les indemnités :</strong> le calculateur applique la ligne de ta puissance fiscale et la colonne de ton kilométrage, puis la majoration si ta voiture est électrique.</li>
  <li><strong>Salarié en rattachement :</strong> il compare la déduction forfaitaire de 10 % (au minimum 509 € et au maximum 14 555 € pour les revenus de 2025) à tes frais réels, c'est-à-dire tes indemnités plus tes autres frais. Les frais déjà remboursés par ton employeur sont ajoutés à ton revenu, comme le demande l'administration quand on choisit les frais réels.</li>
  <li><strong>Président de SASU :</strong> les indemnités que la société te verse ne sont pas imposables pour toi, dans la limite du barème, et elles sont déduites de son bénéfice. Le calculateur estime l'impôt sur les sociétés évité et, si tu indiques le coût réel de ta voiture, l'écart entre les deux.</li>
</ol>
<div class="box warn"><p><strong>Ce que le barème couvre déjà :</strong> perte de valeur, entretien, réparations, pneus, carburant, assurance, et le loyer si la voiture est louée. Tu ne peux pas les ajouter en plus. Les péages et le stationnement, eux, s'ajoutent avec leurs justificatifs. Garde un relevé de tes trajets : sans lui, les indemnités peuvent être refusées en cas de contrôle.</p></div>
<p>Pour aller plus loin, lis <a href="/blog/indemnites-kilometriques-vtc/">qui a droit aux indemnités kilométriques en VTC</a>, compare avec le <a href="/calculateurs/cout-voiture-km-vtc/">coût réel de ta voiture au km</a> et vérifie ton statut avec le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a>.</p>
<div class="src"><p><strong>Sources</strong></p><ul>
<li><a href="https://www.service-public.gouv.fr/particuliers/actualites/A14686" rel="noopener">Barème kilométrique 2026 pour la déclaration des revenus 2025 (Service-public.fr, avril 2026)</a></li>
<li><a href="https://www.weblex.fr/chiffres-cles/deduction-forfaitaire-de-10-pour-frais-professionnels-declaration-2026" rel="noopener">Déduction forfaitaire de 10 % pour la déclaration 2026 (WebLex)</a></li>
</ul></div>"""
write_calc(c, title, desc, "Combien valent tes kilomètres avec le barème officiel, et est-ce que tu peux vraiment t'en servir ? Le calculateur répond selon ton statut : rattachement, SASU ou auto-entrepreneur.", faq, form, method, "calc-ik.js")

# index des calculateurs
url = SITE + "/calculateurs/"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "Calculateurs pour chauffeurs VTC", "url": url, "inLanguage": "fr-FR",
     "hasPart": [{"@type": "WebApplication", "name": c["h1"], "url": f"{SITE}/calculateurs/{c['slug']}/"} for c in CALCS]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Calculateurs", "item": url}]}]}
page = head("Calculateurs gratuits pour chauffeurs VTC | VTC Rentable", "Calculateurs gratuits et sans inscription pour chauffeurs VTC : revenu net, charges, € / heure et € / km, avec les taux 2026.", url, ld, cur="calc", og="website") + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li>Calculateurs</li></ol>
    <h1>Calculateurs pour chauffeurs VTC</h1>
    <p class="lede">Des outils gratuits, sans inscription, pour savoir ce que tu gagnes vraiment. Tes chiffres restent sur ton appareil.</p>
  </div>
</header>
<main>
<section class="more read" style="padding-top:36px" aria-label="Tous les calculateurs">
  <div class="cards">
{calc_cards()}
  </div>
</section>
<section class="more read" aria-labelledby="art-t">
  <h2 id="art-t">Nos guides</h2>
  <div class="cards">
{cards()}
  </div>
</section>
</main>
''' + FOOT
open(f"{ROOT}/calculateurs/index.html", "w", encoding="utf-8").write(page)

# ---------- modèles gratuits ----------
url = SITE + "/modeles/"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": "Modèles gratuits pour chauffeurs VTC", "url": url, "inLanguage": "fr-FR"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Modèles gratuits", "item": url}]}]}
page = head("Modèles VTC gratuits : tableau de suivi et checklist frais", "Télécharge gratuitement un tableau Excel de suivi de semaine VTC et une checklist des frais à imprimer, pour savoir ce que tu gagnes vraiment.", url, ld, cur="modeles", og="website", css=CSS_CALC) + f"""
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li>Modèles gratuits</li></ol>
    <h1>Modèles gratuits pour chauffeurs VTC</h1>
    <p class="lede">Un tableau de suivi de ta semaine et une checklist des frais à ne pas oublier. Laisse ton adresse e-mail et télécharge-les tout de suite.</p>
  </div>
</header>
<main>
<article class="read" style="padding-top:8px">
<div class="modeles">
  <div class="modele"><p class="fmt">Excel · .xlsx</p><b>Tableau de suivi de la semaine</b><span>Recettes par plateforme, carburant, heures et km jour par jour. Il calcule ton revenu net, ton € / heure et ton € / km, avec les charges de ton statut.</span></div>
  <div class="modele"><p class="fmt">PDF · 1 page A4</p><b>Checklist des frais du chauffeur VTC</b><span>32 frais à cocher, de l'assurance à la CFE, pour être sûr de ne rien oublier dans ton calcul de rentabilité.</span></div>
</div>
<form id="modeles-form" class="calc" novalidate>
  <fieldset>
    <legend>Recevoir les modèles</legend>
    <div style="display:grid;gap:14px">
      <label for="m-email"><span>Ton adresse e-mail</span><input id="m-email" type="email" autocomplete="email" maxlength="254" required></label>
      <div style="display:grid;gap:8px">
        <label class="check" for="m-tab"><input id="m-tab" type="checkbox" name="modele" value="tableau-suivi" checked> Tableau de suivi de la semaine</label>
        <label class="check" for="m-chk"><input id="m-chk" type="checkbox" name="modele" value="checklist-frais" checked> Checklist des frais</label>
      </div>
      <label class="consent" for="m-ok"><input id="m-ok" type="checkbox" required> <span>J'accepte que VTC Rentable conserve mon adresse pour m'envoyer ces modèles et, de temps en temps, des conseils et nouveautés pour chauffeurs VTC. Je peux demander sa suppression à tout moment en écrivant à <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a>.</span></label>
      <div><button id="m-btn" class="btn" type="submit">Recevoir les modèles</button></div>
    </div>
    <p id="m-msg" class="m-msg" role="alert"></p>
  </fieldset>
</form>
<div id="m-done" class="calc done" hidden tabindex="-1">
  <b style="font:800 21px/1.25 var(--f-display)">Merci ! Tes modèles sont prêts.</b>
  <a id="dl-tableau-suivi" class="btn" href="/assets/modeles/tableau-suivi-vtc.xlsx" target="_blank" rel="noopener" type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" hidden>Télécharger le tableau de suivi (.xlsx)</a>
  <a id="dl-checklist-frais" class="btn" href="/assets/modeles/checklist-frais-vtc.pdf" target="_blank" rel="noopener" type="application/pdf" hidden>Télécharger la checklist des frais (.pdf)</a>
  <p style="color:var(--muted);margin:0;font-size:14.5px">Sur iPhone, le fichier s'ouvre en aperçu : touche le bouton Partager, puis « Enregistrer dans Fichiers ». Si rien ne se passe, ouvre cette page dans Safari.</p>
  <p style="color:var(--muted);margin:0">Pour aller plus vite que le tableur, essaie l'appli <a href="{APP}">VTC Rentable</a> : elle fait ces calculs pour toi chaque semaine.</p>
</div>
<p style="color:var(--muted);font-size:14px;margin-top:16px">Ton adresse est enregistrée de façon sécurisée et n'est jamais revendue.</p>
<h2>Et pour un calcul rapide</h2>
<p>Pas envie d'un tableur ? Les <a href="/calculateurs/">calculateurs gratuits</a> donnent ton revenu net, le prix minimum d'une course ou le coût de ta voiture en quelques secondes, sans inscription.</p>
</article>
</main>
<script src="/assets/modeles.js" defer></script>
""" + FOOT
os.makedirs(f"{ROOT}/modeles", exist_ok=True)
open(f"{ROOT}/modeles/index.html", "w", encoding="utf-8").write(page)

# pages stratégiques et Qui sommes-nous
exec(open(os.path.join(ROOT, "outils", "pages_landing.py"), encoding="utf-8").read())
exec(open(os.path.join(ROOT, "outils", "page_examen_blanc.py"), encoding="utf-8").read())

# sitemap
urls = [(SITE + "/", "1.0"), (SITE + "/calculateurs/", "0.8")] + [(f"{SITE}/calculateurs/{c['slug']}/", "0.9") for c in CALCS] \
     + [(SITE + "/modeles/", "0.6"), (SITE + "/blog/", "0.7")] + [(f"{SITE}/blog/{a['slug']}/", "0.8") for a in ARTS] \
     + [(f"{SITE}/{p}/", "0.6" if p == "qui-sommes-nous" else "0.9") for p in LANDING]
LASTMOD = {f"{SITE}/examen-blanc-vtc/": "2026-11-09"}   # date propre aux pages ajoutées après la dernière mise à jour générale
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{u}</loc><lastmod>{LASTMOD.get(u, DATE)}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
open(f"{ROOT}/sitemap.xml", "w").write(sm)
print("ok", [len(a["title"]) for a in ARTS], [len(a["desc"]) for a in ARTS])
