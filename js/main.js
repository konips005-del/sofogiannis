(function () {
  var body = document.body;
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');

  var onScroll = function () { header && header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Μενού κινητού
  if (toggle) {
    var close = function () { body.classList.remove('menu-open'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.mobile-nav a').forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) { close(); toggle.focus(); }
    });
  }

  // Dropdown υπηρεσιών (πληκτρολόγιο / αφή)
  document.querySelectorAll('.nav .dd > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = btn.parentElement.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.nav .dd.open').forEach(function (dd) { dd.classList.remove('open'); dd.querySelector('button').setAttribute('aria-expanded', 'false'); });
  });

  // Ομαλή εμφάνιση κατά το scroll
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SEL = '.trust-item,.sec-title,.section-head > .lead,.service-card,.quote-card,.portrait,.split > div > p,.check-list li,.step,' +
    '.areas,.map,.faq details,.cta-band,.value,.feature,.contact-card,.side-card,.bizcard,.office,.timeline li,.prose > h2,.prose > p,.prose .photo,.note';
  var els = Array.prototype.slice.call(document.querySelectorAll(SEL));
  if (!reduce && 'IntersectionObserver' in window) {
    els.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.9) return; // ό,τι φαίνεται ήδη, μένει ως έχει
      el.classList.add('rv');
      var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return els.indexOf(c) > -1; });
      el.style.setProperty('--d', (Math.min(sibs.indexOf(el), 5) * 70) + 'ms');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  }

  // Καρτέλες οδηγού «Τι κάνω τώρα»
  var tabs = document.querySelectorAll('.guide-tabs [role="tab"]');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) {
        var sel = t === tab;
        t.setAttribute('aria-selected', sel ? 'true' : 'false');
        document.getElementById(t.getAttribute('aria-controls')).hidden = !sel;
      });
    });
  });

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
