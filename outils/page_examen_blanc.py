# Page /examen-blanc-vtc/ — incluse par articles.py (exec) après pages_landing.py.
# Les questions sont dans content/examen-blanc/questions.json ; ce script en tire assets/examen-blanc-data.js.
import json as _json

_EXA = _json.load(open(os.path.join(ROOT, "content", "examen-blanc", "questions.json"), encoding="utf-8"))
_ids = {x["id"] for x in _EXA["epreuves"]}
for _q in _EXA["questions"]:
    assert _q["e"] in _ids and len(_q["o"]) >= 2 and 0 <= _q["a"] < len(_q["o"]) and _q["why"], _q
assert all(sum(1 for q in _EXA["questions"] if q["e"] == i) >= 5 for i in _ids), "au moins 5 questions par épreuve"
open(os.path.join(ROOT, "assets", "examen-blanc-data.js"), "w", encoding="utf-8").write(
    "/* Généré par outils/articles.py depuis content/examen-blanc/questions.json — ne pas modifier à la main. */\n"
    "window.EXAMEN_BLANC = " + _json.dumps(_EXA, ensure_ascii=False, separators=(",", ":")) + ";\n")

_FORMAT = {"A": "5 QRC + 10 QCM", "B": "2 QRC + 16 QCM", "C": "20 QCM", "D": "3 QRC + 7 QCM", "E": "20 QCM", "F": "4 QRC + 12 QCM", "G": "2 QRC + 6 QCM"}
_lignes = "\n".join(
    f'<tr><td>{x["id"]} · {e(x["nom"])}</td><td class="n">{x["duree"]} min</td><td class="n">{x["coef"]}</td><td class="n">sous {x["seuil"]} / 20</td><td>{_FORMAT[x["id"]]}</td></tr>'
    for x in _EXA["epreuves"])
_nb = len(_EXA["questions"])

write_landing("examen-blanc-vtc",
  "Examen blanc VTC gratuit : QCM et correction en ligne",
  "Examen blanc VTC gratuit : 35 questions sur les 7 épreuves, chrono, correction détaillée et verdict d'admissibilité avec coefficients et notes éliminatoires.",
  "Examen blanc VTC gratuit", "Examen blanc VTC",
  "Entraîne-toi aux 7 épreuves écrites de l'examen VTC : un QCM chronométré, une correction pour chaque question et un verdict calculé comme le jour J.",
  f'''<p><strong>Cet examen blanc VTC est gratuit, sans inscription.</strong> Tu choisis un examen complet (5 questions par épreuve, 35 minutes) ou tu révises une seule épreuve avec la correction après chaque réponse. À la fin, le verdict applique les coefficients, la moyenne de 10 / 20 et les notes éliminatoires de l'examen officiel.</p>
<div id="exam" class="calc" aria-labelledby="exam-t">
  <noscript><p>L'examen blanc a besoin de JavaScript pour fonctionner. Active-le dans ton navigateur puis recharge la page.</p></noscript>
</div>
<script src="/assets/examen-blanc-data.js" defer></script>
<script src="/assets/examen-blanc.js" defer></script>
<p class="note-pg" style="font-size:14.5px;color:var(--muted)">Sans compte, rien n'est enregistré : ton score reste dans ton navigateur. Les questions sont tirées au hasard à chaque essai.</p>

<section id="espace-section" aria-labelledby="espace-t" style="margin-top:34px">
<div id="espace" class="calc"><noscript><p>L'espace d'entraînement a besoin de JavaScript pour fonctionner.</p></noscript></div>
</section>

<h2>Comment se passe l'examen VTC ?</h2>
<p>L'accès à la profession de conducteur de VTC passe par un examen en deux temps : sept épreuves écrites d'admissibilité, puis une épreuve pratique d'admission. Cinq épreuves sont communes aux taxis, aux VTC et aux conducteurs de deux ou trois roues motorisés (A à E). Deux sont propres au VTC (F et G).</p>
<div class="tbl"><table>
<thead><tr><th>Épreuve</th><th class="n">Durée</th><th class="n">Coef.</th><th class="n">Éliminatoire</th><th>Format réel</th></tr></thead>
<tbody>
{_lignes}
</tbody></table></div>
<p>Pour être admissible, il faut cumuler trois conditions : une <strong>moyenne pondérée d'au moins 10 / 20</strong> sur les sept épreuves, <strong>au moins 6 / 20</strong> à chacune des épreuves A, B, C, D, F et G, et <strong>au moins 4 / 20</strong> en anglais. Une seule note éliminatoire suffit à écarter un candidat, même avec une bonne moyenne.</p>

<h2>Ce que cet examen blanc fait, et ce qu'il ne fait pas</h2>
<ul>
  <li><strong>Il reprend la structure de l'examen :</strong> les mêmes sept épreuves, les mêmes coefficients, les mêmes seuils.</li>
  <li><strong>Il ne contient que des QCM.</strong> Le vrai examen ajoute des questions à réponses courtes : pour t'y préparer, entraîne-toi à rédiger une phrase complète qui cite la règle puis l'applique.</li>
  <li><strong>Les questions sont originales.</strong> Ce ne sont pas celles de l'examen officiel et elles ne le garantissent pas. Les règles, elles, sont celles en vigueur à la date de mise à jour.</li>
  <li><strong>Le barème est simplifié :</strong> toutes les questions d'une épreuve pèsent autant, et la note est ramenée sur 20.</li>
</ul>
<p>Après l'écrit, l'épreuve pratique est une mise en situation de course avec une phase de conduite d'au moins 20 minutes. Il faut y obtenir au moins 12 / 20, et tu peux t'y présenter trois fois dans l'année qui suit les résultats de l'admissibilité.</p>

<h2>Après l'examen : démarrer ton activité</h2>
<p>Une fois la carte en poche, il reste à choisir ton statut et à chiffrer ton activité. Commence par notre guide pour <a href="/blog/devenir-chauffeur-vtc/">devenir chauffeur VTC</a>, lis <a href="/blog/carte-professionnelle-vtc/">comment obtenir et renouveler la carte professionnelle</a>, puis compare <a href="/calculateurs/comparateur-statut-vtc/">les statuts</a> et calcule <a href="/calculateurs/revenu-net-vtc/">ton revenu net</a> avec nos calculateurs gratuits. Pour suivre ta rentabilité au quotidien, <a href="{APP}">essaie l'appli VTC Rentable</a>.</p>
<p class="src">Sources : <a href="https://www.cma-alsace-moselle-grandest.fr/sites/default/files/2026-02/Habilitation_acces_profession_conducteur_VTC_V1.4_26012026_AA.pdf" rel="noopener">CMA Alsace-Moselle Grand Est, habilitation d'accès à la profession de conducteur VTC</a> (épreuves et conditions d'admissibilité) ; <a href="https://www.service-public.fr/professionnels-entreprises/vosdroits/F31027" rel="noopener">Service-public.fr, exploitant ou conducteur de VTC</a> (réglementation). Vérifie toujours le règlement d'examen en vigueur auprès de ta chambre de métiers et de l'artisanat.</p>''',
  [("Comment se passe l'examen VTC ?", "L'examen comprend sept épreuves écrites d'admissibilité (QCM et questions à réponses courtes) : réglementation du T3P, gestion, sécurité routière, français, anglais, développement commercial et réglementation nationale du VTC. Il se termine par une épreuve pratique d'admission."),
   ("Quelle note faut-il pour être admissible à l'examen VTC ?", "Il faut une moyenne pondérée d'au moins 10 sur 20 sur les sept épreuves, au moins 6 sur 20 aux épreuves A, B, C, D, F et G, et au moins 4 sur 20 en anglais. Une note éliminatoire écarte le candidat même si la moyenne est bonne."),
   ("Cet examen blanc reproduit-il les vraies questions de l'examen VTC ?", "Non. Les questions sont originales, uniquement à choix multiples, et suivent la structure de l'examen (épreuves, coefficients, seuils). Elles servent à t'entraîner, pas à prédire le sujet du jour J."),
   ("L'examen blanc VTC est-il vraiment gratuit ?", "Oui. L'examen blanc complet est accessible sans inscription. Un compte gratuit (adresse e-mail et mot de passe) débloque en plus toute la banque de questions, des examens plus longs, le suivi de ta progression et la revue de tes erreurs."),
   ("Quelle note faut-il à l'épreuve pratique du VTC ?", "Il faut au moins 12 sur 20. L'épreuve comprend une phase de conduite d'au moins 20 minutes, et un candidat admissible peut s'y présenter trois fois dans l'année qui suit les résultats de l'admissibilité.")],
  js="examen-compte.js", css=CSS_CALC)
