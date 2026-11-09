/* Espace compte de l'examen blanc VTC : inscription, connexion, progression, banque complète de questions.
   Les comptes utilisent l'authentification Supabase (e-mail + mot de passe, confirmation par e-mail). La clé ci-dessous est publique :
   les tables sont protégées par des règles d'accès (RLS) — chacun ne lit et n'écrit que ses propres résultats. */
(function () {
  "use strict";
  var root = document.getElementById("espace"), D = window.EXAMEN_BLANC, M = window.VTCExamen;
  if (!root || !D || !M) return;

  var BASE = "https://izjwblfezffiksoyapwa.supabase.co";
  var CLE_API = "sb_publishable_oHSTBBoFqNQEBLQWgrOTgA_d5sACoZU";
  var RETOUR = "https://vtcrentable.com/examen-blanc-vtc/";
  var STORE = "vtcr-exam-session";
  var h = M.h, fr = M.fr;
  var EP = {}; D.epreuves.forEach(function (e) { EP[e.id] = e; });
  var moteur = null, banque = null, reponses = [], essais = [];

  // ---------- Session ----------
  function lire() { try { return JSON.parse(localStorage.getItem(STORE) || "null"); } catch (e) { return null; } }
  function ecrire(s) { try { if (s) localStorage.setItem(STORE, JSON.stringify(s)); else localStorage.removeItem(STORE); } catch (e) {} }
  function sessionDe(r) {
    return { access_token: r.access_token, refresh_token: r.refresh_token, expires_at: Math.floor(Date.now() / 1000) + (r.expires_in || 3600),
      email: (r.user && r.user.email) || (lire() || {}).email || "" };
  }
  function ajax(path, o) {
    o = o || {};
    var hd = { "apikey": CLE_API, "Content-Type": "application/json" };
    if (o.token) hd["Authorization"] = "Bearer " + o.token;
    if (o.prefer) hd["Prefer"] = o.prefer;
    return fetch(BASE + path, { method: o.method || "GET", headers: hd, body: o.body ? JSON.stringify(o.body) : undefined })
      .then(function (r) { return r.text().then(function (t) { var j = null; try { j = t ? JSON.parse(t) : null; } catch (e) {} return { ok: r.ok, status: r.status, json: j }; }); });
  }
  function jeton() {
    var s = lire();
    if (!s) return Promise.resolve(null);
    if (s.expires_at - 60 > Date.now() / 1000) return Promise.resolve(s.access_token);
    return ajax("/auth/v1/token?grant_type=refresh_token", { method: "POST", body: { refresh_token: s.refresh_token } }).then(function (r) {
      if (!r.ok || !r.json || !r.json.access_token) { ecrire(null); return null; }
      var n = sessionDe(r.json); n.email = s.email; ecrire(n); return n.access_token;
    }).catch(function () { return s.access_token; });
  }
  function api(path, o) {
    return jeton().then(function (t) { o = o || {}; o.token = t; return ajax(path, o); });
  }

  // Retour d'un lien de l'e-mail (confirmation ou mot de passe oublié) : la session arrive dans l'adresse
  function lireLien() {
    var p = new URLSearchParams((location.hash || "").replace(/^#/, ""));
    if (!p.get("access_token")) return null;
    var s = { access_token: p.get("access_token"), refresh_token: p.get("refresh_token"), expires_at: Math.floor(Date.now() / 1000) + (parseInt(p.get("expires_in"), 10) || 3600), email: "" };
    var type = p.get("type");
    try { history.replaceState(null, "", location.pathname + location.search + "#espace"); } catch (e) {}
    ecrire(s);
    return type;
  }

  // ---------- Écrans ----------
  function titre(txt) { return '<h2 id="espace-t" tabindex="-1" data-focus style="margin-top:0">' + txt + "</h2>"; }
  function focus() { var t = root.querySelector("[data-focus]"); if (t) t.focus({ preventScroll: true }); }
  function msg(el, txt, err) { el.textContent = txt; el.className = "m-msg" + (err ? " err" : ""); }

  function ecranAccueil(mode, info) {
    mode = mode || "ins";
    root.innerHTML = titre("Va plus loin avec un compte gratuit") +
      '<ul class="benef"><li><b>Toute la banque de questions</b> et des examens plus longs (10 questions par épreuve, 70 minutes).</li>' +
      "<li><b>Ta progression</b> épreuve par épreuve, avec l'historique de tes essais.</li>" +
      "<li><b>« Revoir mes erreurs »</b> : seules les questions que tu rates reviennent.</li></ul>" +
      (info ? '<p class="m-msg">' + h(info) + "</p>" : "") +
      '<div class="seg" role="group" aria-label="Compte">' +
        '<button type="button" data-t="ins" aria-pressed="' + (mode === "ins") + '">Créer mon compte</button>' +
        '<button type="button" data-t="con" aria-pressed="' + (mode === "con") + '">J\'ai déjà un compte</button></div>' +
      '<div id="zone"></div>';
    var zone = root.querySelector("#zone");
    function formIns() {
      zone.innerHTML = '<form id="f-ins" novalidate>' +
        '<label for="ins-mail"><span>Adresse e-mail</span><input id="ins-mail" type="email" autocomplete="email" required></label>' +
        '<label for="ins-mdp"><span>Mot de passe</span><small>8 caractères minimum</small><input id="ins-mdp" type="password" autocomplete="new-password" minlength="8" required></label>' +
        '<label class="consent"><input id="ins-ok" type="checkbox"><span>J\'accepte que VTC Rentable utilise mon adresse e-mail pour créer mon compte et gérer mon accès à l\'examen blanc. Je peux demander la suppression de mon compte à tout moment à contact@vtcrentable.com. <a href="https://app.vtcrentable.com/confidentialite.html">Politique de confidentialité</a></span></label>' +
        '<label class="consent"><input id="ins-nl" type="checkbox"><span>Facultatif : je souhaite recevoir par e-mail des conseils pour préparer l\'examen et des nouveautés de VTC Rentable. Je peux me désinscrire à tout moment.</span></label>' +
        '<p style="margin:14px 0 0"><button type="submit" class="btn" id="ins-go">Créer mon compte</button></p><p id="ins-msg" class="m-msg" role="status"></p></form>';
      zone.querySelector("#f-ins").addEventListener("submit", inscrire);
    }
    function formCon() {
      zone.innerHTML = '<form id="f-con" novalidate>' +
        '<label for="con-mail"><span>Adresse e-mail</span><input id="con-mail" type="email" autocomplete="email" required></label>' +
        '<label for="con-mdp"><span>Mot de passe</span><input id="con-mdp" type="password" autocomplete="current-password" required></label>' +
        '<p style="margin:14px 0 0"><button type="submit" class="btn" id="con-go">Me connecter</button> <button type="button" class="btn ghost" id="oubli">Mot de passe oublié</button></p>' +
        '<p id="con-msg" class="m-msg" role="status"></p><p><button type="button" class="lien" id="renvoi" hidden>Renvoyer l\'e-mail de confirmation</button></p></form>';
      zone.querySelector("#f-con").addEventListener("submit", connecter);
      zone.querySelector("#oubli").addEventListener("click", oublie);
      zone.querySelector("#renvoi").addEventListener("click", renvoyer);
    }
    (mode === "ins" ? formIns : formCon)();
    Array.prototype.forEach.call(root.querySelectorAll("[data-t]"), function (b) {
      b.addEventListener("click", function () {
        var m = b.getAttribute("data-t");
        Array.prototype.forEach.call(root.querySelectorAll("[data-t]"), function (x) { x.setAttribute("aria-pressed", x === b); });
        (m === "ins" ? formIns : formCon)();
      });
    });
  }

  function mailValide(s) { return /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(s); }

  function inscrire(ev) {
    ev.preventDefault();
    var mail = root.querySelector("#ins-mail").value.trim(), mdp = root.querySelector("#ins-mdp").value;
    var ok = root.querySelector("#ins-ok").checked, nl = root.querySelector("#ins-nl").checked;
    var m = root.querySelector("#ins-msg"), b = root.querySelector("#ins-go");
    if (!mailValide(mail)) return msg(m, "Vérifie ton adresse e-mail.", true);
    if (mdp.length < 8) return msg(m, "Le mot de passe doit faire 8 caractères au minimum.", true);
    if (!ok) return msg(m, "Coche la case d'acceptation pour créer ton compte.", true);
    b.disabled = true; msg(m, "Création du compte…");
    ajax("/auth/v1/signup?redirect_to=" + encodeURIComponent(RETOUR), { method: "POST",
      body: { email: mail, password: mdp, data: { source: "examen", consentement: "true", newsletter: nl ? "true" : "false" } } })
      .then(function (r) {
        b.disabled = false;
        if (r.ok && r.json && r.json.access_token) { ecrire(sessionDe(r.json)); ouvrir(); return; }
        if (r.ok) { confirmation(mail); return; }
        var c = r.json && (r.json.error_code || r.json.msg || "");
        if (c === "weak_password") msg(m, "Mot de passe trop faible : ajoute des chiffres ou des lettres différentes.", true);
        else if (c === "over_email_send_rate_limit" || r.status === 429) msg(m, "Trop de demandes pour l'instant : réessaie dans quelques minutes.", true);
        else if (c === "user_already_exists" || c === "email_exists") msg(m, "Cette adresse a déjà un compte : connecte-toi.", true);
        else msg(m, "Impossible de créer le compte pour le moment. Réessaie, ou écris à contact@vtcrentable.com.", true);
      }).catch(function () { b.disabled = false; msg(m, "Connexion impossible. Vérifie ta connexion internet.", true); });
  }

  function confirmation(mail) {
    root.innerHTML = titre("Vérifie ta boîte mail") +
      "<p>Nous venons d'envoyer un e-mail à <b>" + h(mail) + "</b>. Clique sur le lien pour confirmer ton adresse : tu arriveras directement dans ton espace.</p>" +
      '<p class="note">Rien reçu au bout de quelques minutes ? Regarde dans les courriers indésirables, ou écris à <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a>. Si tu as déjà un compte, connecte-toi.</p>' +
      '<p><button type="button" class="btn ghost" id="retour">Se connecter</button></p>';
    focus();
    root.querySelector("#retour").addEventListener("click", function () { ecranAccueil("con"); });
  }

  function connecter(ev) {
    ev.preventDefault();
    var mail = root.querySelector("#con-mail").value.trim(), mdp = root.querySelector("#con-mdp").value;
    var m = root.querySelector("#con-msg"), b = root.querySelector("#con-go"), ren = root.querySelector("#renvoi");
    ren.hidden = true;
    if (!mailValide(mail) || !mdp) return msg(m, "Saisis ton e-mail et ton mot de passe.", true);
    b.disabled = true; msg(m, "Connexion…");
    ajax("/auth/v1/token?grant_type=password", { method: "POST", body: { email: mail, password: mdp } }).then(function (r) {
      b.disabled = false;
      if (r.ok && r.json && r.json.access_token) { var s = sessionDe(r.json); s.email = mail; ecrire(s); ouvrir(); return; }
      var c = r.json && (r.json.error_code || "");
      if (c === "email_not_confirmed") { msg(m, "Confirme d'abord ton adresse e-mail avec le lien reçu à l'inscription.", true); ren.hidden = false; ren.setAttribute("data-mail", mail); }
      else if (r.status === 429) msg(m, "Trop d'essais : réessaie dans quelques minutes.", true);
      else msg(m, "E-mail ou mot de passe incorrect.", true);
    }).catch(function () { b.disabled = false; msg(m, "Connexion impossible. Vérifie ta connexion internet.", true); });
  }

  function renvoyer(ev) {
    var m = root.querySelector("#con-msg"), mail = ev.target.getAttribute("data-mail");
    ajax("/auth/v1/resend", { method: "POST", body: { type: "signup", email: mail, options: { emailRedirectTo: RETOUR } } }).then(function (r) {
      msg(m, r.ok ? "E-mail de confirmation renvoyé. Regarde aussi dans les courriers indésirables." : "Impossible de renvoyer l'e-mail pour le moment.", !r.ok);
    });
  }

  function oublie() {
    var mail = root.querySelector("#con-mail").value.trim(), m = root.querySelector("#con-msg");
    if (!mailValide(mail)) return msg(m, "Saisis d'abord ton adresse e-mail ci-dessus.", true);
    ajax("/auth/v1/recover?redirect_to=" + encodeURIComponent(RETOUR), { method: "POST", body: { email: mail } }).then(function (r) {
      msg(m, r.ok ? "Si un compte existe pour cette adresse, un e-mail de réinitialisation vient d'être envoyé." : "Impossible d'envoyer l'e-mail pour le moment. Réessaie dans quelques minutes.", !r.ok);
    });
  }

  function ecranNouveauMdp() {
    root.innerHTML = titre("Choisis un nouveau mot de passe") +
      '<form id="f-nm" novalidate><label for="nm"><span>Nouveau mot de passe</span><small>8 caractères minimum</small><input id="nm" type="password" autocomplete="new-password" minlength="8" required></label>' +
      '<p style="margin:14px 0 0"><button type="submit" class="btn" id="nm-go">Enregistrer</button></p><p id="nm-msg" class="m-msg" role="status"></p></form>';
    focus();
    root.querySelector("#f-nm").addEventListener("submit", function (ev) {
      ev.preventDefault();
      var v = root.querySelector("#nm").value, m = root.querySelector("#nm-msg");
      if (v.length < 8) return msg(m, "Le mot de passe doit faire 8 caractères au minimum.", true);
      api("/auth/v1/user", { method: "PUT", body: { password: v } }).then(function (r) {
        if (r.ok) ouvrir(); else msg(m, "Impossible de changer le mot de passe. Refais la demande depuis « Mot de passe oublié ».", true);
      });
    });
  }

  // ---------- Données du compte ----------
  function chargerBanque() {
    if (banque) return Promise.resolve(banque);
    return api("/rest/v1/exam_questions?select=e,q,texte,o,a,why&actif=eq.true&limit=1000").then(function (r) {
      if (!r.ok || !Array.isArray(r.json)) throw new Error("banque");
      var vus = {}, tout = [];
      D.questions.concat(r.json).forEach(function (q) { var k = M.cle(q); if (!vus[k]) { vus[k] = 1; tout.push(q); } });
      banque = { questions: tout, premium: r.json.length };
      return banque;
    });
  }
  function chargerHistorique() {
    return Promise.all([
      api("/rest/v1/exam_attempts?select=mode,ep,total,correct,moyenne,admissible,created_at&order=created_at.desc&limit=30"),
      api("/rest/v1/exam_answers?select=question_key,ok,created_at&order=created_at.desc&limit=3000")
    ]).then(function (res) {
      essais = res[0].ok && Array.isArray(res[0].json) ? res[0].json : [];
      reponses = res[1].ok && Array.isArray(res[1].json) ? res[1].json : [];
    });
  }
  // Dernière réponse connue par question
  function dernieres() {
    var d = {};
    reponses.forEach(function (r) { if (!(r.question_key in d)) d[r.question_key] = r.ok; });
    return d;
  }
  function aRevoir() {
    var d = dernieres();
    return banque.questions.filter(function (q) { return d[M.cle(q)] === false; });
  }

  function enregistrer(resume) {
    var tentative = { mode: resume.mode, ep: resume.ep, total: resume.total, correct: resume.correct, moyenne: resume.moyenne, admissible: resume.admissible, par_epreuve: resume.par_epreuve };
    api("/rest/v1/exam_attempts", { method: "POST", prefer: "return=minimal", body: tentative });
    if (resume.reponses.length) {
      api("/rest/v1/exam_answers", { method: "POST", prefer: "return=minimal", body: resume.reponses.map(function (r) { return { question_key: r.cle, ok: r.ok }; }) });
    }
    var now = new Date().toISOString();
    essais.unshift({ mode: resume.mode, ep: resume.ep, total: resume.total, correct: resume.correct, moyenne: resume.moyenne, admissible: resume.admissible, created_at: now });
    resume.reponses.slice().reverse().forEach(function (r) { reponses.unshift({ question_key: r.cle, ok: r.ok, created_at: now }); });
  }

  // ---------- Tableau de bord ----------
  var LIB = { examen: "Examen complet", entrainement: "Entraînement", erreurs: "Revue des erreurs" };
  function dateFr(iso) { try { return new Date(iso).toLocaleDateString("fr-FR", { day: "numeric", month: "short" }); } catch (e) { return ""; } }

  function tableau() {
    var s = lire(); if (!s) return ecranAccueil();
    var d = dernieres(), rev = aRevoir();
    var barres = D.epreuves.map(function (e) {
      var qs = banque.questions.filter(function (q) { return q.e === e.id; }), vues = 0, bonnes = 0;
      qs.forEach(function (q) { var v = d[M.cle(q)]; if (v !== undefined) { vues++; if (v) bonnes++; } });
      var pct = qs.length ? Math.round(bonnes / qs.length * 100) : 0;
      return '<div class="pg"><div class="pg-h"><b>' + e.id + " · " + h(e.court) + "</b><span>" + bonnes + " / " + qs.length + " maîtrisées</span></div>" +
        '<div class="pg-bar" role="img" aria-label="' + pct + ' % maîtrisé"><i style="width:' + pct + '%"></i></div></div>';
    }).join("");
    var ex = essais.filter(function (x) { return x.mode === "examen" && x.moyenne !== null; });
    var best = ex.reduce(function (m, x) { return Math.max(m, Number(x.moyenne)); }, -1);
    var kpi = '<div class="kpis kp"><div class="kpi"><b>' + essais.length + "</b><span>essais</span></div>" +
      '<div class="kpi"><b>' + (best >= 0 ? fr(best) : "–") + "</b><span>meilleure moyenne /20</span></div>" +
      '<div class="kpi"><b>' + banque.questions.length + "</b><span>questions dans la banque</span></div></div>";
    var hist = essais.slice(0, 5).map(function (x) {
      var sc = x.mode === "examen" && x.moyenne !== null ? fr(Number(x.moyenne)) + " / 20" : x.correct + " / " + x.total;
      return "<tr><td>" + dateFr(x.created_at) + "</td><td>" + (LIB[x.mode] || x.mode) + (x.ep && x.ep !== "all" ? " " + h(x.ep) : "") + '</td><td class="n">' + sc + "</td></tr>";
    }).join("");
    var opts = D.epreuves.map(function (e) { return '<option value="' + e.id + '">' + e.id + " · " + h(e.court) + "</option>"; }).join("") + '<option value="all">Toutes les épreuves mélangées</option>';
    root.innerHTML = titre("Ton espace d'entraînement") +
      '<p class="note" style="margin:0 0 14px">Connecté : <b>' + h(s.email || "ton compte") + '</b> · <button type="button" class="lien" id="sortir">Se déconnecter</button></p>' + kpi +
      '<div class="act"><button type="button" class="btn" id="b-exam">Examen blanc complet · ' + (10 * D.epreuves.length) + " questions, 70 min</button>" +
      '<button type="button" class="btn ghost" id="b-err"' + (rev.length ? "" : " disabled") + ">Revoir mes erreurs (" + rev.length + ")</button></div>" +
      '<div class="act"><label for="b-ep" style="flex:1 1 220px">Entraînement par épreuve<select id="b-ep">' + opts + '</select></label><button type="button" class="btn ghost" id="b-train">S\'entraîner</button></div>' +
      "<h3>Ta progression</h3>" + barres +
      (hist ? '<h3>Derniers essais</h3><div class="tbl"><table class="small"><tbody>' + hist + "</tbody></table></div>" : "");
    focus();
    root.querySelector("#sortir").addEventListener("click", deconnecter);
    root.querySelector("#b-exam").addEventListener("click", function () { lancer("exam", null, { parEpreuve: 10, minutes: 70, attemptMode: "examen" }); });
    root.querySelector("#b-train").addEventListener("click", function () { lancer("train", root.querySelector("#b-ep").value, { attemptMode: "entrainement" }); });
    root.querySelector("#b-err").addEventListener("click", function () { lancer("train", "all", { items: shuffle(aRevoir()).slice(0, 20), attemptMode: "erreurs" }); });
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function lancer(mode, ep, opts) {
    if (!moteur) {
      moteur = M.creer(root, { epreuves: D.epreuves, questions: banque.questions, parEpreuve: 10, minutes: 70, nbVrac: 20, onFinish: enregistrer, onRestart: tableau });
    }
    moteur.begin(mode, ep, opts);
    var top = root.getBoundingClientRect().top + window.pageYOffset - 70;
    window.scrollTo({ top: top, behavior: "smooth" });
  }

  function deconnecter() {
    var s = lire();
    if (moteur) { moteur.stop(); moteur = null; }
    banque = null; essais = []; reponses = [];
    if (s) ajax("/auth/v1/logout?scope=local", { method: "POST", token: s.access_token });
    ecrire(null);
    ecranAccueil("con", "Tu es déconnecté.");
  }

  // Ouvre l'espace : charge la banque (réservée aux comptes examen confirmés) puis affiche le tableau de bord
  function ouvrir() {
    root.innerHTML = titre("Chargement de ton espace…");
    chargerBanque().then(function (b) {
      if (!b.premium) { // compte valide mais sans accès examen (par exemple un compte de l'appli)
        root.innerHTML = titre("Compte non activé pour l'examen blanc") +
          '<p>Ce compte n\'a pas été créé depuis cette page. Crée un compte avec une autre adresse e-mail, ou écris à <a href="mailto:contact@vtcrentable.com">contact@vtcrentable.com</a>.</p>' +
          '<p><button type="button" class="btn ghost" id="sortir">Se déconnecter</button></p>';
        root.querySelector("#sortir").addEventListener("click", deconnecter);
        return;
      }
      return chargerHistorique().then(tableau);
    }).catch(function () {
      if (!lire()) { ecranAccueil("con", "Ta session a expiré : reconnecte-toi."); return; }
      root.innerHTML = titre("Espace momentanément indisponible") + "<p>Impossible de charger tes questions pour le moment. Réessaie dans un instant.</p>" +
        '<p><button type="button" class="btn ghost" id="retry">Réessayer</button> <button type="button" class="btn ghost" id="sortir">Se déconnecter</button></p>';
      root.querySelector("#retry").addEventListener("click", ouvrir);
      root.querySelector("#sortir").addEventListener("click", deconnecter);
    });
  }

  // ---------- Démarrage ----------
  var type = lireLien();
  if (type === "recovery") ecranNouveauMdp();
  else if (lire()) ouvrir();
  else ecranAccueil("ins");
  if (type) { var sec = document.getElementById("espace-section"); if (sec) sec.scrollIntoView(); }
})();
