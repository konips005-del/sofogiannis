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
    '.areas,.map,.faq details,.coffin,.cta-band,.value,.feature,.contact-card,.side-card,.bizcard,.office,.timeline li,.prose > h2,.prose > p,.prose .photo,.note';
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

  // Carousel φωτογραφιών με βελάκια
  document.querySelectorAll('.carousel').forEach(function (car) {
    var track = car.querySelector('.car-track');
    var slides = track.querySelectorAll('.slide');
    var prev = car.querySelector('.prev'), next = car.querySelector('.next');
    var dotsBox = car.querySelector('.car-dots');
    var step = function () { return slides[0].getBoundingClientRect().width + 14; };
    var pages = function () { return Math.max(1, Math.round((track.scrollWidth - track.clientWidth) / step()) + 1); };
    var drawDots = function () {
      dotsBox.innerHTML = '';
      for (var i = 0; i < pages(); i++) dotsBox.appendChild(document.createElement('span'));
    };
    var update = function () {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
      var idx = Math.round(track.scrollLeft / step());
      Array.prototype.forEach.call(dotsBox.children, function (d, i) { d.classList.toggle('on', i === idx); });
    };
    var go = function (dir) { track.scrollBy({ left: dir * step(), behavior: 'smooth' }); setTimeout(update, 60); setTimeout(update, 450); };
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); next.click(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); prev.click(); }
    });
    var t; track.addEventListener('scroll', function () { update(); clearTimeout(t); t = setTimeout(update, 150); }, { passive: true });
    window.addEventListener('resize', function () { drawDots(); update(); });
    drawDots(); update();
  });

  // Μουσική υπόκρουση (YouTube, κατόπιν επιθυμίας του πελάτη). Οι browsers δεν επιτρέπουν ήχο πριν
  // από την πρώτη αλληλεπίδραση, οπότε αν μπλοκαριστεί ξεκινά με το πρώτο κλικ/άγγιγμα/πλήκτρο.
  var VID = '8w_E3fyzPnw';
  var store = function (k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } };
  var sstore = function (k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } };
  var startMusic = function () {
    var box = document.createElement('div');
    box.className = 'music';
    box.innerHTML = '<div class="music-player"><div id="yt-music"></div></div>' +
      '<button type="button" class="music-btn" aria-pressed="false" aria-label="Μουσική">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18V5l11-2v13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6" cy="18" r="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="16" r="3" fill="none" stroke="currentColor" stroke-width="2"/></svg>' +
      '<span class="music-label">Μουσική</span><span class="music-eq" aria-hidden="true"><i></i><i></i><i></i></span></button>';
    document.body.appendChild(box);
    var btn = box.querySelector('.music-btn');
    var player, playing = false, wantOff = store('music') === 'off';
    var setUI = function () {
      btn.setAttribute('aria-pressed', playing ? 'true' : 'false');
      btn.setAttribute('aria-label', playing ? 'Παύση μουσικής' : 'Αναπαραγωγή μουσικής');
      box.classList.toggle('on', playing);
    };
    var gesture = function () {
      ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.removeEventListener(ev, gesture, true); });
      if (player && !playing && store('music') !== 'off') player.playVideo();
    };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (!player) return;
      if (playing) { player.pauseVideo(); store('music', 'off'); }
      else { store('music', 'on'); player.playVideo(); }
    });
    window.onYouTubeIframeAPIReady = function () {
      player = new YT.Player('yt-music', {
        width: 200, height: 113, videoId: VID,
        playerVars: { autoplay: wantOff ? 0 : 1, playsinline: 1, rel: 0, modestbranding: 1, start: Math.floor(+sstore('music-t') || 0) },
        events: {
          onReady: function () {
            if (wantOff) return;
            player.setVolume(60); player.playVideo();
            setTimeout(function () {
              if (!playing) ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.addEventListener(ev, gesture, true); });
            }, 1200);
          },
          onStateChange: function (e) {
            playing = e.data === 1;
            if (e.data === 0) { sstore('music-t', 0); player.seekTo(0); player.playVideo(); } // επανάληψη
            setUI();
          }
        }
      });
      setInterval(function () { if (playing && player.getCurrentTime) sstore('music-t', player.getCurrentTime()); }, 2000);
    };
    window.addEventListener('pagehide', function () { if (player && player.getCurrentTime) sstore('music-t', player.getCurrentTime()); });
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
  };
  if (document.readyState === 'complete') startMusic(); else window.addEventListener('load', startMusic);

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
