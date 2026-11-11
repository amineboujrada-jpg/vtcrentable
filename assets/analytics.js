/* Mesure d'audience Google Analytics 4, chargée seulement après accord du visiteur (règles CNIL).
   Pour l'activer : remplace la valeur de GA_ID par ton identifiant de mesure (G-XXXXXXXXXX). Vide = rien n'est chargé. */
(function () {
  "use strict";
  var GA_ID = "G-4WV1YZM1PJ";
  if (!GA_ID || /^G-X+$/.test(GA_ID)) return;
  if (location.hostname !== "vtcrentable.com") return;   // pas de mesure sur la copie github.io

  var CLE = "vtcr-cookies";
  function lire() { try { return localStorage.getItem(CLE); } catch (e) { return null; } }
  function ecrire(v) { try { localStorage.setItem(CLE, v); } catch (e) {} }

  function charger() {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
  }

  // Retrait du consentement : arrête la mesure et supprime les cookies Google Analytics (_ga, _ga_*).
  function effacerCookies() {
    var hotes = [location.hostname, "." + location.hostname];
    document.cookie.split(";").forEach(function (c) {
      var nom = c.split("=")[0].trim();
      if (nom !== "_ga" && nom.indexOf("_ga_") !== 0 && nom !== "_gid") return;
      hotes.forEach(function (h) { document.cookie = nom + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + h; });
      document.cookie = nom + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    });
  }

  function bandeau() {
    if (document.getElementById("vtcr-bandeau")) return;
    var b = document.createElement("div");
    b.id = "vtcr-bandeau";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookies de mesure d'audience");
    b.style.cssText = "position:fixed;left:12px;right:12px;bottom:12px;z-index:50;max-width:560px;margin:0 auto;background:#0f1116;color:#f1f2f5;border:1px solid #2c3140;border-radius:14px;padding:16px;font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;box-shadow:0 12px 40px rgba(0,0,0,.35)";
    b.innerHTML = '<p style="margin:0 0 12px">On aimerait mesurer la fréquentation du site avec Google Analytics, pour savoir quelles pages t\'aident le plus. Aucune pub, aucune revente. Tu peux changer d\'avis à tout moment avec « Gérer mes cookies » en bas de page. Tu acceptes ?</p>' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap"><button type="button" data-v="oui" style="font:700 14px/1 inherit;background:#f2a614;color:#1d1400;border:0;border-radius:10px;padding:11px 16px;cursor:pointer">Accepter</button>' +
      '<button type="button" data-v="non" style="font:700 14px/1 inherit;background:transparent;color:#f1f2f5;border:1px solid #2c3140;border-radius:10px;padding:11px 16px;cursor:pointer">Refuser</button></div>';
    b.addEventListener("click", function (ev) {
      var v = ev.target && ev.target.getAttribute("data-v");
      if (!v) return;
      var avant = lire();
      ecrire(v);
      b.remove();
      if (v === "oui") charger();
      else {
        window["ga-disable-" + GA_ID] = true;
        effacerCookies();
        if (avant === "oui") location.reload();   // arrête le script déjà chargé
      }
    });
    document.body.appendChild(b);
  }

  // Lien « Gérer mes cookies » dans le pied de page : permet de retirer ou de donner son accord à tout moment.
  function lienGerer() {
    var pied = document.querySelector("footer nav") || document.querySelector("footer .wrap") || document.querySelector("footer");
    if (!pied || document.getElementById("vtcr-gerer-cookies")) return;
    var a = document.createElement("a");
    a.id = "vtcr-gerer-cookies";
    a.href = "#gerer-mes-cookies";
    a.textContent = "Gérer mes cookies";
    a.addEventListener("click", function (ev) { ev.preventDefault(); bandeau(); });
    pied.appendChild(a);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", lienGerer);
  else lienGerer();

  var choix = lire();
  if (choix === "oui") charger();
  else if (choix !== "non") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bandeau);
    else bandeau();
  }
})();
