/* PACT — shared interactions */
(function(){
  var head=document.getElementById('head');
  if(head){
    var onScroll=function(){head.setAttribute('data-scrolled',window.scrollY>8?'true':'false');};
    onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  }

  /* reveal on scroll */
  var reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var els=document.querySelectorAll('.reveal');
  if(reduce||!('IntersectionObserver'in window)){els.forEach(function(e){e.classList.add('in');});}
  else{
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});
    },{threshold:.12,rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(e){io.observe(e);});
  }

  /* mobile menu */
  var mob=document.getElementById('mobileNav'),open=document.getElementById('menuBtn'),close=document.getElementById('menuClose');
  if(mob&&open){
    var set=function(o){mob.setAttribute('data-open',o?'true':'false');mob.setAttribute('aria-hidden',o?'false':'true');open.setAttribute('aria-expanded',o?'true':'false');document.body.style.overflow=o?'hidden':'';};
    open.addEventListener('click',function(){set(true);});
    if(close)close.addEventListener('click',function(){set(false);});
    mob.querySelectorAll('[data-close]').forEach(function(a){a.addEventListener('click',function(){set(false);});});
  }

  /* insights filter */
  var chipBtns=document.querySelectorAll('.chip-btn');
  if(chipBtns.length){
    chipBtns.forEach(function(b){
      b.addEventListener('click',function(){
        chipBtns.forEach(function(x){x.setAttribute('aria-pressed','false');});
        b.setAttribute('aria-pressed','true');
        var cat=b.getAttribute('data-cat');
        document.querySelectorAll('[data-art]').forEach(function(card){
          var show=cat==='all'||card.getAttribute('data-art')===cat;
          card.style.display=show?'':'none';
        });
      });
    });
  }

  /* contact form (front-end only; no backend wired yet) */
  var form=document.getElementById('contactForm');
  if(form){
    var msg=document.getElementById('formMsg');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(!form.checkValidity()){form.reportValidity();return;}
      msg.className='form__msg ok';
      msg.textContent='شكراً لتواصلك مع PACT. تلقّينا طلبك وسنراجعه للتواصل معك بشأن الخطوة التالية.';
      form.reset();
      msg.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});
    });
  }
})();
