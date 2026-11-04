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
