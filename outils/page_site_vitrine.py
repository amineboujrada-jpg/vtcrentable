# Landing de vente « Site vitrine chauffeur VTC » — incluse par pages_landing.py (exec).
# Reprend la feuille de style de l'accueil (index.html) pour garder le même design, plus quelques styles propres à la page.
import re as _re

_slug = "site-vitrine-chauffeur-vtc"
_url = f"{SITE}/{_slug}/"
_title = "Site chauffeur VTC avec réservation en ligne : 19,99 €/mois"
_desc = "Un site vitrine à ton nom, avec réservation en ligne et bon de commande automatique, visible sur Google dans ta ville. 19,99 € par mois, sans engagement."
assert len(_title) <= 60 and 70 <= len(_desc) <= 160

_home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_css_home = _re.search(r"<style>(.*?)</style>", _home, _re.S).group(1)

_faq = [
    ("Combien coûte un site internet pour chauffeur VTC ?",
     "19,99 € par mois, sans frais de création et sans engagement. Tu peux arrêter à tout moment."),
    ("Est-ce que je paie une commission sur les réservations ?",
     "Non. Les réservations faites sur ton site sont des courses privées : tu fixes ton prix et tu gardes la totalité, sans commission de plateforme."),
    ("Le bon de commande est-il fait automatiquement ?",
     "Oui. Chaque réservation reçue par ton site crée un bon de commande PDF avec les mentions obligatoires et l'heure de la commande, à présenter en cas de contrôle."),
    ("Combien de temps faut-il pour avoir mon site ?",
     "Après ta demande, on te rappelle sous 48 h pour récupérer tes informations. Le site t'est ensuite envoyé pour validation avant sa mise en ligne."),
    ("Je peux arrêter quand je veux ?",
     "Oui. L'abonnement est sans engagement : tu l'arrêtes quand tu veux, sans frais."),
    ("Il faut que j'utilise l'appli VTC Rentable ?",
     "Non, le site vitrine est une option à part. L'appli reste gratuite, et tu peux utiliser l'une sans l'autre."),
]

_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "@id": _url, "url": _url, "name": _title, "description": _desc, "inLanguage": "fr-FR",
     "publisher": ORG, "breadcrumb": {"@id": _url + "#fil"}},
    {"@type": "Service", "name": "Site vitrine avec réservation en ligne pour chauffeur VTC",
     "serviceType": "Création et hébergement de site internet pour chauffeur VTC",
     "description": "Site d'une page au nom du chauffeur, réservation en ligne, bon de commande PDF automatique et référencement local.",
     "provider": ORG, "areaServed": {"@type": "Country", "name": "France"}, "url": _url,
     "offers": {"@type": "Offer", "price": "19.99", "priceCurrency": "EUR", "url": _url + "#demande",
                "priceSpecification": {"@type": "UnitPriceSpecification", "price": "19.99", "priceCurrency": "EUR",
                                       "unitText": "MONTH", "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MON"}}}},
    {"@type": "BreadcrumbList", "@id": _url + "#fil", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Site vitrine chauffeur VTC", "item": _url}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in _faq]},
]}

_faqhtml = "\n".join(f"        <details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in _faq)

_css_page = """
/* ---------- Page site vitrine ---------- */
[hidden] { display: none !important; }
.hero .phone.real img { aspect-ratio: 780 / 1688; }
.offer-badge { display: inline-flex; align-items: baseline; gap: 8px; margin-top: 22px; padding: 10px 14px; border: 1px solid var(--night-line); border-radius: 12px; }
.offer-badge b { font: 600 26px/1 var(--f-num); color: var(--night-fg); white-space: nowrap; }
@media (max-width: 860px) { .hero .offer-badge { order: 5; margin-top: 18px; } }
.offer-badge span { color: var(--night-muted); font-size: 14px; }
.compare { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.compare > div { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: 22px 24px; display: grid; gap: 10px; align-content: start; }
.compare .cap { font: 600 11.5px/1 var(--f-num); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.compare h3 { font-size: 21px; font-weight: 800; }
.compare ul { margin: 0; padding-left: 18px; color: var(--muted); display: grid; gap: 6px; font-size: 15px; }
.compare .good { border: 2px solid var(--net); }
.compare .good .cap { color: var(--net); }
@media (max-width: 760px) { .compare { grid-template-columns: 1fr; } }
.steps.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 900px) { .steps.four { grid-template-columns: 1fr 1fr; } }
@media (max-width: 560px) { .steps.four { grid-template-columns: 1fr; } }
.price .cta-row { grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.price .cta-row span { color: var(--muted); font-size: 14px; }
.req { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 32px; align-items: start; }
.req-side { display: grid; gap: 14px; }
.req-side p { color: var(--muted); font-size: 16px; }
.req-side ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }
.req-side li { display: flex; gap: 10px; } .req-side li::before { content: "✓"; color: var(--net); font-weight: 800; }
.req-form { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: 24px; display: grid; gap: 14px; }
.req-form label { display: grid; gap: 6px; font-size: 14px; font-weight: 600; }
.req-form input[type=text], .req-form input[type=tel], .req-form input[type=email], .req-form textarea { width: 100%; font: 500 16px/1.3 var(--f-body); color: var(--fg); background: var(--bg); border: 1px solid var(--line); border-radius: 10px; padding: 12px; }
.req-form textarea { resize: vertical; }
.req-form .two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.req-form .consent { display: grid; grid-template-columns: 20px 1fr; gap: 10px; font-weight: 400; color: var(--muted); font-size: 13.5px; }
.req-form .consent input { width: 18px; height: 18px; margin-top: 2px; }
.req-form .btn { width: 100%; }
.m-msg { font-size: 14.5px; margin: 0; } .m-msg.err { color: var(--charge); font-weight: 600; }
.req-done { background: var(--surface); border: 2px solid var(--net); border-radius: 18px; padding: 24px; display: grid; gap: 10px; }
.req-done b { font: 800 22px/1.25 var(--f-display); }
.req-done p { color: var(--muted); }
.req-note { color: var(--muted); font-size: 13.5px; margin-top: 12px; }
@media (max-width: 860px) { .req { grid-template-columns: 1fr; gap: 20px; } }
@media (max-width: 480px) { .req-form .two { grid-template-columns: 1fr; } .req-form { padding: 18px; } }
"""

_page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f1116">
<title>{e(_title)}</title>
<meta name="description" content="{e(_desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{_url}">
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VTC Rentable">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{_url}">
<meta property="og:title" content="Ton site de chauffeur VTC avec réservation en ligne · 19,99 €/mois">
<meta property="og:description" content="{e(_desc)}">
<meta property="og:image" content="https://app.vtcrentable.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(_ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Public+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>{_css_home}{_css_page}</style>
</head>
<body>
<header class="night">
  <nav class="top" aria-label="Navigation principale">
    <div class="wrap">
      <a class="logo" href="/"><img src="/icon-192.png" alt="" width="30" height="30">VTC <span>Rentable</span></a>
      <ul>
        <li><a href="#exemple">Exemple</a></li>
        <li><a href="#inclus">Ce qui est compris</a></li>
        <li><a href="#prix">Prix</a></li>
        <li><a href="#faq">Questions</a></li>
        <li><a href="/">L'appli gratuite</a></li>
      </ul>
      <a class="btn btn-amber" href="#demande">Demander mon site</a>
    </div>
  </nav>

  <div class="hero" id="top">
    <div class="wrap">
      <div class="hero-text">
        <h1><span class="eyebrow h1-kicker">Site vitrine pour chauffeurs VTC</span> Tes clients réservent chez toi. <em>Sans commission.</em></h1>
        <p class="lead">On crée ton site à ton nom, avec la réservation en ligne et le bon de commande automatique. Tes clients fidèles réservent en deux minutes, et tu gardes tout le prix de la course.</p>
        <ul class="gains">
          <li><span><b>Un site à ton nom</b>, ton véhicule, tes zones et tes tarifs</span></li>
          <li><span><b>La réservation en ligne</b>, de jour comme de nuit</span></li>
          <li><span><b>Visible sur Google</b> quand on cherche un VTC dans ta ville</span></li>
        </ul>
        <div class="ctas">
          <a class="btn btn-amber" href="#demande">Demander mon site</a>
          <a class="btn btn-ghost" href="#exemple">Voir un exemple</a>
        </div>
        <div class="offer-badge"><b>19,99 €</b><span>par mois · sans engagement · sans frais de création</span></div>
      </div>
      <div class="phone real">
        <img src="/assets/captures/exemple-site-accueil.webp" width="780" height="1688" alt="Exemple fictif de site vitrine de chauffeur VTC sur téléphone : nom, ville, services et bouton Réserver" fetchpriority="high">
      </div>
    </div>
  </div>
</header>

<main>
  <section class="block" id="exemple">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Exemple</p>
        <h2>Voilà à quoi ressemble ton site.</h2>
        <p>Trois écrans d'un site créé avec l'offre, sur téléphone. Ton site reprendra ton nom, ton véhicule, tes zones et tes prix.</p>
      </div>
      <div class="shots">
        <figure class="shot"><img src="/assets/captures/exemple-site-accueil.webp" width="780" height="1688" loading="lazy" alt="Exemple fictif : accueil du site d'un chauffeur VTC à Lyon"><figcaption><b>L'accueil</b><span>Ton nom, ta ville, tes services et le bouton Réserver.</span></figcaption></figure>
        <figure class="shot"><img src="/assets/captures/exemple-site-reservation.webp" width="780" height="1688" loading="lazy" alt="Exemple fictif : formulaire de réservation avec départ, arrivée, date et heure"><figcaption><b>La réservation</b><span>Départ, arrivée, date, heure et coordonnées du client.</span></figcaption></figure>
        <figure class="shot"><img src="/assets/captures/exemple-site-bon.webp" width="780" height="1688" loading="lazy" alt="Exemple fictif : confirmation de réservation et bon de commande PDF"><figcaption><b>La confirmation</b><span>Avec le bon de commande PDF créé automatiquement.</span></figcaption></figure>
      </div>
      <p class="demo-note">Exemple fictif réalisé pour illustrer l'offre : ce chauffeur n'existe pas.</p>
    </div>
  </section>

  <section class="block tight" id="pourquoi">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Pourquoi</p>
        <h2>Une course en direct, c'est tout pour toi.</h2>
        <p>Sur une course privée, il n'y a pas de commission de plateforme. 19,99 € par mois, c'est moins qu'une seule course aéroport.</p>
      </div>
      <div class="compare">
        <div>
          <p class="cap">Via une plateforme</p>
          <h3>Le client est celui de la plateforme</h3>
          <ul>
            <li>La plateforme prend sa commission sur chaque course</li>
            <li>Le prix est fixé par l'algorithme</li>
            <li>Le client satisfait ne peut pas te redemander</li>
          </ul>
        </div>
        <div class="good">
          <p class="cap">Avec ton site</p>
          <h3>Le client est le tien</h3>
          <ul>
            <li>Aucune commission : tu gardes tout le prix</li>
            <li>Tu fixes tes tarifs et tes forfaits</li>
            <li>Il réserve chez toi la fois suivante, en deux minutes</li>
          </ul>
        </div>
      </div>
      <p class="demo-note" style="margin-top:14px">Le détail de ce qu'il reste après les charges est dans notre article sur le <a href="/blog/salaire-chauffeur-vtc/">salaire d'un chauffeur VTC</a>.</p>
    </div>
  </section>

  <section class="block tight" id="inclus">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Ce qui est compris</p>
        <h2>Tout ce qu'il faut pour recevoir des réservations.</h2>
      </div>
      <div class="feats">
        <div class="feat"><div class="ic c1" aria-hidden="true">1</div><h3>Un site à ton nom</h3><p>Une page claire : ta présentation, ton véhicule, tes zones de prise en charge, tes tarifs et forfaits, ton contact.</p></div>
        <div class="feat"><div class="ic c2" aria-hidden="true">2</div><h3>La réservation en ligne</h3><p>Le client choisit la date, l'heure, le départ et l'arrivée. Tu reçois la demande et tu la confirmes.</p></div>
        <div class="feat"><div class="ic c3" aria-hidden="true">3</div><h3>Le bon de commande automatique</h3><p>Chaque réservation crée le <a href="/blog/bon-de-commande-vtc/">bon de commande</a> PDF avec les mentions obligatoires et l'heure de la commande.</p></div>
        <div class="feat"><div class="ic c4" aria-hidden="true">4</div><h3>Visible sur Google</h3><p>On t'aide à créer ou améliorer ta fiche Google et on prépare ton site pour ressortir sur « chauffeur VTC » dans ta ville.</p></div>
        <div class="feat"><div class="ic c5" aria-hidden="true">5</div><h3>Pensé pour le téléphone</h3><p>Tes clients réservent depuis leur téléphone : le site est conçu d'abord pour un petit écran.</p></div>
        <div class="feat"><div class="ic c6" aria-hidden="true">6</div><h3>Mis en ligne pour toi</h3><p>Tu n'as rien de technique à faire : on crée le site, on le met en ligne, tu le valides.</p></div>
      </div>
    </div>
  </section>

  <section class="block tight" id="etapes">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Comment ça se passe</p>
        <h2>Ton site en quatre étapes.</h2>
      </div>
      <div class="steps four">
        <div class="step"><h3>Tu envoies ta demande</h3><p>Avec le formulaire en bas de page : une minute suffit.</p></div>
        <div class="step"><h3>On t'appelle</h3><p>Sous 48 h, pour récupérer ton nom, ton véhicule, tes zones et tes tarifs.</p></div>
        <div class="step"><h3>On crée ton site</h3><p>Tu le reçois pour validation et tu demandes les changements avant la mise en ligne.</p></div>
        <div class="step"><h3>Tu reçois tes réservations</h3><p>19,99 € par mois, et tu arrêtes quand tu veux.</p></div>
      </div>
    </div>
  </section>

  <section class="block tight" id="prix">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Prix</p>
        <h2>Un prix simple, sans engagement.</h2>
      </div>
      <div class="price">
        <div class="big">19,99 €<small>par mois,<br>sans frais de création</small></div>
        <ul>
          <li>Un site d'une page à ton nom</li>
          <li>Réservation en ligne</li>
          <li>Bon de commande PDF automatique</li>
          <li>Référencement local et fiche Google</li>
          <li>Adapté au téléphone</li>
          <li>Sans engagement, arrêt à tout moment</li>
        </ul>
        <div class="cta-row"><a class="btn btn-amber" href="#demande">Demander mon site</a><span>L'appli VTC Rentable reste gratuite, avec ou sans site.</span></div>
      </div>
    </div>
  </section>

  <section class="block tight" id="demande">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Demande</p>
        <h2>Demander mon site.</h2>
      </div>
      <div class="req">
        <div class="req-side">
          <p>Laisse tes coordonnées : on te rappelle sous 48 h pour préparer ton site avec toi.</p>
          <ul>
            <li>Aucun paiement à cette étape</li>
            <li>Tu valides le site avant sa mise en ligne</li>
            <li>19,99 € par mois ensuite, sans engagement</li>
          </ul>
        </div>
        <div>
          <form id="site-form" class="req-form" novalidate>
            <label for="s-nom">Nom et prénom<input id="s-nom" type="text" autocomplete="name" maxlength="100" required></label>
            <div class="two">
              <label for="s-tel">Téléphone<input id="s-tel" type="tel" autocomplete="tel" maxlength="30" required></label>
              <label for="s-email">E-mail<input id="s-email" type="email" autocomplete="email" maxlength="254" required></label>
            </div>
            <label for="s-ville">Ville ou zone où tu travailles<input id="s-ville" type="text" autocomplete="address-level2" maxlength="100" required></label>
            <label for="s-message">Un message (facultatif)<textarea id="s-message" rows="3" maxlength="1000" placeholder="Ton véhicule, tes trajets habituels, une question…"></textarea></label>
            <label class="consent" for="s-ok"><input id="s-ok" type="checkbox" required><span>J'accepte que VTC Rentable conserve ces informations pour me recontacter au sujet du site vitrine. Je peux demander leur suppression à tout moment à contact@vtcrentable.com.</span></label>
            <button id="s-btn" class="btn btn-amber" type="submit">Envoyer ma demande</button>
            <p id="s-msg" class="m-msg" role="alert"></p>
          </form>
          <div id="s-done" class="req-done" hidden tabindex="-1">
            <b>Merci, ta demande est bien envoyée.</b>
            <p>On te rappelle sous 48 h pour préparer ton site. En attendant, tu peux suivre ton activité avec l'appli <a href="{APP}">VTC Rentable</a>, gratuite.</p>
          </div>
          <p class="req-note">Tes informations sont enregistrées de façon sécurisée, ne servent qu'à te recontacter et ne sont jamais revendues.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="block tight" id="faq">
    <div class="wrap">
      <div class="sec-head">
        <p class="eyebrow">Questions</p>
        <h2>Questions fréquentes</h2>
      </div>
      <div class="faq">
{_faqhtml}
      </div>
    </div>
  </section>

  <section class="night final">
    <div class="wrap">
      <h2>Ton prochain client fidèle réserve chez toi.</h2>
      <p>Ton site à ton nom, la réservation en ligne et le bon de commande automatique, pour 19,99 € par mois.</p>
      <a class="btn btn-amber" href="#demande">Demander mon site</a>
      <div class="support"><b>Une question ?</b><a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a><span>Réponse sous 24 h, par un chauffeur qui connaît le métier.</span></div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <span>© 2026 VTC Rentable · créée par un chauffeur VTC</span>
    <nav aria-label="Liens utiles">
      <a href="/">VTC Rentable, l'appli gratuite</a>
      <a href="/calculateurs/">Calculateurs pour chauffeurs VTC</a>
      <a href="/blog/">Blog pour chauffeurs VTC</a>
      <a href="/qui-sommes-nous/">Qui sommes-nous</a>
      <a href="{APP}mentions-legales.html">Mentions légales</a>
      <a href="{APP}confidentialite.html">Politique de confidentialité</a>
      <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com · réponse sous 24 h</a>
    </nav>
  </div>
</footer>
<script src="/assets/demande-site.js" defer></script>
</body>
</html>
'''

os.makedirs(f"{ROOT}/{_slug}", exist_ok=True)
open(f"{ROOT}/{_slug}/index.html", "w", encoding="utf-8").write(_page)
LANDING.append(_slug)
