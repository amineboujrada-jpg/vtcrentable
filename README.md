# VTC Rentable

Site vitrine de l'appli VTC Rentable : https://vtcrentable.com

Les pages du blog, des calculateurs, des modèles et `sitemap.xml` sont générées par `outils/articles.py`.
Après toute modification, lancer `python3 outils/articles.py` puis publier le résultat.
Styles communs : `assets/article.css` (blog) et `assets/calc.css` (calculateurs).

## Ajouter un article au blog

1. Créer `content/blog/<slug>.html` (le slug devient l'adresse : `vtcrentable.com/blog/<slug>/`).
2. En haut du fichier, une ligne par information, puis une ligne `---`, puis le corps de l'article en HTML :

```
slug: mon-article
date: 2026-11-20
categorie: Rentabilité
title: Titre pour Google (65 caractères maximum)
desc: Description pour Google (entre 70 et 160 caractères)
h1: Titre affiché sur la page
short: Titre court (fil d'Ariane)
lede: Chapeau sous le titre
card: Résumé affiché sur les cartes
faq: Une question ? || Sa réponse.
source: Nom de la source || https://adresse-de-la-source
---
<p>Premier paragraphe…</p>
<h2>Un intertitre</h2>
```

`faq:` et `source:` peuvent être répétées. Les catégories utilisées aujourd'hui : Réglementation, Statut et charges, Rentabilité, Démarrer.
Mettre dans chaque article des liens vers les calculateurs (`/calculateurs/...`), les autres articles (`/blog/...`) et les rubriques de l'accueil (`/#fonctions`, `/#statut`, `/#prix`).

3. Lancer `python3 outils/articles.py` : la page, la liste du blog, les « À lire aussi » et le sitemap se mettent à jour.

Les anciennes adresses `/articles/...` redirigent vers `/blog/...`.

## Examen blanc VTC (quiz + comptes)

- Page `/examen-blanc-vtc/` générée par `outils/page_examen_blanc.py`. Quiz gratuit : `content/examen-blanc/questions.json` (publiques, copiées dans `assets/examen-blanc-data.js`).
- Espace avec compte (e-mail + mot de passe, confirmation par e-mail) : `assets/examen-compte.js`, authentification Supabase du projet `vtc-pro`. Les questions réservées (`content/examen-blanc/premium.json`) sont dans la table `exam_questions`, lisible seulement par les comptes examen confirmés. Pour en ajouter : insérer dans `exam_questions` (même format que `premium.json`) ; les doublons (épreuve + énoncé) sont ignorés.
- Tables : `exam_profiles`, `exam_questions`, `exam_attempts`, `exam_answers` (règles RLS : chacun ne voit que ses propres résultats). Les inscrits se listent avec `select * from admin_exam_users()` (admin).

### Ajouter des questions ou des examens blancs (sans toucher au code du site)

L'espace charge tout depuis Supabase (projet `vtc-pro`), par pages de 1000 : la banque peut grandir librement.

- **Nouvelles questions** : `insert into exam_questions (e, q, texte, o, a, why) values (...)` — `e` = épreuve (A à G), `o` = tableau JSON des choix, `a` = index de la bonne réponse (à partir de 0), `why` = explication. Les doublons (épreuve + énoncé) sont ignorés. Elles apparaissent aussitôt dans l'entraînement, l'examen aléatoire et « Revoir mes erreurs ».
- **Nouvel examen blanc numéroté** : `insert into exam_sets (titre, description, duree_minutes, ordre)`, puis une ligne par question dans `exam_set_questions (set_id, question_id, position)`. Il s'affiche en carte « Examens blancs » avec la meilleure moyenne de l'élève ; chaque essai enregistre `exam_attempts.set_id`. L'examen n°1 contient 42 questions (6 par épreuve, 45 min).
- **Date d'examen** : champ facultatif à l'inscription (`exam_profiles.date_examen`), modifiable par l'élève dans son espace (compte à rebours) et visible dans l'admin (colonne + filtre « moins de 30 jours »).

## Sites vitrines des chauffeurs (`<adresse>.vtcrentable.fr`)

- Les chauffeurs créent leur site dans l'appli (Réglages › Site vitrine). Les données sont dans la table `sites` du projet Supabase `vtc-pro` (`supabase/sites.sql` du dépôt `vtc-pro`).
- Les pages sont servies par un programme Cloudflare (Worker) : `cloudflare/sites-chauffeurs.js`. Il reçoit toutes les adresses `*.vtcrentable.fr`, lit le site en ligne dans Supabase et renvoie la page complète (titre, description, données structurées, réservation). `apercu.vtcrentable.fr` affiche l'aperçu envoyé par l'appli ; `vtcrentable.fr` renvoie vers `/site-vitrine-chauffeur-vtc/`.
- Publication automatique : le Worker `sites-chauffeurs` du compte Cloudflare est relié à ce dépôt (dossier `cloudflare/`, réglages dans `cloudflare/wrangler.jsonc`). Chaque fusion sur `main` publie la nouvelle version. Le domaine a un enregistrement DNS `*` (AAAA `100::`, proxy activé) pour que toutes les adresses arrivent au programme.
- Les 3 modèles (Nuit, Clair, Prestige) sont en haut du fichier (`MODELES`) : couleurs et caractères seulement, les rubriques sont communes.
- Version anglaise : chaque site existe aussi sur `/en/`. Un visiteur dont le navigateur n'est pas en français est envoyé sur `/en/` ; un navigateur en français (et Google) reste sur `/`. Le bouton de langue (globe, en haut de page) change de version et retient le choix un an. Les textes fixes sont écrits dans les deux langues (`TEXTES`) ; les textes du chauffeur sont traduits automatiquement par Workers AI (liaison `AI` de `wrangler.jsonc`, modèle `m2m100`), chaque phrase étant gardée 30 jours. Les champs `accroche_en` et `presentation_en`, remplis dans l'appli, remplacent la traduction automatique. Si la traduction ne répond pas, le texte français du chauffeur est affiché.
