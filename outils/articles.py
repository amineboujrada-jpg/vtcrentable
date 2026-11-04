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
<p>Pour une course Uber, Bolt ou Heetch, la plateforme s'en charge dans son application. Le sujet concerne surtout <strong>tes clients en direct</strong> : un habitué qui t'appelle, un hôtel, une réservation par SMS ou WhatsApp. Ces courses ne te coûtent aucune commission : le <a href="/calculateurs/comparateur-plateformes-vtc/">comparateur des plateformes</a> montre ce qu'elles te rapportent de plus.</p>

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
<p>Si tu démarres dans le métier, notre guide pour <a href="/articles/devenir-chauffeur-vtc/">devenir chauffeur VTC</a> reprend toutes les obligations, dans l'ordre.</p>
<div class="box warn">
  <p>Cet article résume la réglementation pour t'aider au quotidien. Il ne remplace pas le texte officiel : en cas de doute, consulte l'arrêté sur Légifrance ou la préfecture de ton département.</p>
</div>

<h2>Le faire en 30 secondes avec VTC Rentable</h2>
<p>Dans l'onglet <strong>Réservations</strong> de l'appli, tu notes le client, son téléphone, l'heure et le lieu de prise en charge. L'appli enregistre toute seule l'heure de la commande, qui ne peut plus être modifiée ensuite, et reprend les informations de l'exploitant que tu as remplies une fois dans tes réglages.</p>
<p>Elle produit un bon de commande en PDF, directement sur le téléphone et même sans réseau, que tu peux montrer ou envoyer au client. Elle refuse de le créer tant qu'une mention de l'exploitant manque.</p>
<p>Le bon de commande n'est qu'une des <a href="/#fonctions">fonctions de l'appli</a> : elle suit aussi tes recettes, tes frais et ton revenu net, et elle est <a href="/#prix">gratuite</a>.</p>
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
<p>Tu hésites encore sur ton statut ? Le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a> met côte à côte auto-entrepreneur, société et rattachement, avec tes chiffres.</p>

<h2>L'impôt sur le revenu</h2>
<p>Tu as deux possibilités :</p>
<ul>
  <li><strong>Le versement libératoire :</strong> tu paies 1,7 % de ton CA en même temps que tes cotisations, et l'impôt sur ces revenus est réglé. Il faut le demander, et ton revenu fiscal de référence ne doit pas dépasser un plafond.</li>
  <li><strong>Sans versement libératoire :</strong> ton CA est déclaré une fois par an avec tes autres revenus, après un abattement de 50 %. Le montant dépend alors de toute ta situation fiscale.</li>
</ul>

<h2>Le plafond et la TVA</h2>
<p>Pour rester en micro-entreprise, ton chiffre d'affaires annuel ne doit pas dépasser <strong>83 600 € hors taxes</strong> pour les prestations de services. Ce plafond vaut pour 2026, 2027 et 2028.</p>
<p>La franchise de TVA est un seuil différent : <strong>37 500 €</strong> pour les services en 2026. Au-dessus, tu dois facturer et reverser la TVA, même en restant micro-entrepreneur. Vérifie où tu en es avec le <a href="/calculateurs/seuil-tva-vtc/">calculateur des seuils de TVA</a>, et vois quel chiffre viser avec l'<a href="/calculateurs/objectif-chiffre-affaires-vtc/">objectif de chiffre d'affaires</a>.</p>

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
<p>Pour ne rien oublier, télécharge la <a href="/modeles/">checklist des frais du chauffeur VTC</a>, et calcule ce que te coûte vraiment ta voiture avec le <a href="/calculateurs/cout-voiture-km-vtc/">calculateur du coût au kilomètre</a>.</p>

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
<p>Pour faire le calcul avec tes propres chiffres, ACRE et versement libératoire compris, utilise le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net VTC</a>.</p>
<div class="box warn">
  <p>Les taux de cet article sont ceux connus en novembre 2026. Ils changent régulièrement : vérifie toujours sur ton espace URSSAF ou avec ton comptable avant de prendre une décision.</p>
</div>

<h2>Suivre tout ça sans tableur</h2>
<p>Dans VTC Rentable, qui gère <a href="/#statut">tous les statuts</a>, tu choisis le statut <strong>Auto-entrepreneur</strong>, puis ton taux, ton ACRE et le versement libératoire si tu l'as. Chaque semaine, l'appli calcule les cotisations sur ton CA réel et les retire de ton revenu net, avec l'assurance et tes autres charges.</p>
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
<div class="box">
  <p><strong>Pressé ?</strong> Le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net VTC</a> fait ces étapes pour toi, gratuitement et sans inscription.</p>
</div>

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
<p>Pour voir lequel te laisse le plus, utilise le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a>.</p>

<h2>Étape 5 : n'oublie pas la voiture</h2>
<p>Si tu as acheté ta voiture, elle perd de la valeur chaque mois. Une façon simple de le compter : (prix d'achat − prix de revente prévu) ÷ nombre de mois d'utilisation. Une voiture achetée 15 000 €, revendue 4 000 € au bout de 3 ans, coûte environ 305 € par mois, soit 70 € par semaine. Ajoute l'entretien et les pneus. Le <a href="/calculateurs/cout-voiture-km-vtc/">calculateur du coût de la voiture</a> fait ce calcul pour toi, location comprise.</p>

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
<p><strong>Le € / km</strong> te dit si tu roules pour rien. 1 150 € pour 1 340 km, c'est 0,86 € par km en brut. Compare-le d'une semaine à l'autre, et entre plateformes : une course qui paie bien mais fait revenir à vide de loin fait chuter ce chiffre. Avant d'accepter, vérifie-la avec le <a href="/calculateurs/prix-minimum-course-vtc/">calculateur du prix minimum d'une course</a>.</p>
<div class="box">
  <p><strong>Astuce :</strong> regarde ces chiffres par jour de la semaine et par créneau. Beaucoup de chauffeurs découvrent qu'une partie de leurs heures rapporte moins que le reste et réorganisent leur planning en conséquence.</p>
</div>

<h2>Le faire automatiquement</h2>
<p>Tu préfères un tableur ? Télécharge notre <a href="/modeles/">tableau de suivi de la semaine</a>, gratuit.</p>
<p>VTC Rentable fait ces cinq étapes pour toi. Tu notes ta journée le soir (recettes par plateforme, carburant, heures, km), et l'appli ajoute chaque semaine l'assurance répartie, les charges de ton statut et tes charges fixes. Tu vois ton net de la semaine et du mois, ton € / heure, ton € / km et le coût de ta voiture. Découvre <a href="/#fonctions">tout ce que fait l'appli</a>.</p>
""",
  faq=[("Comment calculer son revenu net de chauffeur VTC ?","Additionne tout ce que tu encaisses (plateformes, courses privées, cash, pourboires), puis retire tes frais de la semaine, tes charges mensuelles ramenées à la semaine (× 12 ÷ 52), les charges de ton statut et le coût de la voiture."),
       ("Comment calculer son € / heure en VTC ?","Divise ce que tu as encaissé par le nombre d'heures travaillées pour le brut, ou ton revenu net par ces mêmes heures pour le net. Exemple : 577 € nets pour 48 heures donnent 12 € de l'heure.")],
  sources=[("Chiffrage de la rentabilité VTC (Keobiz)","https://www.keobiz.fr/fiches-pratiques/creer-activite-vtc/chiffrage-rentabilite-vtc/"),
           ("Coût kilométrique d'un VTC (Keobiz)","https://www.keobiz.fr/fiches-pratiques/creer-activite-vtc/cout-kilometre-vtc/"),
           ("Taux de cotisations micro-entrepreneur 2026 (Accounts OS)","https://accounts-os.com/fr/questions/what-are-the-micro-entrepreneur-contribution-rates-in-2026")]),
 dict(slug="devenir-chauffeur-vtc", short="Devenir chauffeur VTC",
  title="Devenir chauffeur VTC en 2026 : étapes, examen et budget",
  desc="Devenir chauffeur VTC en 2026 : conditions, examen à la CMA, carte professionnelle, registre VTC, voiture, assurance et budget de départ, étape par étape.",
  h1="Devenir chauffeur VTC en 2026 : le guide étape par étape",
  lede="Conditions, examen, carte professionnelle, entreprise, voiture et budget : tout ce qu'il faut faire, dans l'ordre, pour transporter tes premiers clients.",
  card="Les étapes, l'examen, les papiers et le budget pour démarrer, dans le bon ordre.",
  body="""
<p>Devenir chauffeur VTC prend en général deux à quatre mois. Il faut réussir un examen, obtenir une carte professionnelle, créer une entreprise (ou se rattacher à une société), puis trouver une voiture qui respecte les règles. Voici les étapes dans l'ordre.</p>

<h2>Étape 1 : vérifier que tu remplis les conditions</h2>
<ul>
  <li><strong>Le permis B depuis plus de 3 ans</strong>, en cours de validité.</li>
  <li><strong>Un casier compatible :</strong> certaines condamnations, notamment à au moins 6 mois de prison pour des délits comme le vol ou certaines infractions routières, interdisent le métier.</li>
  <li><strong>L'aptitude médicale :</strong> une visite chez un médecin agréé par la préfecture, à refaire régulièrement (en général tous les 5 ans).</li>
</ul>

<h2>Étape 2 : passer l'examen VTC</h2>
<p>L'examen est organisé par la <strong>chambre de métiers et de l'artisanat (CMA)</strong> de ta région, avec une inscription en ligne. Compte environ <strong>200 €</strong> de frais d'inscription, selon la région.</p>
<ul>
  <li><strong>Une épreuve de connaissances :</strong> réglementation du transport de personnes, gestion, sécurité routière, développement commercial, français et anglais.</li>
  <li><strong>Une épreuve pratique :</strong> une conduite d'une vingtaine de minutes, avec un parcours à préparer et des questions sur la relation client.</li>
</ul>
<p>Tu peux le préparer seul (quelques centaines d'euros de manuels et d'entraînements) ou en centre de formation, entre 1 500 et 3 000 € environ, souvent finançable par le CPF. Il est aussi possible d'être dispensé d'examen si tu justifies d'au moins un an d'expérience de chauffeur professionnel de personnes sur les dix dernières années.</p>

<h2>Étape 3 : demander ta carte professionnelle</h2>
<p>Une fois l'examen réussi, tu demandes ta <strong>carte professionnelle VTC à la préfecture</strong> de ton département (préfecture de police à Paris), avec ton attestation de réussite, ton permis et ton certificat médical. La carte est <strong>gratuite</strong> ; compte quelques semaines de délai. Pendant les courses, elle doit être visible de l'extérieur.</p>

<h2>Étape 4 : choisir ton statut et créer ton entreprise</h2>
<p>Trois possibilités :</p>
<ul>
  <li><strong>Auto-entrepreneur :</strong> la création est gratuite et les démarches sont simples, mais les cotisations portent sur tout le chiffre d'affaires et le CA est plafonné à 83 600 € par an.</li>
  <li><strong>Société (SASU, EURL) :</strong> quelques centaines d'euros de création, un comptable, mais les frais se déduisent.</li>
  <li><strong>Rattachement :</strong> tu travailles sous la licence d'une société, contre un prix chaque semaine, sans avoir à t'inscrire toi-même au registre.</li>
</ul>
<p>Pour comparer avec tes propres chiffres, utilise le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a>.</p>

<h2>Étape 5 : t'inscrire au registre des VTC</h2>
<p>Si tu exploites toi-même (auto-entrepreneur ou société), tu dois inscrire ton entreprise au <strong>registre des exploitants VTC</strong>, en ligne. L'inscription coûte <strong>170 €</strong> et se renouvelle tous les 5 ans. Il faut fournir notamment ton numéro SIREN ou Kbis, ta carte professionnelle, la carte grise de la voiture et une attestation d'assurance responsabilité civile professionnelle.</p>
<p>Tu reçois ensuite les <strong>macarons VTC</strong> à coller à l'avant et à l'arrière de la voiture (de l'ordre de 36 € l'unité).</p>

<h2>Étape 6 : trouver la bonne voiture</h2>
<p>La voiture doit respecter des critères précis :</p>
<ul>
  <li>au moins 4 portes, et de 4 à 9 places chauffeur compris ;</li>
  <li>des dimensions minimales de 4,50 m de long et 1,70 m de large ;</li>
  <li>une puissance d'au moins 84 kW (environ 114 ch) ;</li>
  <li>moins de 6 ans.</li>
</ul>
<p>Les règles d'âge, de taille et de puissance sont assouplies pour les voitures hybrides et électriques : vérifie le détail auprès de ta préfecture avant d'acheter ou de louer. Pense aussi aux zones à faibles émissions (ZFE) de ta ville.</p>
<p>Acheter ou louer ? Fais le calcul avec le <a href="/calculateurs/achat-ou-location-voiture-vtc/">comparateur achat ou location</a>, et estime le coût réel au kilomètre avec le <a href="/calculateurs/cout-voiture-km-vtc/">calculateur du coût de la voiture</a>.</p>

<h2>Étape 7 : t'assurer</h2>
<p>Deux assurances sont indispensables : une <strong>assurance de la voiture pour le transport de personnes à titre onéreux</strong>, et une <strong>responsabilité civile professionnelle</strong>. L'assurance VTC est souvent le poste le plus lourd après la voiture : demande plusieurs devis.</p>

<h2>Le budget de départ</h2>
<div class="tbl"><table>
  <thead><tr><th>Poste</th><th class="n">Ordre de grandeur</th></tr></thead>
  <tbody>
    <tr><td>Examen VTC (inscription)</td><td class="n">≈ 200 €</td></tr>
    <tr><td>Préparation à l'examen</td><td class="n">200 € à 3 000 €</td></tr>
    <tr><td>Visite médicale</td><td class="n">quelques dizaines d'€</td></tr>
    <tr><td>Carte professionnelle</td><td class="n">gratuite</td></tr>
    <tr><td>Création de l'entreprise</td><td class="n">0 € à quelques centaines d'€</td></tr>
    <tr><td>Inscription au registre VTC</td><td class="n">170 €</td></tr>
    <tr><td>Macarons</td><td class="n">≈ 72 €</td></tr>
    <tr><td>Premier mois de location ou apport voiture</td><td class="n">500 € à 1 200 € et plus</td></tr>
  </tbody>
</table></div>
<p>En comptant une préparation en centre et la location d'une voiture, les sources estiment un budget de départ autour de <strong>2 500 à 5 000 €</strong>, hors achat de voiture.</p>

<h2>Après le démarrage</h2>
<ul>
  <li><strong>La formation continue :</strong> un stage d'au moins 7 heures tous les 5 ans, dans un centre agréé, pour garder ta carte.</li>
  <li><strong>Le justificatif de réservation :</strong> chaque course doit être réservée à l'avance et prouvée. Les règles ont changé en 2025 : lis <a href="/articles/bon-de-commande-vtc/">les 7 mentions obligatoires du bon de commande</a>.</li>
  <li><strong>Tes chiffres :</strong> le montant affiché par les plateformes n'est pas ton revenu. Apprends à <a href="/articles/calcul-revenu-net-vtc/">calculer ton revenu net</a> dès les premières semaines, et compare ce que te laisse chaque plateforme avec le <a href="/calculateurs/comparateur-plateformes-vtc/">comparateur des plateformes</a>.</li>
  <li><strong>Tes charges :</strong> lis <a href="/articles/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a> et garde la <a href="/modeles/">checklist des frais</a> sous la main.</li>
</ul>
<div class="box warn">
  <p>Les montants de ce guide sont des ordres de grandeur relevés en novembre 2026 ; certains varient selon la région. Vérifie toujours auprès de ta CMA et de ta préfecture avant de t'engager.</p>
</div>

<h2>Bien démarrer avec VTC Rentable</h2>
<p>Dès ta première semaine, note tes recettes, ton carburant et tes heures dans VTC Rentable, <a href="/#demarrer">prête en cinq minutes</a> : l'appli calcule ton revenu net, ton € / heure et ton € / km, avec les charges de ton statut.</p>
""",
  faq=[("Combien de temps faut-il pour devenir chauffeur VTC ?","En général deux à quatre mois : la préparation et le passage de l'examen à la CMA, la demande de carte professionnelle en préfecture, la création de l'entreprise et l'inscription au registre des VTC."),
       ("Combien coûte le démarrage en VTC ?","Hors achat de voiture, compter environ 2 500 à 5 000 € avec une préparation en centre et la location d'un véhicule : examen (environ 200 €), formation, registre VTC (170 €), macarons, assurance et premier loyer.")],
  sources=[("Devenir chauffeur VTC (Wisestart, mis à jour en octobre 2026)","https://wisestart.fr/guides/juridique/devenir-chauffeur-vtc/"),
           ("Comment devenir chauffeur VTC (Dougs)","https://www.dougs.fr/blog/comment-devenir-chauffeur-vtc/"),
           ("Chauffeur VTC : conditions et démarches (Service Public, fiche F31027)","https://sites.service-information-publique.fr/carnac/guide-professionnels/F31027.html")]),

]

def e(s): return html.escape(s, quote=True)

def head(title, desc, url, extra_ld, cur="articles", og="article", css=""):
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
</head>
<body>
<nav class="top" aria-label="Navigation principale">
  <div class="wrap">
    <a class="logo" href="/"><img src="/icon-192.png" alt="" width="30" height="30">VTC <span>Rentable</span></a>
    <ul>
      <li><a href="/">L'appli</a></li>
      {li("/calculateurs/", "Calculateurs", "calc")}
      {li("/articles/", "Articles", "articles")}
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
      <a href="/calculateurs/">Calculateurs</a>
      <a href="/articles/">Articles</a>
      <a href="/modeles/">Modèles gratuits</a>
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
              card="Uber, Bolt, Heetch, FreeNow : ce qu'il te reste sur une même course selon la commission de chaque plateforme.")]

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
title = "Calculateur revenu net VTC 2026 : gratuit et sans inscription"
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
      {num_field("carburant", "Carburant ou recharge (€)", "210")}
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
<p>Le calculateur suit la méthode détaillée dans notre article <a href="/articles/calcul-revenu-net-vtc/">Comment calculer son revenu net de chauffeur VTC</a> :</p>
<ol>
  <li><strong>Ce que tu encaisses :</strong> le montant versé par les plateformes, plus tes courses privées et tes pourboires. Si tu saisis le prix payé par les clients, la commission est retirée d'abord.</li>
  <li><strong>Les charges de ton statut :</strong> pour un auto-entrepreneur, 21,2 % du CA plus la formation professionnelle, avec l'ACRE et le versement libératoire si tu les as (détails dans <a href="/articles/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>). En société, le pourcentage que tu mets de côté. En rattachement, le prix payé chaque semaine.</li>
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
        "En auto-entrepreneur, environ 21,3 % du CA en 2026 (cotisations et formation), 23 % avec le versement libératoire. En société, le pourcentage que tu mets de côté, souvent autour de 25 %. En rattachement, mets 0 et ajoute le prix du rattachement à tes charges fixes mensuelles."),
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
      {num_field("stat", "Charges de ton statut (% du CA)", "21.3", "Auto-entrepreneur : 21,3 % ; avec versement libératoire : 23 %", step="0.1")}
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
<p>Pour suivre ces chiffres sur toute ta semaine, et pas seulement course par course, utilise le <a href="/calculateurs/revenu-net-vtc/">calculateur de revenu net VTC</a> ou lis <a href="/articles/calcul-revenu-net-vtc/">comment calculer son revenu net</a>.</p>
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
  <li><strong>Auto-entrepreneur :</strong> 21,2 % du CA et la formation professionnelle, réduits par l'ACRE, plus 1,7 % avec le versement libératoire. Détails dans <a href="/articles/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>.</li>
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
        "C'est le point à faire confirmer par ton comptable, car il décide souvent si tu dépasses le seuil. Le calculateur propose par défaut le calcul prudent, sur le prix total payé par les clients, commission comprise.")]
form = f"""
<form id="calc" class="calc" novalidate aria-describedby="calc-intro">
  <p id="calc-intro" class="note" style="margin:0 0 14px">Prérempli avec un exemple : remplace par tes chiffres, le résultat se met à jour tout seul.</p>
  <fieldset>
    <legend>Ton chiffre d'affaires</legend>
    <div class="row">
      {num_field("caan", "Montant versé depuis le 1er janvier (€)", "25000", "Plateformes, courses privées et pourboires")}
      {num_field("mois", "Nombre de mois écoulés", "10", "Mois complets depuis janvier")}
      {num_field("caprec", "Montant versé l'an dernier (€)", "28000", "0 si tu as commencé cette année")}
    </div>
  </fieldset>
  <fieldset>
    <legend>Base du calcul</legend>
    <div class="row">
      <label for="base">Comparer aux seuils
        <select id="base"><option value="client">le prix payé par les clients (prudent)</option><option value="verse">le montant versé par les plateformes</option></select></label>
      <div id="f-com">{num_field("com", "Commission moyenne des plateformes (%)", "25", "Pour retrouver le prix payé par les clients")}</div>
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
<div class="box warn"><p><strong>Le point à vérifier :</strong> selon la façon dont la plateforme facture les courses, le chiffre comparé au seuil peut être le prix total payé par les clients, commission comprise, et non ce qui arrive sur ton compte. L'écart est d'environ un tiers avec 25 % de commission. Fais confirmer la bonne base par ton comptable avant de te fier au résultat. La commission facturée depuis l'étranger peut aussi entraîner une autoliquidation de TVA.</p></div>
<p>Pour voir l'effet sur ce qu'il te reste, utilise le <a href="/calculateurs/comparateur-statut-vtc/">comparateur de statuts</a> et lis <a href="/articles/charges-chauffeur-vtc-auto-entrepreneur/">les charges d'un VTC auto-entrepreneur</a>.</p>
<div class="src"><p><strong>Sources</strong></p><ul>
<li><a href="https://www.superindep.fr/blog/2024/nouveautes-tva-2025/" rel="noopener">Seuils de TVA en microentreprise 2026 (SuperIndep)</a></li>
<li><a href="https://pro.credit-agricole.fr/tva/vtc" rel="noopener">Quelle TVA s'applique aux chauffeurs VTC (Crédit Agricole Pro)</a></li>
<li><a href="https://hayot-expertise.fr/blog/vtc-tva-commission-uber-deduction-vehicule-2026" rel="noopener">VTC : TVA 10 %, commission Uber et déduction du véhicule (Hayot Expertise)</a></li>
</ul></div>"""
write_calc(c, title, desc, "Vas-tu dépasser la franchise de TVA cette année ? À partir de ton chiffre depuis janvier, le calculateur projette ton année et te dit quand la TVA s'appliquera.", faq, form, method, "calc-seuil-tva.js")

# --- comparateur des plateformes ---
c = CALCS[7]
title = "Commission Uber, Bolt, Heetch, FreeNow : comparateur VTC 2026"
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
      {num_field("stat", "Charges de ton statut (% du CA)", "21.3", "Auto-entrepreneur : 21,3 %", step="0.1")}
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
page = head("Modèles gratuits VTC : tableau de suivi et checklist des frais", "Télécharge gratuitement un tableau Excel de suivi de semaine VTC et une checklist des frais à imprimer, pour savoir ce que tu gagnes vraiment.", url, ld, cur="modeles", og="website", css=CSS_CALC) + f"""
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

# sitemap
urls = [(SITE + "/", "1.0"), (SITE + "/calculateurs/", "0.8")] + [(f"{SITE}/calculateurs/{c['slug']}/", "0.9") for c in CALCS] \
     + [(SITE + "/modeles/", "0.6"), (SITE + "/articles/", "0.7")] + [(f"{SITE}/articles/{a['slug']}/", "0.8") for a in ARTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
open(f"{ROOT}/sitemap.xml", "w").write(sm)
print("ok", [len(a["title"]) for a in ARTS], [len(a["desc"]) for a in ARTS])
