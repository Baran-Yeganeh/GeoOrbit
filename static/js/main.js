(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Navbar: scrolled state + mobile menu ---------- */
  var nav = $("#goNav");
  function onScroll() { if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 30); }
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  var burger = $("#goBurger");
  if (burger) burger.addEventListener("click", function () { nav.classList.toggle("is-open"); });

  /* ---------- Live mission search ---------- */
  var input = $("#searchInput"), results = $("#searchResults"), timer = null;
  if (input && results && window.jQuery) {
    input.addEventListener("input", function () {
      clearTimeout(timer);
      var q = input.value.trim();
      if (!q) { results.innerHTML = ""; return; }
      timer = setTimeout(function () {
        window.jQuery.ajax({
          url: "/gnss/search/", method: "GET", data: { name: q },
          success: function (res) {
            results.innerHTML = "";
            if (!res.mission.length) {
              var d = document.createElement("div");
              d.className = "search-empty"; d.textContent = "No mission found";
              results.appendChild(d); return;
            }
            res.mission.forEach(function (m) {
              var a = document.createElement("a");
              a.href = "/gnss/missiondetail/" + m.id + "/";
              a.textContent = m.name;               /* textContent: no HTML injection */
              results.appendChild(a);
            });
          }
        });
      }, 200);
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".go-search")) results.innerHTML = "";
    });
  }

  /* ---------- UTC clock ---------- */
  var clock = $("#clockUtc"), foot = $("#footClock");
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function tick() {
    var d = new Date(), t = pad(d.getUTCHours()) + ":" + pad(d.getUTCMinutes()) + ":" + pad(d.getUTCSeconds());
    if (clock) clock.textContent = t + " UTC";
    if (foot) foot.textContent = "UTC " + t;
  }
  tick(); setInterval(tick, 1000);

  /* ---------- Cycling survey-station coordinates ---------- */
  var coord = $("#coordNow");
  if (coord) {
    var pts = [["Tehran", 35.6892, 51.3890], ["Tabriz", 38.0800, 46.2919], ["Isfahan", 32.6546, 51.6680],
               ["Mashhad", 36.2605, 59.6168], ["Shiraz", 29.5918, 52.5837], ["Kish", 26.5579, 54.0194]];
    var i = 0;
    setInterval(function () {
      i = (i + 1) % pts.length; var p = pts[i];
      coord.style.opacity = 0;
      setTimeout(function () {
        coord.textContent = p[1].toFixed(4) + "° N " + p[2].toFixed(4) + "° E";
        coord.style.opacity = 1;
      }, 250);
    }, 3500);
    coord.style.transition = "opacity .25s";
  }

  /* ---------- Constellation accordion (touch / click) ---------- */
  var items = $$(".const-item");
  items.forEach(function (it) {
    it.addEventListener("mouseenter", function () { items.forEach(function (x) { x.classList.remove("is-open"); }); it.classList.add("is-open"); });
    it.addEventListener("click", function () { items.forEach(function (x) { x.classList.remove("is-open"); }); it.classList.add("is-open"); });
  });

  /* ---------- Count-up numbers ---------- */
  function countUp(el) {
    var to = parseInt(el.getAttribute("data-count"), 10) || 0, start = null, dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(to * e);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("is-visible");
        $$("[data-count]", en.target).forEach(countUp);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 80 + "ms"; io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
    $$("[data-count]").forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
  }
})();
