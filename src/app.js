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
