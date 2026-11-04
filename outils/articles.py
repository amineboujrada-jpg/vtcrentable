import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-04"
DATE_FR = "4 novembre 2026"
APP = "https://app.vtcrentable.com/"
SITE = "https://vtcrentable.com"

ARTS = [
 dict(slug="bon-de-commande-vtc", short="Bon de commande VTC",
  title="Bon de commande VTC : les 7 mentions obligatoires en 2026",
  desc="Justificatif de réservation VTC : les 7 mentions obligatoires depuis l'arrêté du 6 août 2025, sur papier ou téléphone, et ce qu'il faut en contrôle.",
  h1="Bon de commande VTC : les 7 mentions obligatoires",
  lede="Depuis le 30 octobre 2025, le justificatif de réservation préalable suit de nouvelles règles. Voici ce qu'il doit contenir, et comment l'avoir sur toi à chaque course.",
  card="Les 7 informations à faire figurer sur le justificatif de réservation, selon l'arrêté du 6 août 2025.",
  body="""
<p>Un VTC ne peut pas prendre un client qui le hèle dans la rue : chaque course doit avoir été réservée avant. En cas de contrôle, tu dois pouvoir le prouver avec un <strong>justificatif de réservation préalable</strong>, que beaucoup de chauffeurs appellent bon de commande ou bon de réservation.</p>
<p>Pour une course Uber, Bolt ou Heetch, la plateforme s'en charge dans son application. Le sujet concerne surtout <strong>tes clients en direct</strong> : un habitué qui t'appelle, un hôtel, une réservation par SMS ou WhatsApp.</p>

<h2>Ce qui a changé en 2025</h2>
<p>Un arrêté du 6 août 2025, publié au Journal officiel le 29 août 2025, a remplacé celui de 2013. Il s'applique depuis le 30 octobre 2025. Il ajoute deux informations sur l'exploitant (son numéro au registre VTC et son numéro SIREN) et assouplit la règle sur les coordonnées du client.</p>

<h2>Les 7 mentions obligatoires</h2>
<ol>
  <li><strong>Le nom ou la dénomination sociale de l'exploitant</strong>, et ses coordonnées. L'exploitant, c'est l'entreprise qui fait la course : ta société, ton auto-entreprise ou ta société de rattachement.</li>
  <li><strong>Le numéro d'inscription de l'exploitant au registre des VTC.</strong></li>
  <li><strong>Le numéro unique d'identification de l'exploitant</strong>, c'est-à-dire son numéro SIREN.</li>
  <li><strong>Le nom et le numéro de téléphone du client</strong> qui a réservé.</li>
  <li><strong>La date et l'heure de la réservation</strong>, autrement dit le moment où le client a commandé.</li>
  <li><strong>La date et l'heure de prise en charge</strong> souhaitées par le client.</li>
  <li><strong>Le lieu de prise en charge</strong> indiqué par le client.</li>
</ol>
<div class="box">
  <p><strong>Si le nom ou le téléphone du client manque</strong> sur le justificatif, le texte te laisse une solution : donner sans attendre aux agents de contrôle un moyen de joindre le client.</p>
</div>
<p>La destination, le prix ou le nombre de passagers ne font pas partie des mentions obligatoires. Les noter reste utile pour toi et pour le client.</p>

<h2>Papier ou téléphone ?</h2>
<p>Les deux sont acceptés. Ce qui compte, c'est de pouvoir le montrer tout de suite, même sans réseau dans un parking souterrain. Garde donc une version enregistrée sur le téléphone, pas seulement un lien à ouvrir.</p>
<p>L'heure de réservation est le point sensible : elle doit être antérieure à la prise en charge. Un justificatif rempli à la main après coup, ou dont l'heure de commande se modifie facilement, ne te protège pas vraiment.</p>

<h2>Ce que tu risques sans justificatif</h2>
<p>Prendre un client sans réservation préalable est sanctionné par le Code des transports. Les cas les plus graves relèvent de l'article L. 3124-12, qui prévoit jusqu'à un an d'emprisonnement et 15 000 € d'amende, avec des peines complémentaires comme la suspension du permis ou l'immobilisation du véhicule. D'autres manquements relèvent d'une contravention de 5e classe.</p>
<div class="box warn">
  <p>Cet article résume la réglementation pour t'aider au quotidien. Il ne remplace pas le texte officiel : en cas de doute, consulte l'arrêté sur Légifrance ou la préfecture de ton département.</p>
</div>

<h2>Le faire en 30 secondes avec VTC Rentable</h2>
<p>Dans l'onglet <strong>Réservations</strong> de l'appli, tu notes le client, son téléphone, l'heure et le lieu de prise en charge. L'appli enregistre toute seule l'heure de la commande, qui ne peut plus être modifiée ensuite, et reprend les informations de l'exploitant que tu as remplies une fois dans tes réglages.</p>
<p>Elle produit un bon de commande en PDF, directement sur le téléphone et même sans réseau, que tu peux montrer ou envoyer au client. Elle refuse de le créer tant qu'une mention de l'exploitant manque.</p>
""",
  faq=[("Quelles sont les mentions obligatoires du bon de commande VTC ?","Depuis l'arrêté du 6 août 2025 : le nom et les coordonnées de l'exploitant, son numéro au registre des VTC, son numéro SIREN, le nom et le téléphone du client, la date et l'heure de la réservation, la date et l'heure de prise en charge, et le lieu de prise en charge."),
       ("Le bon de commande VTC peut-il être sur le téléphone ?","Oui, le justificatif peut être papier ou électronique. Il doit pouvoir être présenté immédiatement lors d'un contrôle, y compris sans réseau.")],
  sources=[("Arrêté du 6 août 2025 relatif au justificatif de la réservation préalable (Légifrance)","https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000052153206"),
           ("VTC : un nouvel arrêté modifie les règles de justification des réservations (L'Officiel des métiers)","https://www.lofficieldesmetiers.fr/vtc-un-nouvel-arrete-modifie-les-regles-relatives-a-la-justification-des-reservations/"),
           ("Bon de réservation VTC : les mentions obligatoires (Dhraagi Conseil)","https://dhraagiconseil.fr/bon-de-reservation-vtc-les-mentions-obligatoires-et-les-autres/"),
           ("Justificatif de réservation VTC (Examen Quiz VTC)","https://www.examen-quiz-vtc.fr/blog/justificatif-reservation-vtc")]),

 dict(slug="charges-chauffeur-vtc-auto-entrepreneur", short="Charges auto-entrepreneur VTC",
  title="Charges d'un chauffeur VTC auto-entrepreneur en 2026",
  desc="URSSAF 21,2 %, ACRE, versement libératoire, plafond de 83 600 € : les charges d'un chauffeur VTC auto-entrepreneur en 2026, avec un exemple chiffré.",
  h1="Les charges d'un chauffeur VTC auto-entrepreneur en 2026",
  lede="Cotisations URSSAF, formation, ACRE, impôt et frais de la voiture : ce que tu paies vraiment sur ton chiffre d'affaires, avec les taux de 2026.",
  card="URSSAF, ACRE, versement libératoire, plafond : les taux 2026 et un exemple sur une semaine.",
  body="""
<p>En micro-entreprise, tes charges sociales se calculent sur ton <strong>chiffre d'affaires</strong>, pas sur ton bénéfice. Que ta semaine ait coûté cher en carburant ou non, l'URSSAF prend le même pourcentage. C'est pour ça qu'il faut garder un œil sur les deux à la fois.</p>

<h2>Les cotisations URSSAF : 21,2 % du CA</h2>
<p>Le transport de personnes en VTC relève des prestations de services commerciales (BIC). En 2026, le taux de cotisations sociales est de <strong>21,2 % du chiffre d'affaires</strong> encaissé. Tu le déclares chaque mois ou chaque trimestre sur ton espace URSSAF.</p>
<p>Le CA à déclarer, c'est ce que tu encaisses : les montants versés par les plateformes, tes courses privées, le cash et les pourboires.</p>

<h3>La contribution à la formation professionnelle</h3>
<p>Elle s'ajoute aux cotisations et se paie en même temps. Son taux dépend de ton activité : il est faible, de l'ordre de 0,1 % du CA pour une activité commerciale. Le taux exact figure sur ton espace URSSAF.</p>

<h2>L'ACRE : moins de cotisations au démarrage</h2>
<p>L'ACRE réduit tes cotisations sociales pendant environ un an : le trimestre où tu te lances, plus les trois trimestres suivants.</p>
<ul>
  <li><strong>Activité créée avant le 1er juillet 2026 :</strong> réduction de 50 %, que tu gardes jusqu'à la fin de ta période d'ACRE.</li>
  <li><strong>Activité créée depuis le 1er juillet 2026 :</strong> réduction de 25 %. Tu paies donc 75 % du taux normal.</li>
</ul>
<p>L'ACRE ne baisse que les cotisations sociales, pas l'impôt ni la formation professionnelle. La demande se fait dans les 60 jours qui suivent la création.</p>

<h2>L'impôt sur le revenu</h2>
<p>Tu as deux possibilités :</p>
<ul>
  <li><strong>Le versement libératoire :</strong> tu paies 1,7 % de ton CA en même temps que tes cotisations, et l'impôt sur ces revenus est réglé. Il faut le demander, et ton revenu fiscal de référence ne doit pas dépasser un plafond.</li>
  <li><strong>Sans versement libératoire :</strong> ton CA est déclaré une fois par an avec tes autres revenus, après un abattement de 50 %. Le montant dépend alors de toute ta situation fiscale.</li>
</ul>

<h2>Le plafond et la TVA</h2>
<p>Pour rester en micro-entreprise, ton chiffre d'affaires annuel ne doit pas dépasser <strong>83 600 € hors taxes</strong> pour les prestations de services. Ce plafond vaut pour 2026, 2027 et 2028.</p>
<p>La franchise de TVA est un seuil différent : <strong>37 500 €</strong> pour les services en 2026. Au-dessus, tu dois facturer et reverser la TVA, même en restant micro-entrepreneur.</p>

<h2>Les frais de l'activité</h2>
<p>En micro-entreprise, tu ne déduis pas tes frais de ton chiffre d'affaires pour calculer tes cotisations. Ils pèsent pourtant lourd sur ce qu'il te reste :</p>
<ul>
  <li>le carburant ou la recharge, souvent le premier poste ;</li>
  <li>l'assurance VTC, en général payée au mois ;</li>
  <li>la voiture elle-même : crédit, location, ou perte de valeur si tu l'as achetée ;</li>
  <li>l'entretien, les pneus, la visite technique, le lavage ;</li>
  <li>le téléphone, les péages, le parking, les amendes ;</li>
  <li>la cotisation foncière des entreprises (CFE), due à partir de ta deuxième année.</li>
</ul>

<h2>Exemple sur une semaine</h2>
<p>Un chauffeur auto-entrepreneur, sans ACRE ni versement libératoire, encaisse 1 150 € dans la semaine.</p>
<div class="tbl"><table>
  <thead><tr><th>Poste</th><th class="n">Montant</th></tr></thead>
  <tbody>
    <tr><td>Chiffre d'affaires (plateformes, privées, pourboires)</td><td class="n">1 150 €</td></tr>
    <tr><td>Cotisations URSSAF et formation (21,3 %)</td><td class="n minus">− 245 €</td></tr>
    <tr><td>Carburant</td><td class="n minus">− 210 €</td></tr>
    <tr><td>Repas et cafés</td><td class="n minus">− 45 €</td></tr>
    <tr><td>Assurance (160 € par mois, ramenés à la semaine)</td><td class="n minus">− 37 €</td></tr>
    <tr><td>Péage, parking, lavage</td><td class="n minus">− 36 €</td></tr>
    <tr class="tot"><td>Il reste avant impôt</td><td class="n">577 €</td></tr>
  </tbody>
</table></div>
<p>Sur 1 150 € encaissés, il reste donc environ la moitié, et ce n'est pas encore le net final : l'impôt sur le revenu et la perte de valeur de la voiture viennent ensuite.</p>
<div class="box warn">
  <p>Les taux de cet article sont ceux connus en novembre 2026. Ils changent régulièrement : vérifie toujours sur ton espace URSSAF ou avec ton comptable avant de prendre une décision.</p>
</div>

<h2>Suivre tout ça sans tableur</h2>
<p>Dans VTC Rentable, tu choisis le statut <strong>Auto-entrepreneur</strong>, puis ton taux, ton ACRE et le versement libératoire si tu l'as. Chaque semaine, l'appli calcule les cotisations sur ton CA réel et les retire de ton revenu net, avec l'assurance et tes autres charges.</p>
""",
  faq=[("Quel est le taux de cotisations d'un chauffeur VTC auto-entrepreneur en 2026 ?","21,2 % du chiffre d'affaires pour les prestations de services commerciales (BIC), auxquels s'ajoute la contribution à la formation professionnelle. Avec le versement libératoire, il faut ajouter 1,7 % pour l'impôt sur le revenu."),
       ("Quel est le plafond de chiffre d'affaires d'un VTC en micro-entreprise ?","83 600 € hors taxes par an pour les prestations de services, en 2026, 2027 et 2028. La franchise de TVA est un seuil distinct de 37 500 € en 2026.")],
  sources=[("Taux de cotisations micro-entrepreneur 2026 (Accounts OS)","https://accounts-os.com/fr/questions/what-are-the-micro-entrepreneur-contribution-rates-in-2026"),
           ("ACRE 2026 : une exonération de cotisations fortement réduite (Portail Auto-Entrepreneur)","https://www.portail-autoentrepreneur.fr/actualites/acre-2026"),
           ("Nouveaux seuils de la micro-entreprise 2026 (L-Expert-Comptable)","https://www.l-expert-comptable.com/a/nouveaux-seuils-micro-entreprise-2026.html"),
           ("Taux du versement libératoire 2026 (Wisestart)","https://wisestart.fr/guides/fiscalite/taux-versement-liberatoire-2026/")]),

 dict(slug="calcul-revenu-net-vtc", short="Calcul du revenu net VTC",
  title="Comment calculer son revenu net de chauffeur VTC",
  desc="Calculer son revenu net de chauffeur VTC : chiffre d'affaires, charges de la semaine, € / heure et € / km. La méthode pas à pas, avec un exemple chiffré.",
  h1="Comment calculer son revenu net de chauffeur VTC",
  lede="Le montant que t'affiche Uber ou Bolt n'est pas ce que tu gagnes. Voici la méthode pour connaître ton vrai net, ton € / heure et ton € / km.",
  card="La méthode pas à pas pour passer du chiffre d'affaires au vrai revenu net, avec € / heure et € / km.",
  body="""
<p>Les applications des plateformes affichent ce qu'elles te versent. C'est ton chiffre d'affaires, pas ton revenu. Entre les deux, il y a le carburant, l'assurance, la voiture, les charges de ton statut, et toutes les petites dépenses de la journée.</p>

<h2>Étape 1 : additionne tout ce que tu encaisses</h2>
<p>Ton chiffre d'affaires de la semaine, c'est la somme de :</p>
<ul>
  <li>ce que chaque plateforme te verse (Uber, Bolt, Heetch, FreeNow…) ;</li>
  <li>tes courses privées, payées en direct ;</li>
  <li>le cash encaissé et les pourboires.</li>
</ul>
<p>Prends les montants réellement versés, après la commission de la plateforme. C'est ce qui arrive sur ton compte qui compte.</p>

<h2>Étape 2 : retire les frais de la semaine</h2>
<p>Ce sont les dépenses liées à ton activité, au moment où tu les paies : carburant, repas sur la route, péage, parking, lavage, amendes.</p>

<h2>Étape 3 : ramène les charges mensuelles à la semaine</h2>
<p>C'est l'étape que beaucoup de chauffeurs oublient. L'assurance, la location de la voiture, le téléphone ou le comptable se paient une fois par mois, mais ils coûtent aussi les semaines où tu ne les paies pas.</p>
<p>Pour les répartir, multiplie le montant mensuel par 12 et divise par 52. Une assurance à 160 € par mois coûte ainsi <strong>36,92 € par semaine</strong>.</p>

<h2>Étape 4 : retire les charges de ton statut</h2>
<ul>
  <li><strong>Société (SASU, EURL…) :</strong> mets de côté une part de ton CA pour l'impôt et les charges, souvent autour de 25 %. Fixe ce pourcentage avec ton comptable.</li>
  <li><strong>Auto-entrepreneur :</strong> les cotisations URSSAF, 21,2 % du CA en 2026, plus la formation professionnelle et le versement libératoire si tu l'as choisi.</li>
  <li><strong>Salarié en rattachement :</strong> la commission de ta société de rattachement, souvent un montant fixe par semaine.</li>
</ul>

<h2>Étape 5 : n'oublie pas la voiture</h2>
<p>Si tu as acheté ta voiture, elle perd de la valeur chaque mois. Une façon simple de le compter : (prix d'achat − prix de revente prévu) ÷ nombre de mois d'utilisation. Une voiture achetée 15 000 €, revendue 4 000 € au bout de 3 ans, coûte environ 305 € par mois, soit 70 € par semaine. Ajoute l'entretien et les pneus.</p>

<h2>Exemple complet</h2>
<p>Un auto-entrepreneur a travaillé 48 heures et roulé 1 340 km dans la semaine.</p>
<div class="tbl"><table>
  <thead><tr><th>Poste</th><th class="n">Montant</th></tr></thead>
  <tbody>
    <tr><td>Chiffre d'affaires</td><td class="n">1 150 €</td></tr>
    <tr><td>Carburant</td><td class="n minus">− 210 €</td></tr>
    <tr><td>Repas et cafés</td><td class="n minus">− 45 €</td></tr>
    <tr><td>Péage, parking, lavage</td><td class="n minus">− 36 €</td></tr>
    <tr><td>Assurance ramenée à la semaine</td><td class="n minus">− 37 €</td></tr>
    <tr><td>Cotisations URSSAF et formation</td><td class="n minus">− 245 €</td></tr>
    <tr class="tot"><td>Revenu net de la semaine</td><td class="n">577 €</td></tr>
  </tbody>
</table></div>

<h2>€ / heure et € / km : les deux chiffres à suivre</h2>
<p><strong>Le € / heure</strong> te dit si tes journées valent le coup. Dans l'exemple, 577 € pour 48 heures donnent 12 € de l'heure net. Sur le brut, 1 150 € pour 48 heures, c'est 24 € de l'heure : l'écart montre tout ce que coûte l'activité.</p>
<p><strong>Le € / km</strong> te dit si tu roules pour rien. 1 150 € pour 1 340 km, c'est 0,86 € par km en brut. Compare-le d'une semaine à l'autre, et entre plateformes : une course qui paie bien mais fait revenir à vide de loin fait chuter ce chiffre.</p>
<div class="box">
  <p><strong>Astuce :</strong> regarde ces chiffres par jour de la semaine et par créneau. Beaucoup de chauffeurs découvrent qu'une partie de leurs heures rapporte moins que le reste et réorganisent leur planning en conséquence.</p>
</div>

<h2>Le faire automatiquement</h2>
<p>VTC Rentable fait ces cinq étapes pour toi. Tu notes ta journée le soir (recettes par plateforme, carburant, heures, km), et l'appli ajoute chaque semaine l'assurance répartie, les charges de ton statut et tes charges fixes. Tu vois ton net de la semaine et du mois, ton € / heure, ton € / km et le coût de ta voiture.</p>
""",
  faq=[("Comment calculer son revenu net de chauffeur VTC ?","Additionne tout ce que tu encaisses (plateformes, courses privées, cash, pourboires), puis retire tes frais de la semaine, tes charges mensuelles ramenées à la semaine (× 12 ÷ 52), les charges de ton statut et le coût de la voiture."),
       ("Comment calculer son € / heure en VTC ?","Divise ce que tu as encaissé par le nombre d'heures travaillées pour le brut, ou ton revenu net par ces mêmes heures pour le net. Exemple : 577 € nets pour 48 heures donnent 12 € de l'heure.")],
  sources=[("Chiffrage de la rentabilité VTC (Keobiz)","https://www.keobiz.fr/fiches-pratiques/creer-activite-vtc/chiffrage-rentabilite-vtc/"),
           ("Coût kilométrique d'un VTC (Keobiz)","https://www.keobiz.fr/fiches-pratiques/creer-activite-vtc/cout-kilometre-vtc/"),
           ("Taux de cotisations micro-entrepreneur 2026 (Accounts OS)","https://accounts-os.com/fr/questions/what-are-the-micro-entrepreneur-contribution-rates-in-2026")]),
]

def e(s): return html.escape(s, quote=True)

def head(title, desc, url, extra_ld):
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
<meta property="og:type" content="article">
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
<link rel="stylesheet" href="/assets/article.css">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
</head>
<body>
<nav class="top" aria-label="Navigation principale">
  <div class="wrap">
    <a class="logo" href="/"><img src="/icon-192.png" alt="" width="30" height="30">VTC <span>Rentable</span></a>
    <ul>
      <li><a href="/">L'appli</a></li>
      <li><a href="/articles/" aria-current="page">Articles</a></li>
      <li><a href="/#faq">Questions</a></li>
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
      <a href="/articles/">Articles</a>
      <a href="{APP}">Ouvrir l'appli</a>
      <a href="https://app.vtcrentable.com/mentions-legales.html">Mentions légales</a>
      <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a>
    </nav>
  </div>
</footer>
</body>
</html>
'''

def cards(exclude=None):
    return "\n".join(f'<a class="card" href="/articles/{a["slug"]}/"><b>{e(a["h1"])}</b><span>{e(a["card"])}</span></a>' for a in ARTS if a["slug"] != exclude)

ORG = {"@type": "Organization", "name": "VTC Rentable", "url": SITE + "/", "logo": SITE + "/icon-192.png"}
for a in ARTS:
    url = f"{SITE}/articles/{a['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": a["h1"], "description": a["desc"], "datePublished": DATE, "dateModified": DATE,
         "inLanguage": "fr-FR", "mainEntityOfPage": url, "image": "https://app.vtcrentable.com/og-image.png", "author": ORG, "publisher": ORG},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Articles", "item": SITE + "/articles/"},
            {"@type": "ListItem", "position": 3, "name": a["short"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faq"]]}]}
    faqhtml = "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(r)}</p>" for q, r in a["faq"])
    src = "\n".join(f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in a["sources"])
    page = head(a["title"], a["desc"], url, ld) + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li><a href="/articles/">Articles</a></li><li>{e(a["short"])}</li></ol>
    <h1>{e(a["h1"])}</h1>
    <p class="lede">{e(a["lede"])}</p>
    <p class="meta">Mis à jour le {DATE_FR}</p>
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
{cards(a["slug"])}
  </div>
</section>
</main>
''' + FOOT
    os.makedirs(f"{ROOT}/articles/{a['slug']}", exist_ok=True)
    open(f"{ROOT}/articles/{a['slug']}/index.html", "w", encoding="utf-8").write(page)

# index des articles
url = SITE + "/articles/"
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "Articles pour chauffeurs VTC", "url": url, "inLanguage": "fr-FR",
     "hasPart": [{"@type": "Article", "headline": a["h1"], "url": f"{SITE}/articles/{a['slug']}/"} for a in ARTS]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Articles", "item": url}]}]}
page = head("Articles pour chauffeurs VTC | VTC Rentable", "Bon de commande VTC, charges d'un auto-entrepreneur, calcul du revenu net : des guides pratiques pour les chauffeurs VTC en France.", url, ld) + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li>Articles</li></ol>
    <h1>Articles pour chauffeurs VTC</h1>
    <p class="lede">Des réponses claires aux questions qu'on se pose en roulant : réglementation, charges, et comment savoir ce qu'on gagne vraiment.</p>
  </div>
</header>
<main>
<section class="more read" style="padding-top:36px" aria-label="Tous les articles">
  <div class="cards">
{cards()}
  </div>
</section>
</main>
''' + FOOT
os.makedirs(f"{ROOT}/articles", exist_ok=True)
open(f"{ROOT}/articles/index.html", "w", encoding="utf-8").write(page)

# sitemap
urls = [(SITE + "/", "1.0"), (SITE + "/articles/", "0.7")] + [(f"{SITE}/articles/{a['slug']}/", "0.8") for a in ARTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
open(f"{ROOT}/sitemap.xml", "w").write(sm)
print("ok", [len(a["title"]) for a in ARTS], [len(a["desc"]) for a in ARTS])
