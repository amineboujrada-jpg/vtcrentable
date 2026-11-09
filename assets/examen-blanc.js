/* Examen blanc VTC — tout se passe dans le navigateur, aucune réponse n'est envoyée.
   Les questions viennent de assets/examen-blanc-data.js (généré depuis content/examen-blanc/questions.json). */
(function () {
  "use strict";
  var D = window.EXAMEN_BLANC, root = document.getElementById("exam");
  if (!D || !root) return;

  var PAR_EPREUVE = 5;      // questions tirées par épreuve dans l'examen complet
  var MINUTES = 35;         // une minute par question
  var NB_VRAC = 20;         // questions de l'entraînement « toutes les épreuves »
  var EP = {};
  D.epreuves.forEach(function (e) { EP[e.id] = e; });
  var timer = null;
  var S = null;             // état de la session en cours

  function h(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function fr(n, d) { return n.toFixed(d === undefined ? 1 : d).replace(".", ","); }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function track(name, params) { try { if (window.gtag) window.gtag("event", name, params || {}); } catch (e) {} }
  function parEp(id) { return D.questions.filter(function (q) { return q.e === id; }); }

  // Prépare une question : ordre des réponses mélangé, bonne réponse repérée
  function prepare(q) {
    var idx = shuffle(q.o.map(function (_, i) { return i; }));
    return { q: q, order: idx, good: idx.indexOf(q.a), pick: -1, done: false };
  }

  function build(mode, ep) {
    var list;
    if (mode === "exam") {
      list = [];
      D.epreuves.forEach(function (e) { list = list.concat(shuffle(parEp(e.id)).slice(0, PAR_EPREUVE)); });
    } else if (ep === "all") {
      list = shuffle(D.questions).slice(0, NB_VRAC);
    } else {
      list = shuffle(parEp(ep));
    }
    return list.map(prepare);
  }

  function stopTimer() { if (timer) { clearInterval(timer); timer = null; } }
  function focusTitle() { var t = root.querySelector("[data-focus]"); if (t) t.focus({ preventScroll: false }); }

  // ---------- Écran de départ ----------
  function start() {
    stopTimer();
    S = null;
    var opts = D.epreuves.map(function (e) {
      return '<option value="' + e.id + '">' + e.id + " · " + h(e.court) + " (" + parEp(e.id).length + " questions)</option>";
    }).join("");
    root.innerHTML =
      '<h2 id="exam-t" tabindex="-1" data-focus style="margin-top:0">Lance ton examen blanc</h2>' +
      '<div class="seg" role="group" aria-label="Mode">' +
        '<button type="button" data-mode="exam" aria-pressed="true">Examen blanc complet</button>' +
        '<button type="button" data-mode="train" aria-pressed="false">Entraînement par épreuve</button>' +
      "</div>" +
      '<p id="mode-desc" class="note" style="margin:0 0 16px"></p>' +
      '<div id="train-opts" class="hide"><label for="ep-choix">Épreuve à réviser' +
        '<select id="ep-choix">' + opts + '<option value="all">Toutes les épreuves mélangées (' + NB_VRAC + " questions)</option></select></label></div>" +
      '<p style="margin:18px 0 0"><button type="button" class="btn" id="go">Commencer</button></p>';
    var mode = "exam";
    var desc = root.querySelector("#mode-desc"), tr = root.querySelector("#train-opts");
    function maj() {
      desc.textContent = mode === "exam"
        ? (PAR_EPREUVE * D.epreuves.length) + " questions (" + PAR_EPREUVE + " par épreuve), " + MINUTES + " minutes chrono, correction à la fin. Le verdict applique les coefficients et les notes éliminatoires de l'examen."
        : "Tu choisis une épreuve, sans chrono. Chaque réponse est corrigée tout de suite, avec l'explication.";
      tr.classList.toggle("hide", mode === "exam");
      Array.prototype.forEach.call(root.querySelectorAll("[data-mode]"), function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-mode") === mode); });
    }
    root.addEventListener("click", function onClick(ev) {
      var b = ev.target.closest("button");
      if (!b || !root.contains(b)) return;
      if (b.hasAttribute("data-mode")) { mode = b.getAttribute("data-mode"); maj(); }
      else if (b.id === "go") {
        root.removeEventListener("click", onClick);
        var ep = mode === "train" ? root.querySelector("#ep-choix").value : null;
        begin(mode, ep);
      }
    });
    maj();
  }

  function begin(mode, ep) {
    S = { mode: mode, ep: ep, items: build(mode, ep), i: 0, t0: Date.now(), confirmFin: false };
    track("examen_blanc_debut", { mode: mode, epreuve: ep || "toutes" });
    if (mode === "exam") {
      S.fin = S.t0 + MINUTES * 60000;
      timer = setInterval(tick, 1000);
    }
    show();
  }

  function restant() { return Math.max(0, Math.round((S.fin - Date.now()) / 1000)); }
  function chronoTxt() { var r = restant(); return Math.floor(r / 60) + ":" + ("0" + (r % 60)).slice(-2); }
  function tick() {
    var c = root.querySelector("#chrono");
    if (c) { c.textContent = chronoTxt(); c.classList.toggle("urgent", restant() <= 300); }
    if (restant() <= 0) finish(true);
  }

  // ---------- Question ----------
  function show() {
    var it = S.items[S.i], q = it.q, e = EP[q.e], n = S.items.length;
    var train = S.mode === "train";
    var opts = it.order.map(function (orig, k) {
      var cls = "", dis = "";
      if (it.done) {
        dis = " disabled";
        if (k === it.good) cls = " good"; else if (k === it.pick) cls = " bad";
      }
      return '<label class="opt' + cls + '"><input type="radio" name="rep" value="' + k + '"' + (it.pick === k ? " checked" : "") + dis + "><span>" + h(q.o[orig]) + "</span></label>";
    }).join("");
    var fb = "";
    if (it.done) {
      var ok = it.pick === it.good;
      fb = '<div class="fb ' + (ok ? "ok" : "ko") + '" role="status"><b>' + (ok ? "Bonne réponse" : "Pas tout à fait") + "</b> " + h(q.why) + "</div>";
    }
    var last = S.i === n - 1;
    var nav = '<div class="exam-nav">';
    if (!train && S.i > 0) nav += '<button type="button" class="btn ghost" id="prev">Précédent</button>';
    if (train) {
      if (!it.done) nav += '<button type="button" class="btn" id="valider"' + (it.pick < 0 ? " disabled" : "") + ">Valider</button>";
      else nav += '<button type="button" class="btn" id="suiv">' + (last ? "Voir mon résultat" : "Question suivante") + "</button>";
    } else {
      if (!last) nav += '<button type="button" class="btn" id="suiv">Suivante</button>';
      else nav += '<button type="button" class="btn" id="fin">' + (S.confirmFin ? "Terminer quand même" : "Terminer l'examen") + "</button>";
    }
    nav += "</div>";
    var warn = "";
    if (!train && last && S.confirmFin) {
      var vides = S.items.filter(function (x) { return x.pick < 0; }).length;
      warn = '<p class="note" style="color:var(--charge);font-weight:600">Il te reste ' + vides + " question" + (vides > 1 ? "s" : "") + " sans réponse. Elles compteront comme fausses.</p>";
    }
    root.innerHTML =
      '<div class="exam-top"><span id="exam-t" tabindex="-1" data-focus>Question ' + (S.i + 1) + " / " + n + "</span>" +
        '<span class="exam-ep">' + "Épreuve " + e.id + " · " + h(e.court) + "</span>" +
        (S.mode === "exam" ? '<span id="chrono" class="chrono" aria-label="Temps restant">' + chronoTxt() + "</span>" : "") +
      "</div>" +
      '<div class="exam-bar" aria-hidden="true"><i style="width:' + Math.round((S.i + (it.done ? 1 : 0)) / n * 100) + '%"></i></div>' +
      (q.texte ? '<blockquote class="exam-text">' + h(q.texte) + "</blockquote>" : "") +
      '<fieldset class="exam-q"><legend>' + h(q.q) + "</legend>" + opts + "</fieldset>" + fb + warn + nav;

    root.addEventListener("change", onChange);
    root.addEventListener("click", onNav);
    focusTitle();
  }

  function detach() { root.removeEventListener("change", onChange); root.removeEventListener("click", onNav); }

  function onChange(ev) {
    if (ev.target.name !== "rep" || !S) return;
    var it = S.items[S.i];
    if (it.done) return;
    it.pick = parseInt(ev.target.value, 10);
    S.confirmFin = false;
    var v = root.querySelector("#valider");
    if (v) v.disabled = false;
  }

  function onNav(ev) {
    var b = ev.target.closest("button");
    if (!b || !S) return;
    var it = S.items[S.i];
    if (b.id === "valider") { if (it.pick < 0) return; it.done = true; detach(); show(); }
    else if (b.id === "suiv") {
      detach();
      if (S.i < S.items.length - 1) { S.i++; show(); } else finish(false);
    }
    else if (b.id === "prev") { detach(); S.i--; show(); }
    else if (b.id === "fin") {
      var vides = S.items.some(function (x) { return x.pick < 0; });
      if (vides && !S.confirmFin) { S.confirmFin = true; detach(); show(); return; }
      detach(); finish(false);
    }
  }

  // ---------- Résultat ----------
  function finish(tempsEcoule) {
    stopTimer();
    detach();
    var items = S.items, groupes = {};
    items.forEach(function (it) {
      var g = groupes[it.q.e] || (groupes[it.q.e] = { ok: 0, n: 0 });
      g.n++; if (it.pick === it.good) g.ok++;
    });
    var total = items.filter(function (it) { return it.pick === it.good; }).length;
    var html = '<h2 id="exam-t" tabindex="-1" data-focus style="margin-top:0">Ton résultat</h2><div class="res" aria-live="polite">';
    var faible = null, faibleR = 2;

    if (S.mode === "exam") {
      var somme = 0, coefs = 0, elim = [];
      var lignes = D.epreuves.map(function (e) {
        var g = groupes[e.id], note = g.ok / g.n * 20;
        somme += note * e.coef; coefs += e.coef;
        var el = note < e.seuil;
        if (el) elim.push(e);
        if (g.ok / g.n < faibleR) { faibleR = g.ok / g.n; faible = e.id; }
        return '<tr><td>' + e.id + " · " + h(e.court) + '</td><td class="n">' + g.ok + " / " + g.n + '</td><td class="n">' + fr(note) + '</td><td class="n">' + e.coef + '</td><td class="n">' + (el ? '<span class="tag ko">sous ' + e.seuil + "</span>" : '<span class="tag ok">ok</span>') + "</td></tr>";
      });
      var moy = somme / coefs, adm = moy >= 10 && elim.length === 0;
      var titre, cls, txt;
      if (adm) { titre = "Tu serais admissible"; cls = "ok"; txt = "Moyenne pondérée d'au moins 10 / 20 et aucune note éliminatoire. Continue de t'entraîner pour viser large : le jour J compte aussi des questions à réponse courte."; }
      else if (moy >= 10) { titre = "Moyenne atteinte, mais note éliminatoire"; cls = "mid"; txt = "Ta moyenne dépasse 10 / 20, mais " + elim.map(function (e) { return "l'épreuve " + e.id + " (" + e.court + ")"; }).join(", ") + " est sous le seuil éliminatoire. Une seule suffit à t'arrêter : revois-la en priorité."; }
      else { titre = "Pas encore admissible"; cls = "bad"; txt = "Il te faut une moyenne pondérée d'au moins 10 / 20" + (elim.length ? " et aucune note éliminatoire (" + elim.map(function (e) { return e.id; }).join(", ") + " sous le seuil)" : "") + ". Reprends les corrections ci-dessous puis refais un examen."; }
      html += '<p class="k">Moyenne pondérée' + (tempsEcoule ? " · temps écoulé" : "") + '</p><p class="big' + (adm ? "" : " neg") + '">' + fr(moy) + ' / 20</p>' +
        '<p class="sub">' + total + " bonnes réponses sur " + items.length + "</p>" +
        '<div class="verdict ' + cls + '"><b>' + titre + "</b>" + txt + "</div>" +
        '<div class="tbl-res"><table class="small"><thead><tr><th>Épreuve</th><th class="n">Bonnes</th><th class="n">Note /20</th><th class="n">Coef.</th><th class="n">Seuil</th></tr></thead><tbody>' + lignes.join("") + "</tbody></table></div>" +
        '<p class="note-res">Seuils de l\'examen : moyenne pondérée d\'au moins 10 / 20, au moins 6 / 20 à chaque épreuve sauf l\'anglais (4 / 20). Barème simplifié : toutes les questions comptent pareil dans une épreuve.</p>';
      track("examen_blanc_fin", { mode: "exam", moyenne: Math.round(moy * 10) / 10, admissible: adm });
    } else {
      var note = total / items.length * 20, e1 = S.ep === "all" ? null : EP[S.ep];
      var verdict = "";
      if (e1) {
        var oks = note >= e1.seuil;
        verdict = '<div class="verdict ' + (oks ? "ok" : "bad") + '"><b>' + (oks ? "Au-dessus du seuil éliminatoire" : "Sous le seuil éliminatoire") + "</b>Pour l'épreuve " + e1.id + ", il faut au moins " + e1.seuil + " / 20. Vise plus haut : la moyenne générale doit atteindre 10 / 20.</div>";
        if (!oks) faible = e1.id;
      }
      html += '<p class="k">' + (e1 ? "Épreuve " + e1.id + " · " + h(e1.court) : "Toutes les épreuves") + '</p><p class="big">' + fr(note) + ' / 20</p>' +
        '<p class="sub">' + total + " bonnes réponses sur " + items.length + "</p>" + verdict;
      track("examen_blanc_fin", { mode: "train", epreuve: S.ep, note: Math.round(note * 10) / 10 });
    }
    html += '<p class="exam-actions"><button type="button" class="btn" id="again">Refaire un examen</button>' +
      (S.mode === "exam" && faible ? ' <button type="button" class="btn ghost-night" id="weak" data-ep="' + faible + '">Réviser l\'épreuve ' + faible + " (ta plus faible)</button>" : "") + "</p></div>";

    var fausses = items.filter(function (it) { return it.pick !== it.good; });
    html += "<h2>" + (fausses.length ? "À revoir (" + fausses.length + ")" : "Aucune erreur") + "</h2>";
    if (!fausses.length) html += "<p>Bravo, toutes les réponses étaient justes. Tente un nouvel examen : les questions sont tirées au hasard.</p>";
    fausses.forEach(function (it) {
      var q = it.q;
      html += '<div class="rev"><p class="rev-ep">Épreuve ' + q.e + " · " + h(EP[q.e].court) + "</p>" +
        (q.texte ? '<blockquote class="exam-text">' + h(q.texte) + "</blockquote>" : "") +
        "<p><b>" + h(q.q) + "</b></p>" +
        '<p class="rev-ko">Ta réponse : ' + (it.pick < 0 ? "<i>aucune</i>" : h(q.o[it.order[it.pick]])) + "</p>" +
        '<p class="rev-ok">Bonne réponse : ' + h(q.o[q.a]) + "</p>" +
        '<p class="rev-why">' + h(q.why) + "</p></div>";
    });
    root.innerHTML = html;
    root.addEventListener("click", onEnd);
    focusTitle();
  }

  function onEnd(ev) {
    var b = ev.target.closest("button");
    if (!b) return;
    if (b.id === "again") { root.removeEventListener("click", onEnd); start(); }
    else if (b.id === "weak") { root.removeEventListener("click", onEnd); begin("train", b.getAttribute("data-ep")); }
  }

  start();
})();
