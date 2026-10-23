/* Kousthubh M S : site behaviour (no dependencies) */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Material ripple ---------- */
  document.addEventListener("pointerdown", function (e) {
    var el = e.target.closest(".btn, .chip, .icon-btn, .gopura-btn, .stambha, .c-item");
    if (!el || reduce) return;
    var r = el.getBoundingClientRect();
    var d = Math.max(r.width, r.height);
    var s = document.createElement("span");
    s.className = "ripple";
    s.style.width = s.style.height = d + "px";
    s.style.left = (e.clientX - r.left - d / 2) + "px";
    s.style.top = (e.clientY - r.top - d / 2) + "px";
    el.appendChild(s);
    setTimeout(function () { s.remove(); }, 650);
  });

  /* ---------- Gopura menu ---------- */
  var gopura = $("#gopura");
  var opener = $(".gopura-btn");
  var lastFocus = null;
  function openG() {
    if (!gopura) return;
    lastFocus = document.activeElement;
    gopura.classList.add("open");
    gopura.setAttribute("aria-hidden", "false");
    opener && opener.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    var cur = $(".tier[aria-current]", gopura) || $(".tier", gopura);
    setTimeout(function () { cur && cur.focus(); }, 60);
  }
  function closeG() {
    if (!gopura) return;
    gopura.classList.remove("open");
    gopura.setAttribute("aria-hidden", "true");
    opener && opener.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    lastFocus && lastFocus.focus && lastFocus.focus();
  }
  opener && opener.addEventListener("click", openG);
  gopura && $(".close", gopura).addEventListener("click", closeG);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && gopura && gopura.classList.contains("open")) closeG();
    if (e.key === "Tab" && gopura && gopura.classList.contains("open")) {
      var f = $$("a, button", gopura);
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Snackbar ---------- */
  function snack(msg) {
    var s = $(".snackbar");
    if (!s) { s = document.createElement("div"); s.className = "snackbar"; s.setAttribute("role", "status"); document.body.appendChild(s); }
    s.textContent = msg;
    s.classList.add("show");
    clearTimeout(snack.t);
    snack.t = setTimeout(function () { s.classList.remove("show"); }, 2600);
  }
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var v = b.getAttribute("data-copy");
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(function () { snack("Copied: " + v); });
      else snack(v);
    });
  });

  /* ---------- Sound: plucked string (Karplus-Strong) ---------- */
  var ctx = null;
  function ac() {
    if (!ctx) { var C = window.AudioContext || window.webkitAudioContext; if (!C) return null; ctx = new C(); }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }
  var cache = {};
  function pluckBuffer(freq, secs) {
    var key = Math.round(freq * 100) + ":" + secs;
    if (cache[key]) return cache[key];
    var a = ac(); var sr = a.sampleRate; var n = Math.floor(sr * secs);
    var buf = a.createBuffer(1, n, sr); var d = buf.getChannelData(0);
    var p = Math.round(sr / freq); var ring = new Float32Array(p);
    for (var i = 0; i < p; i++) ring[i] = Math.random() * 2 - 1;
    var idx = 0, prev = 0;
    for (var j = 0; j < n; j++) {
      var cur = ring[idx];
      var next = ring[(idx + 1) % p];
      var v = 0.4985 * (cur + next);
      ring[idx] = v * 0.999 + (Math.random() - .5) * 0.0004; /* jivari buzz */
      d[j] = cur * 0.6 + prev * 0.4; prev = cur;
      idx = (idx + 1) % p;
    }
    cache[key] = buf; return buf;
  }
  function pluck(freq, when, gain, secs) {
    var a = ac(); if (!a) return;
    var src = a.createBufferSource(); src.buffer = pluckBuffer(freq, secs || 2.4);
    var g = a.createGain(); g.gain.value = gain || .5;
    src.connect(g); g.connect(a.destination);
    src.start(when || a.currentTime);
  }
  var SA = 146.83; /* D, a common shruti for male vocalists */
  var RATIOS = [1, 16 / 15, 9 / 8, 6 / 5, 5 / 4, 4 / 3, 45 / 32, 3 / 2, 8 / 5, 5 / 3, 9 / 5, 15 / 8];
  window.KMS = { pluck: pluck, SA: SA, RATIOS: RATIOS, snack: snack };

  /* tambura drone: Pa Sa Sa Sa(low) */
  var droneTimer = null;
  function droneCycle() {
    var a = ac(); if (!a) return;
    var t = a.currentTime + .05;
    pluck(SA * 3 / 4, t, .35, 3.2);
    pluck(SA, t + .7, .3, 3.2);
    pluck(SA, t + 1.4, .3, 3.2);
    pluck(SA / 2, t + 2.1, .45, 3.6);
  }
  $$("[data-drone]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (droneTimer) {
        clearInterval(droneTimer); droneTimer = null;
        b.setAttribute("aria-pressed", "false"); $(".lbl", b).textContent = "Play tambura drone";
      } else {
        droneCycle(); droneTimer = setInterval(droneCycle, 2800);
        b.setAttribute("aria-pressed", "true"); $(".lbl", b).textContent = "Stop drone";
      }
    });
  });

  /* ---------- Rashi mandapa: 12 pillars / 12 swarasthanas ---------- */
  var ring = $("#ring");
  if (ring) {
    var RASHI = [
      ["ಮೇಷ", "Mesha", [3, 14]], ["ವೃಷಭ", "Vrishabha", [4, 15]], ["ಮಿಥುನ", "Mithuna", [5, 15]],
      ["ಕರ್ಕಾಟಕ", "Karkataka", [6, 16]], ["ಸಿಂಹ", "Simha", [7, 17]], ["ಕನ್ಯಾ", "Kanya", [8, 17]],
      ["ತುಲಾ", "Tula", [9, 17]], ["ವೃಶ್ಚಿಕ", "Vrishchika", [10, 16]], ["ಧನು", "Dhanu", [11, 16]],
      ["ಮಕರ", "Makara", [0, 14]], ["ಕುಂಭ", "Kumbha", [1, 13]], ["ಮೀನ", "Meena", [2, 14]]
    ];
    var SW = [
      ["ಸ", "S", "Shadja"], ["ರಿ₁", "R1", "Shuddha Rishabha"], ["ರಿ₂", "R2", "Chatushruti Rishabha"],
      ["ಗ₂", "G2", "Sadharana Gandhara"], ["ಗ₃", "G3", "Antara Gandhara"], ["ಮ₁", "M1", "Shuddha Madhyama"],
      ["ಮ₂", "M2", "Prati Madhyama"], ["ಪ", "P", "Panchama"], ["ದ₁", "D1", "Shuddha Dhaivata"],
      ["ದ₂", "D2", "Chatushruti Dhaivata"], ["ನಿ₂", "N2", "Kaishiki Nishada"], ["ನಿ₃", "N3", "Kakali Nishada"]
    ];
    var now = new Date(); var sun = 0;
    for (var k = 0; k < 12; k++) {
      var m = RASHI[k][2][0], dd = RASHI[k][2][1];
      var nk = RASHI[(k + 1) % 12][2];
      var start = new Date(now.getFullYear(), m, dd);
      var end = new Date(now.getFullYear() + (nk[0] < m ? 1 : 0), nk[0], nk[1]);
      var startPrev = new Date(now.getFullYear() - 1, m, dd);
      var endPrev = new Date(now.getFullYear() - 1 + (nk[0] < m ? 1 : 0), nk[0], nk[1]);
      if ((now >= start && now < end) || (now >= startPrev && now < endPrev)) sun = k;
    }
    var out = $("#rashi-out");
    var ray = $(".sunray", ring);
    var radius = 44;
    RASHI.forEach(function (r, i) {
      var ang = (i / 12) * 360 - 90;
      var rad = ang * Math.PI / 180;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "stambha" + (i === sun ? " sun" : "");
      var pos = "translate(" + (Math.cos(rad) * radius * ring.clientWidth / 100) + "px," + (Math.sin(rad) * radius * ring.clientWidth / 100) + "px)";
      b.style.setProperty("--pos", pos);
      b.style.transform = pos;
      b.dataset.i = i;
      b.innerHTML = '<span lang="kn">' + SW[i][0] + "</span><small>" + r[1].slice(0, 4) + "</small>";
      b.setAttribute("aria-label", "Pillar of " + r[1] + ", swarasthana " + SW[i][2]);
      ring.appendChild(b);
    });
    function place() {
      $$(".stambha", ring).forEach(function (b) {
        var i = +b.dataset.i; var rad = ((i / 12) * 360 - 90) * Math.PI / 180;
        var pos = "translate(" + (Math.cos(rad) * radius * ring.clientWidth / 100) + "px," + (Math.sin(rad) * radius * ring.clientWidth / 100) + "px)";
        b.style.setProperty("--pos", pos); b.style.transform = pos;
      });
    }
    window.addEventListener("resize", place);
    function aim(i) { if (ray) ray.style.transform = "rotate(" + ((i / 12) * 360 - 90) + "deg)"; }
    aim(sun);
    if (out) out.innerHTML = "Today the sun stands with <b>" + RASHI[sun][1] + "</b> (<span lang=\"kn\">" + RASHI[sun][0] + "</span>). Touch any pillar to hear its swara.";
    ring.addEventListener("click", function (e) {
      var b = e.target.closest(".stambha"); if (!b) return;
      var i = +b.dataset.i;
      pluck(SA * RATIOS[i], null, .55, 2.6);
      $$(".stambha.on", ring).forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on"); b.classList.remove("ping"); void b.offsetWidth; b.classList.add("ping");
      aim(i);
      $(".center b", ring).textContent = SW[i][0];
      $(".center small", ring).textContent = SW[i][2];
      if (out) out.innerHTML = "<b>" + RASHI[i][1] + "</b> pillar (<span lang=\"kn\">" + RASHI[i][0] + "</span>) sounds <b>" + SW[i][2] + "</b>, swarasthana " + (i + 1) + " of 12.";
    });
  }

  /* ---------- Raga wheel (Sadhana page) ---------- */
  var wheel = $("#raga-wheel");
  if (wheel) {
    var NS = "http://www.w3.org/2000/svg";
    var LBL = ["S", "R1", "R2", "G2", "G3", "M1", "M2", "P", "D1", "D2", "N2", "N3"];
    var C = 210, R = 160;
    var pts = LBL.map(function (l, i) { var a = (i / 12) * Math.PI * 2 - Math.PI / 2; return [C + Math.cos(a) * R, C + Math.sin(a) * R]; });
    var g = document.createElementNS(NS, "g");
    pts.forEach(function (p) { var ln = document.createElementNS(NS, "line"); ln.setAttribute("x1", C); ln.setAttribute("y1", C); ln.setAttribute("x2", p[0]); ln.setAttribute("y2", p[1]); ln.setAttribute("class", "spoke"); g.appendChild(ln); });
    wheel.appendChild(g);
    var shape = document.createElementNS(NS, "polygon"); shape.setAttribute("class", "shape"); wheel.appendChild(shape);
    var nodes = pts.map(function (p, i) {
      var c = document.createElementNS(NS, "circle"); c.setAttribute("cx", p[0]); c.setAttribute("cy", p[1]); c.setAttribute("r", 20); c.setAttribute("class", "node"); wheel.appendChild(c);
      var t = document.createElementNS(NS, "text"); t.setAttribute("x", p[0]); t.setAttribute("y", p[1]); t.textContent = LBL[i]; wheel.appendChild(t);
      return c;
    });
    var RAGAS = {
      mayamalavagowla: { n: "Mayamalavagowla", m: "Mela 15. The first raga a Karnataka student meets.", s: [0, 1, 4, 5, 7, 8, 11] },
      shankarabharanam: { n: "Dheerashankarabharanam", m: "Mela 29. Majestic and expansive.", s: [0, 2, 4, 5, 7, 9, 11] },
      kalyani: { n: "Mechakalyani", m: "Mela 65. The prati madhyama gives it a luminous lift.", s: [0, 2, 4, 6, 7, 9, 11] },
      kharaharapriya: { n: "Kharaharapriya", m: "Mela 22. Deep, tender and full of karuna.", s: [0, 2, 3, 5, 7, 9, 10] },
      mohana: { n: "Mohana", m: "Pentatonic, janya of Harikambhoji. Joyful and open.", s: [0, 2, 4, 7, 9] },
      hindola: { n: "Hindola", m: "Pentatonic, janya of Natabhairavi. Swinging and serene.", s: [0, 3, 5, 8, 10] }
    };
    var nameEl = $("#raga-name"), metaEl = $("#raga-meta");
    function show(key, play) {
      var r = RAGAS[key];
      shape.setAttribute("points", r.s.map(function (i) { return pts[i].join(","); }).join(" "));
      nodes.forEach(function (c, i) { c.classList.toggle("on", r.s.indexOf(i) > -1); c.classList.remove("play"); });
      nameEl.textContent = r.n; metaEl.textContent = r.m + " Arohana: " + r.s.map(function (i) { return LBL[i]; }).join(" ") + " S'";
      $$("[data-raga]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.raga === key ? "true" : "false"); });
      if (play) {
        var a = ac(); if (!a) return;
        var seq = r.s.concat([12]);
        seq.forEach(function (i, n) {
          var f = i === 12 ? SA * 2 : SA * RATIOS[i];
          pluck(f, a.currentTime + n * .42, .5, 1.8);
          setTimeout(function () {
            nodes.forEach(function (c) { c.classList.remove("play"); });
            nodes[i % 12].classList.add("play");
          }, n * 420);
        });
        setTimeout(function () { nodes.forEach(function (c) { c.classList.remove("play"); }); }, seq.length * 420 + 300);
      }
    }
    $$("[data-raga]").forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.raga, true); }); });
    show("mayamalavagowla", false);
  }

  /* ---------- Accolades filter ---------- */
  var chipsBox = $("#acc-chips");
  if (chipsBox) {
    chipsBox.addEventListener("click", function (e) {
      var c = e.target.closest(".chip"); if (!c) return;
      var f = c.dataset.f;
      $$(".chip", chipsBox).forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      $$(".tier-band").forEach(function (t) { t.hidden = !(f === "all" || t.dataset.cat === f); });
    });
  }

  /* ---------- Gallery lightbox ---------- */
  var lb = $("#lightbox");
  if (lb) {
    var items = $$(".masonry figure button");
    var img = $("img", lb), cap = $(".cap", lb), cur = 0, lastBtn = null;
    function showAt(i) {
      cur = (i + items.length) % items.length;
      var b = items[cur];
      img.src = b.dataset.full; img.alt = b.querySelector("img").alt;
      cap.textContent = b.dataset.cap || "";
    }
    items.forEach(function (b, i) { b.addEventListener("click", function () { lastBtn = b; showAt(i); lb.classList.add("open"); document.body.style.overflow = "hidden"; $(".x", lb).focus(); }); });
    function close() { lb.classList.remove("open"); document.body.style.overflow = ""; lastBtn && lastBtn.focus(); }
    $(".x", lb).addEventListener("click", close);
    $(".prev", lb).addEventListener("click", function () { showAt(cur - 1); });
    $(".next", lb).addEventListener("click", function () { showAt(cur + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") showAt(cur - 1);
      if (e.key === "ArrowRight") showAt(cur + 1);
    });
  }

  /* ---------- Enquiry form: compose an email ---------- */
  var form = $("#enquiry");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var subj = "Concert enquiry: " + (d.get("type") || "") + (d.get("date") ? " on " + d.get("date") : "");
      var body = "Namaskara Vidwan Kousthubh,\n\n" + (d.get("msg") || "") + "\n\nName: " + (d.get("name") || "") + "\nOrganisation / place: " + (d.get("org") || "") + "\nPhone: " + (d.get("phone") || "") + "\n";
      window.location.href = "mailto:kousthubms@gmail.com?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
      snack("Opening your email app");
    });
  }

  /* year */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
