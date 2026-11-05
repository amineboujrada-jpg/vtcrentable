# Pages stratégiques et « Qui sommes-nous » — inclus par articles.py (exec), utilise head(), FOOT, ORG, SITE, APP, e(), cards(), calc_cards()
def fig(name, cap, alt):
    return f'<figure><img src="/assets/captures/{name}.webp" width="780" height="1688" loading="lazy" alt="{e(alt)}"><figcaption>{e(cap)}</figcaption></figure>'
NOTE_DEMO = '<p class="figs-note">Captures de l\'appli réalisées avec des données de démonstration.</p>'
CTA = f'''<div class="cta">
  <strong>Essaie VTC Rentable, c'est gratuit.</strong>
  <p>Note ta journée en une minute et vois ton revenu net, ton € / heure et ton € / km.</p>
  <a class="btn" href="{APP}">Créer mon compte gratuit</a>
</div>'''
SUPPORT = '<p>Une question ? Écris à <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a> : réponse sous 24 h.</p>'
TEMOIGNAGES = '''<blockquote class="quote-l"><p>« VTC Rentable a changé ma façon de voir mon activité. Je sais enfin ce que je gagne vraiment, et je gère mon activité beaucoup plus clairement. »</p><cite>Mohamed Amine, chauffeur VTC et fondateur de VTC Rentable</cite></blockquote>
<blockquote class="quote-l"><p>« C'est efficace : je vois ma rentabilité et j'ai enfin la main dessus. »</p><cite>Jawad, chauffeur VTC, utilisateur de l'appli</cite></blockquote>'''
LANDING = []

def write_landing(slug, title, desc, h1, short, lede, body, faq, kind="WebPage", js=None, css=""):
    assert len(title) <= 65, (slug, len(title)); assert 70 <= len(desc) <= 160, (slug, len(desc))
    url = f"{SITE}/{slug}/"
    graph = [{"@type": kind, "name": h1, "url": url, "description": desc, "inLanguage": "fr-FR", "publisher": ORG},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": short, "item": url}]}]
    if kind == "SoftwareApplication":
        graph[0].update({"applicationCategory": "BusinessApplication", "operatingSystem": "iPhone, Android, navigateur web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}})
    if kind == "WebApplication":
        graph[0].update({"applicationCategory": "FinanceApplication", "operatingSystem": "Navigateur web", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}})
    if kind == "AboutPage":
        graph[0]["mainEntity"] = AUTEUR
    if faq: graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]})
    faqhtml = ("<h2>Questions fréquentes</h2>\n" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(r)}</p>" for q, r in faq)) if faq else ""
    page = head(title, desc, url, {"@context": "https://schema.org", "@graph": graph}, cur=slug, og="website", css=css) + f'''
<header class="head">
  <div class="read">
    <ol class="crumbs"><li><a href="/">Accueil</a></li><li>{e(short)}</li></ol>
    <h1>{e(h1)}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
<main>
<article class="read">
{body}
{faqhtml}
</article>
<section class="more read" aria-labelledby="more-t">
  <h2 id="more-t">Pour aller plus loin</h2>
  <div class="cards">
{cards(None, None).split(chr(10))[0]}
<a class="card" href="/calculateurs/"><b>Calculateurs gratuits</b><span>Revenu net, prix minimum d'une course, coût de la voiture, statuts : en quelques secondes.</span></a>
<a class="card" href="/blog/"><b>Le blog des chauffeurs VTC</b><span>Réglementation, charges, statut et rentabilité, expliqués simplement.</span></a>
  </div>
</section>
</main>
''' + (f'<script src="/assets/{js}" defer></script>\n' if js else "") + FOOT
    os.makedirs(f"{ROOT}/{slug}", exist_ok=True)
    open(f"{ROOT}/{slug}/index.html", "w", encoding="utf-8").write(page)
    LANDING.append(slug)

# ---------- /application-vtc ----------
write_landing("application-vtc",
  "Application VTC gratuite : revenu net et bon de commande",
  "VTC Rentable, l'application des chauffeurs VTC : revenu net de la semaine, € / heure, € / km, dépenses, bon de commande PDF et entretien. Gratuite.",
  "L'application VTC pour savoir ce que tu gagnes vraiment", "Application VTC",
  "Tu notes ta journée le soir, l'appli calcule ton revenu net, ton € / heure et ton € / km, retire tes charges et prépare tes bons de commande.",
  f'''<p><strong>VTC Rentable est une application gratuite pour chauffeurs VTC en France.</strong> Elle répond à une seule question : combien te reste-t-il, une fois le carburant, l'assurance, le rattachement ou l'URSSAF payés ? Les plateformes affichent ton chiffre d'affaires. L'appli affiche ce que tu gagnes.</p>
<div class="figs">
{fig("jour", "Ta journée : recettes par plateforme, carburant, heures, km.", "Onglet Jour de l'application VTC Rentable")}
{fig("semaine", "Le détail de la semaine : net, charges, € / heure, € / km.", "Détail de la semaine dans VTC Rentable")}
{fig("stats", "Tes statistiques sur plusieurs mois.", "Onglet Stats de VTC Rentable")}
</div>
{NOTE_DEMO}
<h2>Ce que fait l'application</h2>
<ul>
  <li><strong>Ta journée en moins d'une minute :</strong> une case par plateforme (Uber, Bolt, Heetch, FreeNow, LeCab, Allocab…), les courses privées et les pourboires, le carburant en montants rapides, les heures et les km au compteur.</li>
  <li><strong>Ton revenu net de la semaine et du mois</strong>, avec les charges de ton statut retirées automatiquement : commission de rattachement, cotisations URSSAF avec ACRE et versement libératoire, ou provision pour une société.</li>
  <li><strong>Ton € / heure et ton € / km</strong>, pour voir quels jours et quelles plateformes valent le coup.</li>
  <li><strong>Tes dépenses rangées</strong> : carburant, entretien, péage, parking, repas, et les charges fixes (assurance, location, téléphone) ajoutées toutes seules chaque semaine. Voir <a href="/gestion-depenses-vtc/">la gestion des dépenses VTC</a>.</li>
  <li><strong>Le bon de commande PDF</strong> pour les courses réservées en direct, avec tes mentions d'exploitant, prêt pour un contrôle, même sans réseau.</li>
  <li><strong>Tes virements vérifiés</strong> : ce que la plateforme t'a versé, comparé à ton chiffre d'affaires moins le cash et la commission.</li>
  <li><strong>Ta voiture suivie</strong> : coût réel par semaine, rappel de la vidange à 1 000 km et de la visite technique 30 jours avant.</li>
</ul>
<h2>Pour quel chauffeur ?</h2>
<p>Pour tous les statuts : salarié d'une société de rattachement, auto-entrepreneur ou société (SASU, EURL). Au premier lancement, l'appli te demande ton statut et tes plateformes, puis fait les calculs qui te correspondent. Elle marche sur iPhone, Android et ordinateur, et continue de fonctionner sans réseau.</p>
<h2>Gratuite, et tes données restent à toi</h2>
<p>L'application est gratuite. Tes chiffres sont stockés en Europe (Irlande), visibles par toi seul, sans publicité ni revente. Tu peux les exporter ou supprimer ton compte quand tu veux. Plus de détails sur la page <a href="/logiciel-vtc-gratuit/">logiciel VTC gratuit</a>.</p>
{CTA}
{SUPPORT}''',
  [("L'application VTC Rentable est-elle vraiment gratuite ?", "Oui. Tu crées ton compte avec ton email et tu utilises toutes les fonctions sans payer."),
   ("Faut-il installer quelque chose ?", "Non. Tu ouvres app.vtcrentable.com sur ton téléphone et tu l'ajoutes à l'écran d'accueil : elle s'utilise comme une application, même sans réseau."),
   ("Est-ce que l'appli se connecte à Uber ou Bolt ?", "Non. Tu notes toi-même ce que chaque plateforme t'a rapporté, ce qui prend moins d'une minute par jour. Tu gardes la main sur tes chiffres.")],
  kind="SoftwareApplication")

# ---------- /calculateur-rentabilite-vtc ----------
form = f'''<form id="rent" class="calc" novalidate>
  <p class="note" style="margin:0 0 14px">Prérempli avec une semaine type : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ta période (semaine ou mois)</legend>
    <div class="row">
      {num_field("ca", "Ce que tu as encaissé (€)", "1150", "Plateformes après commission, courses privées, pourboires")}
      {num_field("h", "Heures travaillées", "48", "Connecté, en attente compris")}
      {num_field("km", "Kilomètres parcourus", "1340", "À vide compris")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Ce que ça t'a coûté</legend>
    <div class="row">
      {num_field("carb", "Carburant ou recharge (€)", "105", "Souvent 8 à 10 % du CA")}
      {num_field("frais", "Autres frais : repas, péage, parking, lavage (€)", "81")}
      {num_field("fixes", "Charges fixes de la période : assurance, rattachement, location (€)", "37")}
      {num_field("statut", "Cotisations ou provision (% du CA)", "21.3", "Auto-entrepreneur : 21,2 % URSSAF + 0,1 % formation = 21,3 % ; 0 si rattaché", "0.1")}
    </div>
  </fieldset>
  <div class="res" aria-live="polite">
    <p class="k">Ta rentabilité</p>
    <p id="r-net" class="big">—</p>
    <p class="sub">de revenu net sur la période</p>
    <div id="r-kpis" class="kpis"></div>
    <p id="r-msg" class="msg"></p>
    <div class="go">
      <p>Ce calcul, VTC Rentable le fait chaque jour pour toi, à partir de ta journée notée en une minute.</p>
      <a class="btn" href="{APP}">Suivre ma rentabilité gratuitement</a>
    </div>
  </div>
  <p class="note" style="margin-top:12px">Résultat indicatif. Tes chiffres restent sur ton appareil : rien n'est envoyé.</p>
</form>'''
write_landing("calculateur-rentabilite-vtc",
  "Calculateur de rentabilité VTC : ton € / heure et ton € / km",
  "Calcule gratuitement ta rentabilité de chauffeur VTC : € / heure et € / km en brut et en net, après carburant, frais, charges fixes et cotisations.",
  "Calculateur de rentabilité VTC par heure et par kilomètre", "Calculateur de rentabilité VTC",
  "Ce que tu gagnes vraiment pour une heure de travail et pour un kilomètre roulé, avant et après tes frais.",
  form + '''
<h2>Comment lire le résultat</h2>
<p><strong>Le € / heure brut</strong> divise ce que tu as encaissé par tes heures. C'est le chiffre que tu compares d'une semaine à l'autre et entre plateformes. <strong>Le € / heure net</strong> fait la même division sur ce qu'il te reste après tes frais et tes charges : c'est ce que ton heure te rapporte vraiment.</p>
<p><strong>Le € / km</strong> montre si tu roules pour rien. Une course bien payée qui te fait revenir à vide de loin fait chuter ce chiffre. Avant d'accepter une course, vérifie-la avec le <a href="/calculateurs/prix-minimum-course-vtc/">calculateur de prix minimum</a>.</p>
<div class="box"><p><strong>Exemple :</strong> 1 150 € encaissés en 48 h et 1 340 km, 105 € de carburant (9 % du CA), 81 € d'autres frais, 37 € d'assurance et 245 € de cotisations (21,2 % URSSAF + 0,1 % formation). Il reste 682 € : 24 € de l'heure en brut, 14 € en net, et 0,51 € net par km.</p></div>
<p>Pour le calcul complet selon ton statut (ACRE, versement libératoire, société, rattachement), utilise le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net VTC</a>.</p>''' + "\n" + CTA,
  [("Comment calculer son € / heure de chauffeur VTC ?", "Divise ce que tu as encaissé par tes heures travaillées pour le brut. Pour le net, retire d'abord ton carburant, tes frais, tes charges fixes et tes cotisations, puis divise par les mêmes heures."),
   ("Quelle part du chiffre d'affaires part dans le carburant ?", "Le plus souvent entre 8 et 10 % du chiffre d'affaires pour une hybride. Note tes pleins pendant quelques semaines pour connaître ta vraie part."),
   ("Faut-il compter les heures d'attente ?", "Oui. Une heure connecté sans course reste une heure de travail : la compter donne un € / heure réaliste.")],
  kind="WebApplication", js="calc-rentabilite.js", css=CSS_CALC)

# ---------- /gestion-depenses-vtc ----------
write_landing("gestion-depenses-vtc",
  "Gestion des dépenses VTC : suivre ses frais et ses charges",
  "Suivre ses dépenses de chauffeur VTC : carburant, entretien, assurance, rattachement, URSSAF. Les frais à noter et comment l'appli les range pour toi.",
  "Gestion des dépenses VTC : suivre ses frais et ses charges", "Gestion des dépenses VTC",
  "Pour connaître ton vrai revenu, il faut voir passer chaque euro dépensé. Voici les frais à suivre, et comment ne plus en oublier.",
  f'''<p><strong>Un chauffeur VTC a deux sortes de dépenses :</strong> celles du quotidien, qui changent chaque jour, et les charges qui reviennent chaque semaine ou chaque mois. Oublier les secondes est la première raison pour laquelle on croit gagner plus que la réalité.</p>
<h2>Les frais du quotidien</h2>
<ul>
  <li><strong>Carburant ou recharge :</strong> souvent 8 à 10 % du chiffre d'affaires. C'est la plus grosse dépense variable.</li>
  <li><strong>Sur la route :</strong> repas et cafés, péages, parking, amendes.</li>
  <li><strong>Voiture :</strong> entretien, pneus, réparations, lavage, visite technique.</li>
  <li><strong>Pro et administratif :</strong> carte VTC et formation, comptable, téléphone et abonnements, frais bancaires.</li>
</ul>
<h2>Les charges qui reviennent</h2>
<ul>
  <li><strong>Selon ton statut :</strong> commission de la société de rattachement chaque semaine, cotisations URSSAF en pourcentage du CA si tu es auto-entrepreneur, ou une part mise de côté pour impôts et charges en société.</li>
  <li><strong>Pour la voiture :</strong> assurance, loyer si tu loues, ou perte de valeur si tu as acheté.</li>
  <li><strong>Charges fixes :</strong> téléphone, comptable, mutuelle… à ramener à la semaine (montant mensuel × 12 ÷ 52).</li>
</ul>
<h2>Comment VTC Rentable s'en occupe</h2>
<div class="figs">
{fig("depenses", "Mes dépenses : les charges de chaque semaine et leur total.", "Page Mes dépenses de VTC Rentable")}
{fig("semaine", "Le carburant comparé à ton CA dans le détail de la semaine.", "Détail de la semaine avec la part du carburant")}
</div>
{NOTE_DEMO}
<ul>
  <li>Le carburant et les repas se notent dans la journée, en montants rapides.</li>
  <li>Les autres dépenses sont rangées en quatre groupes : Voiture, Sur la route, Pro et administratif, Autre. Tu peux ajouter tes propres catégories.</li>
  <li>Le rattachement, l'assurance, la location et tes charges fixes sont <strong>ajoutés automatiquement chaque semaine</strong>, et répartis sur les jours : une semaine à cheval sur deux mois compte au bon prorata dans chaque mois.</li>
  <li>Le résumé montre le total de tes charges fixes par semaine, et le détail de la semaine la part du carburant dans ton chiffre d'affaires.</li>
</ul>
<p>Tu préfères un tableur ? Télécharge le <a href="/modeles/">tableau de suivi et la checklist des frais</a>, gratuits.</p>
{CTA}''',
  [("Quelles dépenses un chauffeur VTC doit-il suivre ?", "Le carburant, les frais de route (repas, péage, parking), la voiture (entretien, pneus, assurance, loyer ou perte de valeur), les frais pro (carte VTC, comptable, téléphone) et les charges de ton statut."),
   ("Comment ramener une charge mensuelle à la semaine ?", "Multiplie le montant mensuel par 12 puis divise par 52. Par exemple, 160 € d'assurance par mois font 36,92 € par semaine."),
   ("Peut-on exporter ses dépenses ?", "Oui. L'appli peut copier tes données dans ton propre Google Sheets et tu peux les sauvegarder dans un fichier.")])

# ---------- /rentabilite-uber-bolt ----------
write_landing("rentabilite-uber-bolt",
  "Rentabilité Uber et Bolt : ce qu'il reste après commissions",
  "Uber et Bolt affichent tes gains, pas ton revenu. Comprends ce qu'il te reste après la commission, le carburant, tes charges et ton statut de VTC.",
  "Rentabilité Uber et Bolt : ce qu'il te reste vraiment", "Rentabilité Uber et Bolt",
  "Le montant affiché dans l'appli Uber ou Bolt n'est pas ce que tu gagnes. Voici comment passer de ce chiffre à ton vrai revenu.",
  f'''<p><strong>Ce que tu vois dans Uber Driver ou Bolt Driver, ce sont tes gains après la commission de la plateforme.</strong> Il reste encore à payer ta voiture, ton carburant, tes frais et les charges de ton statut. C'est seulement après tout ça que tu connais ta rentabilité.</p>
<h2>Les quatre étapes, du prix de la course à ton revenu</h2>
<ol>
  <li><strong>Le prix payé par le client.</strong> La plateforme en garde une part : sa commission, qui varie selon la plateforme et le type de course.</li>
  <li><strong>Tes gains affichés</strong> = ce que la plateforme te verse. C'est le chiffre à noter chaque jour, plateforme par plateforme.</li>
  <li><strong>Tes frais :</strong> carburant (souvent 8 à 10 % de ce que tu encaisses), repas, péage, parking, entretien, et les charges de la voiture (assurance, loyer ou perte de valeur).</li>
  <li><strong>Ton statut :</strong> commission de rattachement par semaine, cotisations URSSAF en pourcentage si tu es auto-entrepreneur, ou provision en société.</li>
</ol>
<div class="box"><p><strong>Exemple sur une semaine :</strong> 1 150 € encaissés sur Uber, Bolt et des courses privées. Moins 105 € de carburant, 81 € de repas, péage et parking, 37 € d'assurance et 245 € de cotisations (21,2 % URSSAF + 0,1 % formation) : il reste 682 €, soit 59 % de ce qui était affiché.</p></div>
<h2>Uber ou Bolt : laquelle te rapporte le plus ?</h2>
<p>La bonne comparaison n'est pas la course la mieux payée, mais <strong>ce qui te reste par heure et par kilomètre</strong> sur chaque plateforme. Une plateforme qui prend moins de commission mais t'envoie loin à vide peut te rapporter moins. Compare la même course sur chaque plateforme avec le <a href="/calculateurs/comparateur-plateformes-vtc/">comparateur des plateformes</a>, et ton € / heure avec le <a href="/calculateur-rentabilite-vtc/">calculateur de rentabilité VTC</a>.</p>
<h2>Le suivre chaque semaine</h2>
<p>Dans VTC Rentable, tu notes chaque soir ce que Uber, Bolt et Heetch t'ont versé. L'appli te montre la part de chaque plateforme, ton net, ton € / heure et ton € / km, et vérifie que les virements reçus correspondent à ton chiffre d'affaires.</p>
<div class="figs">
{fig("semaine", "Par plateforme : la part d'Uber et de Bolt dans ta semaine.", "Détail de la semaine avec la répartition Uber et Bolt")}
{fig("stats", "Sur plusieurs mois : ton net moyen et tes meilleures semaines.", "Statistiques de rentabilité dans VTC Rentable")}
</div>
{NOTE_DEMO}
{CTA}''',
  [("Le montant affiché par Uber est-il mon revenu ?", "Non. C'est ton chiffre d'affaires après la commission d'Uber. Il faut encore retirer ton carburant, tes frais, tes charges de voiture et les charges de ton statut."),
   ("Comment comparer Uber et Bolt ?", "Compare ce qu'il te reste par heure et par kilomètre sur chaque plateforme, pas seulement le prix des courses. Les trajets à vide comptent."),
   ("Où trouver ce que la plateforme m'a versé ?", "Dans le relevé hebdomadaire de l'application chauffeur (gains de la semaine). Note aussi le cash encaissé à part pour vérifier ton virement.")])

# ---------- /logiciel-vtc-gratuit ----------
write_landing("logiciel-vtc-gratuit",
  "Logiciel VTC gratuit : suivre son activité sans payer",
  "Un logiciel VTC gratuit pour suivre ton chiffre d'affaires, tes dépenses, ton revenu net et tes bons de commande, sur téléphone et ordinateur.",
  "Logiciel VTC gratuit pour suivre ton activité", "Logiciel VTC gratuit",
  "Pas besoin de payer un abonnement ni de bricoler un tableur : VTC Rentable fait le suivi de ton activité gratuitement.",
  f'''<p><strong>VTC Rentable est un logiciel de gestion VTC gratuit</strong>, utilisable sur iPhone, Android et ordinateur. Il remplace le tableur que beaucoup de chauffeurs remplissent à la main, avec les calculs déjà faits.</p>
<h2>Ce qui est gratuit</h2>
<ul>
  <li>Le suivi du chiffre d'affaires par plateforme, des heures et des km</li>
  <li>Le revenu net de la semaine et du mois, avec les charges de ton statut</li>
  <li>Le € / heure, le € / km et les statistiques sur plusieurs mois</li>
  <li>Les dépenses et les charges fixes ajoutées chaque semaine</li>
  <li>Les bons de commande PDF pour tes réservations directes</li>
  <li>Le suivi des virements, de l'entretien et de la visite technique</li>
  <li>La synchronisation entre téléphone et ordinateur, et l'export vers Google Sheets</li>
</ul>
<h2>Logiciel gratuit ou tableur ?</h2>
<div class="tbl"><table><thead><tr><th>Ce que tu veux</th><th>Tableur</th><th>VTC Rentable</th></tr></thead><tbody>
<tr><td>Noter ta journée depuis la voiture</td><td>Peu pratique sur téléphone</td><td>Une minute, d'une main</td></tr>
<tr><td>Charges de ton statut</td><td>Formules à écrire toi-même</td><td>Calculées automatiquement</td></tr>
<tr><td>Assurance et rattachement chaque semaine</td><td>À ajouter à la main</td><td>Ajoutés tout seuls</td></tr>
<tr><td>Bon de commande pour un contrôle</td><td>Non</td><td>PDF en un geste, même sans réseau</td></tr>
<tr><td>Rappel entretien et visite technique</td><td>Non</td><td>Oui</td></tr>
</tbody></table></div>
<h2>Gratuit, mais pas au prix de tes données</h2>
<p>Pas de publicité, pas d'outil de suivi, aucune donnée revendue. Tes chiffres sont stockés en Europe et visibles par toi seul. Tu peux les exporter ou supprimer ton compte à tout moment.</p>
<div class="figs">
{fig("jour", "L'écran du jour.", "Écran Jour du logiciel VTC gratuit VTC Rentable")}
{fig("reservation", "Une réservation et son bon de commande.", "Réservation et bon de commande dans VTC Rentable")}
{fig("depenses", "Tes charges de chaque semaine.", "Charges de la semaine dans VTC Rentable")}
</div>
{NOTE_DEMO}
{CTA}
{SUPPORT}''',
  [("Le logiciel est-il vraiment gratuit, sans limite de durée ?", "Oui, toutes les fonctions de l'appli sont gratuites aujourd'hui, sans carte bancaire."),
   ("Comment l'appli est-elle financée ?", "Ni par la publicité ni par la revente de données. Elle est développée par un chauffeur VTC pour les chauffeurs."),
   ("Puis-je l'utiliser sur ordinateur ?", "Oui. Le même compte fonctionne sur le téléphone et sur l'ordinateur, avec tes données synchronisées.")],
  kind="SoftwareApplication")

# ---------- /site-vitrine-chauffeur-vtc : landing de vente, voir outils/page_site_vitrine.py ----------
exec(open(os.path.join(ROOT, "outils", "page_site_vitrine.py"), encoding="utf-8").read())

# ---------- /qui-sommes-nous ----------
write_landing("qui-sommes-nous",
  "Qui sommes-nous ? VTC Rentable, créée par un chauffeur VTC",
  "VTC Rentable est créée par Mohamed Amine, chauffeur VTC en Île-de-France. Notre histoire, nos engagements et comment nous contacter.",
  "Qui sommes-nous ?", "Qui sommes-nous",
  "VTC Rentable est née derrière le volant, d'un chauffeur qui voulait savoir ce qu'il gagnait vraiment.",
  f'''<h2>Le fondateur</h2>
<p><strong>Mohamed Amine, le fondateur, est chauffeur VTC en Île-de-France</strong>, rattaché à une société de transport. Comme beaucoup de chauffeurs, il notait ses journées dans un tableur pour savoir ce qu'il lui restait après le carburant, l'assurance et la commission de rattachement.</p>
<p>Le tableur prenait du temps et les chiffres n'étaient jamais à jour. Développeur de formation, il a donc créé l'outil qu'il cherchait : une appli qui se remplit en une minute le soir, et qui donne enfin le vrai revenu net de la semaine, le € / heure et le € / km.</p>
<p>VTC Rentable est utilisée chaque jour pour son activité. Chaque fonction vient d'un besoin réel du terrain : le bon de commande pour les contrôles, le rappel de la visite technique, la vérification des virements des plateformes.</p>
<h2>Ce qu'en disent les chauffeurs</h2>
{TEMOIGNAGES}
<p>Tu utilises VTC Rentable ? <a href="mailto:contact@vtcrentable.com?subject=Mon%20avis%20sur%20VTC%20Rentable">Envoie-nous ton avis</a>, il pourra apparaître ici avec ton accord.</p>
<h2>Nos engagements</h2>
<div class="engage">
  <div><b>Une appli gratuite</b><span>Toutes les fonctions, sans carte bancaire.</span></div>
  <div><b>Tes données restent à toi</b><span>Stockées en Europe, visibles par toi seul, ni pub ni revente.</span></div>
  <div><b>Un support qui répond</b><span>contact@vtcrentable.com, réponse sous 24 h.</span></div>
  <div><b>Faite par un chauffeur</b><span>Pensée pour être remplie d'une main, en fin de service.</span></div>
</div>
<h2>Nous contacter</h2>
<p>Une question, une idée, un souci ? Écris à <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a>. Tu reçois une réponse sous 24 h, par quelqu'un qui connaît le métier.</p>
<p>Les informations légales sont dans les <a href="{APP}mentions-legales.html">mentions légales</a> et la <a href="{APP}confidentialite.html">politique de confidentialité</a>.</p>
{CTA}''', [], kind="AboutPage")
