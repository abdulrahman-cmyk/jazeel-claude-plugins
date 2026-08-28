/* PACT ARC — shared interactions */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var head = document.getElementById('head');

  /* ---- reveal on scroll ---- */
  var els = document.querySelectorAll('.reveal');
  if(reduce || !('IntersectionObserver' in window)){
    els.forEach(function(e){ e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
    }, {threshold:.12, rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){ io.observe(e); });
  }

  /* ---- count-up for stat numbers ---- */
  function ease(p){ return 1 - Math.pow(1 - p, 3); }
  function countUp(el){
    var raw = el.textContent.trim();
    var m = raw.match(/^(\D*)(\d+)(\D*)$/);
    if(!m){ return; }
    var pre = m[1], target = parseInt(m[2], 10), suf = m[3], width = m[2].length;
    var dur = 1200, start = null;
    function pad(v){ var s = String(v); while(s.length < width){ s = '0' + s; } return s; }
    function step(ts){
      if(start === null){ start = ts; }
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = pre + pad(Math.round(ease(p) * target)) + suf;
      if(p < 1){ requestAnimationFrame(step); }
    }
    requestAnimationFrame(step);
  }
  var nums = document.querySelectorAll('.stat__k');
  if(nums.length && !reduce && 'IntersectionObserver' in window){
    var nio = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if(en.isIntersecting){ countUp(en.target); nio.unobserve(en.target); } });
    }, {threshold:.6});
    nums.forEach(function(n){ nio.observe(n); });
  }

  /* ---- unified scroll loop: header shadow · progress bar · hero parallax ---- */
  var prog = document.createElement('div');
  prog.className = 'scroll-prog';
  prog.setAttribute('aria-hidden', 'true');
  document.body.appendChild(prog);

  var hero = document.querySelector('.hero');
  var pArc = hero && hero.querySelector('.hero__arc');
  var pPeak = hero && hero.querySelector('.hero__peak');
  var pGlow = hero && hero.querySelector('.hero__glow');

  var ticking = false;
  function onFrame(){
    ticking = false;
    var doc = document.documentElement;
    var y = window.scrollY || doc.scrollTop;

    if(head){ head.setAttribute('data-scrolled', y > 8 ? 'true' : 'false'); }

    var max = doc.scrollHeight - doc.clientHeight;
    prog.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';

    if(!reduce && hero && y < window.innerHeight){
      if(pArc){ pArc.style.transform = 'translateY(' + (y * 0.18) + 'px)'; }
      if(pPeak){ pPeak.style.transform = 'translateY(' + (y * 0.10) + 'px)'; }
      if(pGlow){ pGlow.style.transform = 'translateY(' + (y * 0.06) + 'px)'; }
    }
  }
  function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(onFrame); } }
  window.addEventListener('scroll', onScroll, {passive:true});
  onFrame();

  /* ---- insights filter ---- */
  var chipBtns = document.querySelectorAll('.chip-btn');
  if(chipBtns.length){
    chipBtns.forEach(function(b){
      b.addEventListener('click', function(){
        chipBtns.forEach(function(x){ x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        var cat = b.getAttribute('data-cat');
        document.querySelectorAll('[data-art]').forEach(function(card){
          card.style.display = (cat === 'all' || card.getAttribute('data-art') === cat) ? '' : 'none';
        });
      });
    });
  }

  /* ---- mobile menu ---- */
  var mob = document.getElementById('mobileNav'),
      open = document.getElementById('menuBtn'),
      close = document.getElementById('menuClose');
  if(mob && open){
    var set = function(o){
      mob.setAttribute('data-open', o ? 'true' : 'false');
      mob.setAttribute('aria-hidden', o ? 'false' : 'true');
      open.setAttribute('aria-expanded', o ? 'true' : 'false');
      document.body.style.overflow = o ? 'hidden' : '';
    };
    open.addEventListener('click', function(){ set(true); });
    if(close){ close.addEventListener('click', function(){ set(false); }); }
    mob.querySelectorAll('[data-close]').forEach(function(a){ a.addEventListener('click', function(){ set(false); }); });
  }

  /* ---- contact form (front-end only; no backend wired yet) ---- */
  var form = document.getElementById('contactForm');
  if(form){
    var msg = document.getElementById('formMsg');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!form.checkValidity()){ form.reportValidity(); return; }
      msg.className = 'form__msg ok';
      msg.textContent = 'شكراً لتواصلك مع PACT ARC. تلقّينا طلبك وسنراجعه للتواصل معك بشأن الخطوة التالية.';
      form.reset();
      msg.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    });
  }
})();
