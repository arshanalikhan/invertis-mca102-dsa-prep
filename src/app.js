// MCA102 DSA Prep: theme, phone menu, revision progress, mock timer, past-paper filters, tooltips.
// Everything is stored in this browser only (localStorage keys start with "mca102-").
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  // ---- theme: system -> light -> dark
  var root = document.documentElement;
  function themeLabel() {
    var t = root.getAttribute("data-theme") || "system";
    $$(".themebtn span").forEach(function (s) { s.textContent = "Theme: " + t; });
    $$(".themebtn").forEach(function (b) { b.setAttribute("aria-label", "Switch theme (now " + t + ")"); });
  }
  $$(".themebtn").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = root.getAttribute("data-theme");
      var next = !t ? "light" : t === "light" ? "dark" : null;
      if (next) root.setAttribute("data-theme", next); else root.removeAttribute("data-theme");
      try { if (next) localStorage.setItem("mca102-theme", next); else localStorage.removeItem("mca102-theme"); } catch (e) {}
      themeLabel();
    });
  });
  themeLabel();

  // ---- phone menu (drawer)
  var menu = $("#menuBtn"), scrim = $("#scrim");
  function setNav(open) {
    document.body.classList.toggle("navopen", open);
    if (scrim) scrim.hidden = !open;
    if (menu) menu.setAttribute("aria-expanded", String(open));
  }
  if (menu) menu.addEventListener("click", function () { setNav(!document.body.classList.contains("navopen")); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });

  // ---- back to top
  var top = $("#totop");
  if (top) {
    window.addEventListener("scroll", function () { top.classList.toggle("show", window.scrollY > 900); }, { passive: true });
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  // ---- revision progress
  var done = load("mca102-done", []);
  function isDone(id) { return done.indexOf(id) >= 0; }
  function paint() {
    $$("[data-done]").forEach(function (b) {
      var on = isDone(b.getAttribute("data-done"));
      b.setAttribute("aria-pressed", String(on));
      b.textContent = on ? "Revised" : "Mark as revised";
    });
    $$("[data-tick]").forEach(function (t) { t.classList.toggle("on", isDone(t.getAttribute("data-tick"))); });
    $$(".unitprog, .ucard").forEach(function (box) {
      var ids = (box.getAttribute("data-ids") || "").split(",").filter(Boolean);
      var n = ids.filter(isDone).length;
      var bar = $(".bar i", box), lbl = $(".lbl", box);
      if (bar) bar.style.width = (ids.length ? 100 * n / ids.length : 0) + "%";
      if (lbl) lbl.textContent = box.classList.contains("ucard") ? n + " of " + ids.length + " revised" : n + " of " + ids.length + " long answers revised";
    });
  }
  $$("[data-done]").forEach(function (b) {
    b.addEventListener("click", function () {
      var id = b.getAttribute("data-done");
      if (isDone(id)) done.splice(done.indexOf(id), 1); else done.push(id);
      save("mca102-done", done);
      paint();
    });
  });
  paint();

  // ---- mock papers: open all answers, 3-hour timer
  $$("[data-openall]").forEach(function (b) {
    b.addEventListener("click", function () {
      var all = $$("details.mans"), open = all.some(function (d) { return !d.open; });
      all.forEach(function (d) { d.open = open; });
      b.textContent = open ? "Hide all answers" : "Show all answers";
    });
  });
  $$("[data-timer]").forEach(function (b) {
    var slug = b.getAttribute("data-timer"), out = $('[data-timer-out="' + slug + '"]'), key = "mca102-timer-" + slug, tick = null;
    function fmt(ms) {
      var s = Math.abs(Math.round(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
      return (ms < 0 ? "+" : "") + h + ":" + String(m).padStart(2, "0") + ":" + String(x).padStart(2, "0");
    }
    function run() {
      var start = load(key, null);
      if (!start) { out.hidden = true; b.textContent = "Start 3-hour timer"; return; }
      out.hidden = false; b.textContent = "Reset timer";
      var left = start + 3 * 3600 * 1000 - Date.now();
      out.textContent = left >= 0 ? fmt(left) + " left" : "Time up " + fmt(left);
      out.classList.toggle("over", left < 0);
    }
    b.addEventListener("click", function () {
      if (load(key, null)) { if (!confirm("Reset the timer for this paper?")) return; save(key, null); }
      else save(key, Date.now());
      run();
    });
    run();
    tick = setInterval(run, 1000);
  });

  // ---- past papers: unit chips + search
  var search = $("#pqSearch");
  if (search) {
    var unit = "all", count = $("#pqCount");
    var apply = function () {
      var term = search.value.trim().toLowerCase(), shown = 0;
      $$(".pq").forEach(function (li) {
        var ok = (unit === "all" || li.getAttribute("data-unit") === unit) && (!term || li.textContent.toLowerCase().indexOf(term) >= 0);
        li.hidden = !ok;
        if (ok) shown++;
      });
      $$(".ppaper").forEach(function (p) { p.hidden = !$$(".pq", p).some(function (li) { return !li.hidden; }); });
      if (count) count.textContent = shown + " questions shown";
    };
    search.addEventListener("input", apply);
    $$(".chip").forEach(function (c) {
      c.addEventListener("click", function () {
        unit = c.getAttribute("data-f");
        $$(".chip").forEach(function (x) { x.classList.toggle("on", x === c); });
        apply();
      });
    });
    apply();
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
  }

  // ---- reading tools (as on the GATE CSE prep site): text size, focus mode, self-test
  var SCALES = [["S", 0.92], ["M", 1], ["L", 1.12], ["XL", 1.25]];
  var sizeBtn = $("#sizeBtn"), sizeLbl = $("#sizeLbl");
  function curScale() { var v = parseFloat(load("mca102-scale", 1)); return isNaN(v) ? 1 : v; }
  function paintScale() {
    var v = curScale(), i = SCALES.findIndex(function (s) { return s[1] === v; });
    root.style.setProperty("--reading-scale", v);
    if (sizeLbl) sizeLbl.textContent = (SCALES[i] || SCALES[1])[0];
  }
  if (sizeBtn) sizeBtn.addEventListener("click", function () {
    var i = SCALES.findIndex(function (s) { return s[1] === curScale(); });
    save("mca102-scale", SCALES[(i + 1) % SCALES.length][1]); paintScale();
  });
  paintScale();

  function toggleBtn(btn, key, cls) {
    if (!btn) return;
    function paintT() { var on = !!load(key, false); document.body.classList.toggle(cls, on); btn.setAttribute("aria-pressed", String(on)); }
    btn.addEventListener("click", function () { save(key, !load(key, false)); paintT(); });
    paintT();
  }
  toggleBtn($("#focusBtn"), "mca102-focus", "focus");
  var testBtn = $("#testBtn");
  if (testBtn && $(".qa")) { testBtn.hidden = false; toggleBtn(testBtn, "mca102-selftest", "selftest"); }
  $$(".revealbtn").forEach(function (b) {
    b.addEventListener("click", function () { b.closest(".qa").classList.add("shown"); });
  });
  if (location.hash) { var tq = document.getElementById(location.hash.slice(1)); if (tq && tq.classList.contains("qa")) tq.classList.add("shown"); }

  // ---- "On this page" outline with scroll-spy
  var otp = $("#otp");
  if (otp) {
    var heads = $$("main h2[id], main .qa[id]").filter(function (h) { return !h.closest(".shorts") || h.classList.contains("qa") === false; });
    var items = [];
    $$("main h2").forEach(function (h, i) { if (!h.id) h.id = "s-" + i; });
    $$("main h2, main .qa.long, main .qa.problem").forEach(function (h) {
      if (h.closest(".card") || h.closest(".hero")) return;
      var isQ = h.classList.contains("qa");
      var label = isQ ? ($(".q", h) || h).textContent.replace(/^Q\.\s*/, "") : h.childNodes[0].textContent;
      items.push({ el: h, id: h.id, label: label.trim(), lvl: isQ ? 3 : 2 });
    });
    if (items.length >= 3) {
      otp.innerHTML = "<p>On this page</p><ol>" + items.map(function (it) {
        var t = it.label.length > 70 ? it.label.slice(0, 68) + "…" : it.label;
        return '<li><a class="l' + it.lvl + '" href="#' + it.id + '">' + t.replace(/</g, "&lt;") + "</a></li>";
      }).join("") + "</ol>";
      document.body.classList.add("has-otp");
      var links = $$("a", otp);
      var spy = function () {
        var y = 90, cur = 0;
        items.forEach(function (it, i) { if (it.el.getBoundingClientRect().top < y + 40) cur = i; });
        links.forEach(function (a, i) { a.classList.toggle("on", i === cur); });
        var on = links[cur]; if (on && (on.offsetTop < otp.scrollTop || on.offsetTop > otp.scrollTop + otp.clientHeight - 30)) otp.scrollTop = on.offsetTop - 60;
      };
      window.addEventListener("scroll", spy, { passive: true }); spy();
    }
  }

  // ---- site search in the header ("/" to focus)
  var q = $("#q"), sres = $("#sres"), index = null, hits = [], sel = -1;
  function getIndex() {
    if (index) return Promise.resolve(index);
    var src = $('script[src*="app.js"]').getAttribute("src").replace(/app\.js.*$/, "search.json");
    return fetch(src).then(function (r) { return r.json(); }).then(function (d) { index = d; return d; });
  }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function mark(t, terms) {
    var out = esc(t);
    terms.forEach(function (w) { if (w.length > 1) out = out.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>"); });
    return out;
  }
  function snippetOf(x, terms) {
    if (!x) return "";
    var lx = x.toLowerCase(), i = Math.max(0, lx.indexOf(terms[0]) - 50);
    return (i ? "…" : "") + x.slice(i, i + 140) + "…";
  }
  function runSearch() {
    var v = q.value.trim().toLowerCase();
    if (v.length < 2) { sres.hidden = true; q.setAttribute("aria-expanded", "false"); return; }
    getIndex().then(function (ix) {
      var terms = v.split(/\s+/);
      hits = ix.map(function (d) {
        var t = d.t.toLowerCase(), x = d.x.toLowerCase(), score = 0;
        for (var k = 0; k < terms.length; k++) {
          var w = terms[k];
          if (t.indexOf(w) >= 0) score += 3; else if (x.indexOf(w) >= 0) score += 1; else return null;
        }
        if (d.k === "Page") score += 1;
        if (d.k.indexOf("7 marks") >= 0) score += 0.5;
        return { d: d, s: score };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
      sel = -1;
      sres.innerHTML = hits.length ? hits.map(function (h, i) {
        return '<a href="' + h.d.u + '" role="option" data-i="' + i + '"><small>' + esc(h.d.k) + "</small><b>" + mark(h.d.t, terms) + "</b>" +
          (h.d.x ? "<span>" + mark(snippetOf(h.d.x, terms), terms) + "</span>" : "") + "</a>";
      }).join("") : '<div class="none">No results for “' + esc(v) + '”</div>';
      sres.hidden = false; q.setAttribute("aria-expanded", "true");
    });
  }
  if (q) {
    q.addEventListener("input", runSearch);
    q.addEventListener("focus", function () { getIndex(); if (q.value.trim().length > 1) runSearch(); });
    q.addEventListener("keydown", function (e) {
      var as = $$("a", sres);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); if (!as.length) return;
        sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + as.length) % as.length;
        as.forEach(function (a, i) { a.classList.toggle("on", i === sel); }); as[sel].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && as.length) { location.href = as[Math.max(0, sel)].getAttribute("href"); }
      else if (e.key === "Escape") { sres.hidden = true; q.blur(); }
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) sres.hidden = true; });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) { e.preventDefault(); q.focus(); }
    });
    window.addEventListener("hashchange", function () {
      var t = document.getElementById(location.hash.slice(1)); if (t && t.classList.contains("qa")) t.classList.add("shown");
    });
  }

  // ---- tooltips for [data-tip] (heatmap cells, badges, ranking rows)
  var tip = $("#tip");
  function place(e) {
    var x = e.clientX + 14, y = e.clientY + 14, w = tip.offsetWidth, h = tip.offsetHeight;
    if (x + w > window.innerWidth - 8) x = e.clientX - w - 14;
    if (y + h > window.innerHeight - 8) y = e.clientY - h - 14;
    tip.style.left = Math.max(8, x) + "px"; tip.style.top = Math.max(8, y) + "px";
  }
  if (tip) {
    document.addEventListener("mouseover", function (e) {
      var t = e.target.closest && e.target.closest("[data-tip]");
      if (!t) { tip.hidden = true; return; }
      tip.textContent = t.getAttribute("data-tip"); tip.hidden = false; place(e);
    });
    document.addEventListener("mousemove", function (e) { if (!tip.hidden) place(e); });
    document.addEventListener("scroll", function () { tip.hidden = true; }, { passive: true });
  }
})();
