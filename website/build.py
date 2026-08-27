#!/usr/bin/env python3
"""PACT static site builder.

Assembles every page from shared partials (one header/footer definition) so
the chrome stays identical across the site, then also emits a self-contained
copy of each page under dist/ with CSS + JS inlined (for previewing or for
dropping onto any static host).

Run:  python3 build.py
"""
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT / "assets"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600'
    '&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700'
    '&family=Inter:wght@300;400;500;600&family=Readex+Pro:wght@300;400;500;600;700&display=swap" />')

ICON = ('<svg class="pa-icon" viewBox="0 0 60 74" aria-hidden="true">'
    '<path d="M5 71 L30 5 L55 71" fill="none" stroke="currentColor" stroke-width="3" '
    'stroke-linejoin="round" stroke-linecap="round"/>'
    '<polygon points="30,30 39,50 21,50" fill="currentColor"/></svg>')

def wordmark(color=None):
    style = f' style="color:{color}"' if color else ''
    return f'<span class="wordmark"{style}>P{ICON}C&#8202;T</span>'

NAV = [
    ("index.html", "الرئيسية"),
    ("legal-studies.html", "الدراسات القانونية"),
    ("corporate-contracts.html", "استشارات العقود"),
    ("how-we-work.html", "كيف نعمل"),
    ("about.html", "عن PACT"),
    ("insights.html", "الرؤى"),
]

def header(active):
    def link(href, label):
        cur = ' aria-current="page"' if href == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    links = "\n      ".join(link(h, l) for h, l in NAV)
    mob_links = "\n    ".join(
        f'<a href="{href}" data-close>{label}</a>' for href, label in NAV)
    return f'''<header class="site-head" id="head">
  <div class="head-inner">
    <a href="index.html" class="logo" aria-label="PACT — الصفحة الرئيسية">
      {wordmark()}
      <span class="logo__tag">Legal Advisory &nbsp;|&nbsp; Due Diligence</span>
    </a>
    <nav class="nav" aria-label="التنقل الرئيسي">
      {links}
    </nav>
    <div class="head-cta">
      <a href="contact.html" class="btn btn--solid">اطلب لقاءً تمهيدياً <span class="ar">←</span></a>
      <button class="iconbtn menu-btn" id="menuBtn" aria-label="القائمة" aria-expanded="false">☰</button>
    </div>
  </div>
</header>

<div class="mobile-nav" id="mobileNav" aria-hidden="true">
  <div class="mobile-nav__top">
    <span class="logo logo--onbrand">{wordmark()}<span class="logo__tag">Legal Advisory &nbsp;|&nbsp; Due Diligence</span></span>
    <button class="iconbtn" id="menuClose" aria-label="إغلاق">✕</button>
  </div>
  <nav aria-label="التنقل للجوال">
    {mob_links}
  </nav>
  <a href="contact.html" class="btn btn--onbrand" data-close>اطلب لقاءً تمهيدياً <span class="ar">←</span></a>
</div>'''

def closing(title, text, primary=("contact.html","اطلب لقاءً تمهيدياً"), secondary=("legal-studies.html","استكشف خدماتنا")):
    return f'''<section class="closing">
  <svg class="closing__peak" viewBox="0 0 200 120" aria-hidden="true"><polygon points="100,10 190,118 10,118"/></svg>
  <div class="closing__inner">
    <span class="eyebrow reveal">الدعوة الختامية</span>
    <h2 class="reveal" data-d="1">{title}</h2>
    <p class="reveal" data-d="2">{text}</p>
    <div class="closing__cta reveal" data-d="2">
      <a href="{primary[0]}" class="btn btn--onbrand">{primary[1]} <span class="ar">←</span></a>
      <a href="{secondary[0]}" class="btn btn--onbrand-ghost">{secondary[1]}</a>
    </div>
    <div class="closing__trust reveal" data-d="3"><span>نطاق واضح</span><span class="dot"></span><span>مخرَج عملي</span><span class="dot"></span><span>سرّية منضبطة</span></div>
  </div>
</section>'''

FOOTER = f'''<footer class="foot">
  <div class="foot__inner">
    <div class="foot__top">
      <div class="foot__brand">
        <span class="logo logo--onbrand">{wordmark("#fff")}<span class="logo__tag">Legal Advisory &nbsp;|&nbsp; Due Diligence</span></span>
        <p>رؤية قانونية واضحة ومسنَّدة قبل القرارات المفصلية — للمنشآت التي تتخذ قراراتها على أساس منظّم.</p>
        <div class="foot__offices"><span>LONDON</span><span class="dot">·</span><span>DUBAI</span><span class="dot">·</span><span>RIYADH</span><span class="dot">·</span><span>NEW YORK</span></div>
      </div>
      <div class="foot__col"><h4>الخدمات</h4><ul>
        <li><a href="legal-studies.html">الدراسات القانونية</a></li>
        <li><a href="legal-studies.html">تشخيص الوضع القانوني</a></li>
        <li><a href="legal-studies.html">العناية القانونية الواجبة</a></li>
        <li><a href="corporate-contracts.html">استشارات عقود الشركات</a></li>
      </ul></div>
      <div class="foot__col"><h4>الشركة</h4><ul>
        <li><a href="about.html">عن PACT</a></li>
        <li><a href="how-we-work.html">كيف نعمل</a></li>
        <li><a href="insights.html">الرؤى القانونية</a></li>
        <li><a href="contact.html">تواصل معنا</a></li>
      </ul></div>
      <div class="foot__col foot__contact"><h4>تواصل</h4>
        <div><span class="lbl">الموقع</span>pactadvisory.com</div>
        <div><span class="lbl">البريد الإلكتروني</span>[ يُضاف بعد الاعتماد ]</div>
        <div><span class="lbl">لينكدإن</span><a href="#">الحساب الرسمي</a></div>
      </div>
    </div>
    <div class="foot__bottom">
      <span>© 2026 PACT — جميع الحقوق محفوظة.</span>
      <div class="foot__legal"><a href="#">سياسة الخصوصية</a><a href="#">الشروط والأحكام</a><a href="#">إخلاء المسؤولية المهني</a></div>
    </div>
    <p class="foot__note">تنبيه مهني: المحتوى في هذا الموقع تعريفي وتسويقي، ولا يشكّل رأياً قانونياً أو وعداً بنتيجة أو نطاقاً تعاقدياً. يُحدَّد نطاق كل مهمة وحدودها والتزامات الأطراف بموجب اتفاق مكتوب وترتيبات مهنية مناسبة.</p>
  </div>
</footer>'''

def page_hero(crumb_label, eyebrow, h1, lead):
    return f'''<section class="page-hero">
  <svg class="page-hero__arc" viewBox="0 0 560 400" aria-hidden="true"><path d="M20 380 C 180 80, 380 80, 540 380"/></svg>
  <svg class="page-hero__peak" viewBox="0 0 200 200" aria-hidden="true"><path d="M16 190 L100 14 L184 190" fill="none"/><polygon points="100,78 128,150 72,150"/></svg>
  <div class="page-hero__inner">
    <div class="crumb"><a href="index.html">الرئيسية</a><span class="sep">/</span><span>{crumb_label}</span></div>
    <span class="eyebrow reveal">{eyebrow}</span>
    <h1 class="reveal" data-d="1">{h1}</h1>
    <p class="page-hero__lead reveal" data-d="2">{lead}</p>
  </div>
</section>'''

META = '<meta charset="utf-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1" />'

def head(title, desc, css=None):
    styles = f"<style>\n{css}\n</style>" if css else '<link rel="stylesheet" href="assets/pact.css" />'
    return f'{META}\n<title>{title}</title>\n<meta name="description" content="{desc}" />\n{FONTS}\n{styles}'

def chrome(active, body):
    return f'{header(active)}\n\n{body}\n\n{FOOTER}'

def fragment(title, desc, active, body, css=None, js=None):
    """Artifact/dev fragment — no <html>/<head>/<body> skeleton."""
    script = f"<script>\n{js}\n</script>" if js else '<script src="assets/pact.js"></script>'
    return f'{head(title, desc, css)}\n\n{chrome(active, body)}\n\n{script}\n'

def full_document(title, desc, active, body, css, js):
    """Standalone, deployable document."""
    return (f'<!doctype html>\n<html dir="rtl" lang="ar">\n<head>\n{head(title, desc, css)}\n</head>\n'
            f'<body>\n{chrome(active, body)}\n<script>\n{js}\n</script>\n</body>\n</html>\n')

# ---------------------------------------------------------------- pages
PAGES = {}

# ---- legal-studies ----
PAGES["legal-studies.html"] = dict(
    title="الدراسات القانونية وتشخيص الوضع القانوني ￨ PACT",
    desc="دراسة قانونية منظمة لتشخيص وتقييم الوضع القانوني للمنشآت، وترتيب المخاطر وفجوات المعلومات وخطوات المعالجة المقترحة.",
    active="legal-studies.html",
    body=page_hero("الدراسات القانونية", "الخدمة الرئيسة",
        "تشخيص قانوني منظّم يحوّل الملفات المتفرقة إلى قرار واضح",
        "خدمة تشخيص وتقييم للوضع القانوني للمنشآت. نعتمد منهجية محددة لفحص وتحليل العقود والالتزامات النظامية والمنازعات والمطالبات والهيكل والملكية والسياسات، ثم نحوّلها إلى تقرير تنفيذي مرجعي يدعم الإدارة والمُموّلين والمستثمرين قبل القرارات المفصلية.")
    + '''
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">01</span><span class="eyebrow">ما الذي تجيب عنه الدراسة</span></div>
      <h2>أسئلة متّخذ القرار التي تجيب عنها الدراسة</h2>
    </div>
    <div class="rows">
      <div class="row row--num reveal"><div class="row__t" data-n="Q1"><h3>ما الصورة القانونية الفعلية للمنشأة؟</h3></div><p class="row__d">قراءة منظمة للوثائق والوقائع المتاحة، مع بيان واضح لفجوات المعلومات.</p></div>
      <div class="row row--num reveal"><div class="row__t" data-n="Q2"><h3>أين المسائل والمخاطر المهمة؟</h3></div><p class="row__d">ترتيب للمسائل بحسب أثرها وأولويتها والحاجة إلى المعالجة.</p></div>
      <div class="row row--num reveal"><div class="row__t" data-n="Q3"><h3>ما الذي يجب أن نفعله أولاً؟</h3></div><p class="row__d">خطوات معالجة مقترحة تتضمّن الإجراء والتوقيت والمسؤولية المناسبة للنقاش.</p></div>
      <div class="row row--num reveal"><div class="row__t" data-n="Q4"><h3>ما الذي يحتاج إلى اختصاص إضافي؟</h3></div><p class="row__d">تحديد المسائل التي تستدعي رأياً متخصصاً أو عملاً قانونياً لاحقاً.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <div class="sec-head" style="margin-block-end:2rem">
          <div class="sec-head__top"><span class="idx">02</span><span class="eyebrow">محاور الدراسة</span></div>
          <h2>نطاق مرن يُحدَّد بحسب القرار والتكليف</h2>
          <p class="lead">تُحدَّد محاور الدراسة بحسب القرار ونطاق التكليف. وقد تشمل المحاور التالية عندما تكون متصلة بالمنشأة أو بالقرار محل الدراسة.</p>
        </div>
        <div class="prose">
          <ul>
            <li><strong>العقود:</strong> فحص العقود الجوهرية والتزاماتها وحقوقها ومواعيدها.</li>
            <li><strong>الالتزامات النظامية:</strong> الوقوف على الالتزامات النظامية ذات الأثر على الوضع القانوني.</li>
            <li><strong>المنازعات والمطالبات:</strong> حصر المنازعات القائمة أو المحتملة والمطالبات المرتبطة.</li>
            <li><strong>الهيكل والملكية:</strong> قراءة هيكل المنشأة وملكيتها وترتيباتها الحوكمية.</li>
            <li><strong>السياسات والوثائق ذات الصلة:</strong> مراجعة السياسات والوثائق الداعمة للصورة القانونية.</li>
            <li><strong>الملكية الفكرية:</strong> عندما تكون متصلة بالمنشأة أو بالقرار محل الدراسة.</li>
          </ul>
        </div>
      </div>
      <aside class="split__aside reveal" data-d="1">
        <div class="toc-label">محاور الدراسة</div>
        <div class="toc">
          <a href="#"><span class="n">01</span> العقود</a>
          <a href="#"><span class="n">02</span> الالتزامات النظامية</a>
          <a href="#"><span class="n">03</span> المنازعات والمطالبات</a>
          <a href="#"><span class="n">04</span> الهيكل والملكية</a>
          <a href="#"><span class="n">05</span> السياسات والوثائق</a>
          <a href="#"><span class="n">06</span> الملكية الفكرية</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="problem">
      <div class="reveal">
        <div class="sec-head" style="margin-block-end:1.5rem">
          <div class="sec-head__top"><span class="idx">03</span><span class="eyebrow">مسار متخصص</span></div>
          <h2>العناية القانونية الواجبة ضمن الخدمة</h2>
        </div>
        <div class="prose">
          <p>العناية القانونية الواجبة ليست عنوان الخدمة الوحيد، بل هي مسار متخصص ضمن الدراسات القانونية. تُستخدم عندما تكون المنشأة أو المعاملة محلّ صفقة أو استثمار أو تمويل أو شراكة أو استحواذ، ويُحدَّد نطاقها وفق قرار العميل وترتيبات الصفقة والوثائق ذات الصلة.</p>
        </div>
      </div>
      <aside class="pullnote reveal" data-d="1">
        <span class="k">حدود الخدمة</span>
        <p>لا تمثّل الدراسة فحصاً مالياً أو ضريبياً أو تقييماً لقيمة المنشأة، ما لم يُدرَج ذلك صراحةً ضمن ترتيبات مستقلة مع مختصين مؤهلين.</p>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">04</span><span class="eyebrow">مخرجات الدراسة</span></div>
      <h2>أربعة مخرجات تنقلك من الفهم إلى الفعل</h2>
    </div>
    <div class="grid-2">
      <article class="card reveal"><div class="card__n">01</div><h3>تقرير تنفيذي مرجعي</h3><p>يعرض الصورة القانونية بلغة تساعد الإدارة والمُموّلين والمستثمرين على فهم المسائل والأثر والسياق الذي يستدعي قراراً.</p></article>
      <article class="card reveal" data-d="1"><div class="card__n">02</div><h3>خريطة مخاطر</h3><p>ترتّب المسائل بحسب أثرها وأولويتها، لتساعد على التمييز بين ما يتطلب إجراءً عاجلاً وما يحتاج إلى متابعة أو استيضاح.</p></article>
      <article class="card reveal"><div class="card__n">03</div><h3>فجوات المعلومات</h3><p>توضّح الوثائق أو الوقائع غير المتاحة، وما يلزم لاستكمال القراءة أو تعميقها ضمن نطاق لاحق.</p></article>
      <article class="card reveal" data-d="1"><div class="card__n">04</div><h3>خطوات معالجة مقترحة</h3><p>تربط التشخيص بخطوات عملية مرتّبة ومسؤوليات وتوقيتات مقترحة للنقاش والمتابعة.</p></article>
    </div>
  </div>
</section>
'''
    + closing("هل تحتاج إلى فهم أوضح للوضع القانوني لمنشأتك؟",
        "ابدأ بلقاء تمهيدي قصير نتعرّف فيه إلى القرار وسياق المنشأة ونطاق المعلومات المتوقّع، ثم نحدّد ما إذا كانت الدراسة مناسبة.",
        secondary=("corporate-contracts.html","استشارات العقود")))

# ---- corporate-contracts ----
PAGES["corporate-contracts.html"] = dict(
    title="استشارات عقود الشركات ￨ PACT",
    desc="دعم قانوني منظم لصياغة ومراجعة العقود وبناء حزم التعاقد وإدارة الالتزامات للشركات.",
    active="corporate-contracts.html",
    body=page_hero("استشارات العقود", "الخدمة الثانوية",
        "عقود أكثر وضوحاً. التزامات أكثر انضباطاً.",
        "نساعد الشركات على بناء تعاقدات عملية وواضحة، من خلال صياغة ومراجعة العقود وتنظيم النماذج والملحقات ومتابعة الالتزامات ذات الأولوية — ضمن نطاق محدد وقواعد استجابة واضحة.")
    + '''
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">01</span><span class="eyebrow">مجالات الدعم</span></div>
      <h2>دعم تعاقدي منظّم ضمن نطاق واضح</h2>
    </div>
    <div class="grid-2">
      <article class="card reveal"><div class="card__tag">A — Drafting & Review</div><h3>صياغة ومراجعة العقود</h3><p>إعداد أو مراجعة عقود تجارية واستشارية وتشغيلية محددة النطاق، مع ملاحظات تفاوضية واضحة عند الحاجة.</p></article>
      <article class="card reveal" data-d="1"><div class="card__tag">B — Contract Packs</div><h3>حزم التعاقد</h3><p>تصميم نماذج رئيسة وشروط وملحقات ومسارات اعتماد تساعد على اتساق التعاقد داخل الشركة.</p></article>
      <article class="card reveal"><div class="card__tag">C — Obligations</div><h3>إدارة الالتزامات</h3><p>تنظيم العقود الجوهرية والمواعيد والحقوق والالتزامات ذات الأولوية في صورة قابلة للمتابعة.</p></article>
      <article class="card reveal" data-d="1"><div class="card__tag">D — Retainer</div><h3>اشتراك استشاري للشركات</h3><p>دعم دوري وفق ساعات أو نطاق شهري وقواعد استجابة متفق عليها، يبقى مناسباً لحجم الاحتياج وقرار العميل.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <div class="sec-head" style="margin-block-end:1.5rem">
          <div class="sec-head__top"><span class="idx">02</span><span class="eyebrow">متى تكون مناسبة</span></div>
          <h2>متى تكون هذه الخدمة مناسبة؟</h2>
        </div>
        <div class="prose">
          <p>تكون استشارات العقود مناسبة عندما تحتاج الشركة إلى مراجعة عقد جوهري، أو بناء نموذج تعاقد متكرر، أو تنظيم حزمة عقود قبل توسّع أو تعاون جديد، أو تحويل الملاحظات الناتجة عن دراسة قانونية إلى مشروع معالجة محدد.</p>
          <p>لا تبدأ الخدمة كالتزام مفتوح؛ بل تُبنى من نطاق واضح ومخرجات وتوقيتات قابلة للقياس — لنبدأ من العقد أو الإجراء الذي يستهلك وقت فريقك.</p>
        </div>
      </div>
      <aside class="split__aside reveal" data-d="1">
        <div class="toc-label">مناسبة عند</div>
        <div class="toc">
          <a href="#"><span class="n">01</span> مراجعة عقد جوهري</a>
          <a href="#"><span class="n">02</span> بناء نموذج تعاقد متكرر</a>
          <a href="#"><span class="n">03</span> تنظيم حزمة عقود قبل توسّع</a>
          <a href="#"><span class="n">04</span> تحويل ملاحظات دراسة إلى معالجة</a>
        </div>
      </aside>
    </div>
  </div>
</section>
'''
    + closing("لنبدأ من العقد الذي يستهلك وقت فريقك",
        "تواصل مع PACT لمناقشة احتياجك التعاقدي وتحديد النطاق والمخرجات المناسبة.",
        primary=("contact.html","ناقش احتياجك التعاقدي"), secondary=("legal-studies.html","الدراسات القانونية")))

# ---- how-we-work ----
PAGES["how-we-work.html"] = dict(
    title="كيف نعمل ￨ PACT",
    desc="منهجية PACT في تنفيذ الدراسات القانونية واستشارات العقود بنطاق واضح وسرّية ومخرجات قابلة للاستخدام.",
    active="how-we-work.html",
    body=page_hero("كيف نعمل", "المنهجية",
        "منهجية محدّدة تحترم القرار والوثيقة",
        "كل مهمة لدى PACT تبدأ بتحديد القرار ولا تبدأ بتحميل الملفات. نعمل بمنهجية واضحة تحمي السرية وتضبط النطاق وتنقل المشروع من جمع المعلومات إلى تقرير تنفيذي مرجعي قابل للمراجعة والمتابعة.")
    + '''
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">01</span><span class="eyebrow">مراحل التنفيذ</span></div>
      <h2>مراحل تنفيذ الدراسة القانونية</h2>
    </div>
    <div class="timeline">
      <div class="tl reveal"><div class="tl__n">المرحلة 01</div><h3>تأهيل الفرصة</h3><p>نفهم العميل والقرار المقصود ومدى ملاءمة الخدمة.</p><span class="tl__out"><span class="dot"></span>المخرج: تأكيد ملاءمة أو اعتذار مهني</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 02</div><h3>تحديد النطاق</h3><p>نحدّد المحاور والوثائق والمقابلات والحدود والزمن.</p><span class="tl__out"><span class="dot"></span>المخرج: نطاق عمل وعرض واضح</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 03</div><h3>السرية وتعارض المصالح</h3><p>نستكمل الترتيبات المناسبة قبل تبادل المعلومات.</p><span class="tl__out"><span class="dot"></span>المخرج: إذن منضبط لبدء العمل</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 04</div><h3>الانطلاقة وجمع المعلومات</h3><p>نعقد اجتماعاً افتتاحياً وننظّم طلبات الوثائق ونقاط الاتصال.</p><span class="tl__out"><span class="dot"></span>المخرج: فهرس منظم للوثائق</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 05</div><h3>الفهرسة والتحليل</h3><p>نراجع الملفات والوقائع ونسجّل المسائل وفجوات المعلومات.</p><span class="tl__out"><span class="dot"></span>المخرج: سجل مسائل أولي</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 06</div><h3>مراجعة الجودة</h3><p>نرتّب المسائل الجوهرية ونتحقق من اتساق المخرج.</p><span class="tl__out"><span class="dot"></span>المخرج: خريطة مخاطر داخلية</span></div>
      <div class="tl reveal"><div class="tl__n">المرحلة 07</div><h3>التقرير والتسليم</h3><p>نصيغ التقرير التنفيذي المرجعي ونناقشه مع العميل.</p><span class="tl__out"><span class="dot"></span>المخرج: تقرير نهائي وخطوات معالجة</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="problem">
      <div class="reveal">
        <div class="sec-head" style="margin-block-end:1.5rem">
          <div class="sec-head__top"><span class="idx">02</span><span class="eyebrow">السرّية وإدارة المعلومات</span></div>
          <h2>السرّية جزء من الخدمة، لا خطوة لاحقة لها</h2>
        </div>
        <div class="prose">
          <p>نعالج السرية بوصفها جزءاً من الخدمة، لا خطوة لاحقة لها. لذلك ترتبط مشاركة الوثائق بترتيبات سرية مناسبة وفحص تعارض المصالح، وصلاحيات وصول محددة، ومسار واضح لإدارة الملفات والملاحظات.</p>
          <p>كما نوضّح حدود الدراسة والوثائق غير المتاحة والافتراضات التي تؤثر في القراءة — حتى تبقى الصورة أمينة قابلة للاعتماد عليها.</p>
        </div>
      </div>
      <aside class="pullnote reveal" data-d="1">
        <span class="k">قبل مشاركة أي ملف</span>
        <p>يرجى عدم إرسال وثائق سرية أو بيانات حساسة قبل استكمال ترتيبات السرية وتحديد المسار الآمن لمشاركة الوثائق.</p>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">03</span><span class="eyebrow">جودة المخرَج</span></div>
      <h2>متى يكون المخرَج جيداً؟</h2>
      <p class="lead">يكون المخرج جيداً عندما يجيب بوضوح عن أربعة أسئلة تنقل العميل من الملاحظة إلى القرار.</p>
    </div>
    <div class="principles">
      <div class="principle reveal"><h3>ما الذي نعرفه؟</h3><p>الصورة القانونية المسنَدة إلى الوثائق والوقائع المتاحة.</p></div>
      <div class="principle reveal" data-d="1"><h3>ما الذي لا نعرفه؟</h3><p>فجوات المعلومات والوثائق غير المتاحة بوضوح ودون ادّعاء.</p></div>
      <div class="principle reveal" data-d="2"><h3>ما يمثّل خطراً فعلياً؟</h3><p>تمييز المسائل ذات الأثر عن الملاحظات الأقل أهمية.</p></div>
      <div class="principle reveal" data-d="3"><h3>ما ينبغي فعله الآن؟</h3><p>خطوات معالجة مرتّبة وقابلة للمتابعة.</p></div>
    </div>
  </div>
</section>
'''
    + closing("هل لديك قرار أو ملف يحتاج إلى قراءة منظمة؟",
        "ابدأ بلقاء تمهيدي نحدّد فيه ملاءمة الخدمة والخطوة التالية المناسبة.",
        secondary=("legal-studies.html","الدراسات القانونية")))

# ---- about ----
PAGES["about.html"] = dict(
    title="عن PACT ￨ الدراسات القانونية للمنشآت",
    desc="تعرّف إلى PACT، شركة متخصصة في الدراسات القانونية وتشخيص وتقييم الوضع القانوني للمنشآت واستشارات عقود الشركات.",
    active="about.html",
    body=page_hero("عن PACT", "عن الشركة",
        "نبني رؤية قانونية يمكن العمل بها",
        "PACT شركة متخصصة في الدراسات القانونية وتشخيص وتقييم الوضع القانوني للمنشآت. نعتمد منهجية محددة لفحص وتحليل العقود والالتزامات النظامية والمنازعات والمطالبات والهيكل والملكية والسياسات، ونحوّلها إلى تقرير تنفيذي مرجعي يوضّح الصورة ويرتّب المخاطر ويحدّد فجوات المعلومات وخطوات المعالجة المقترحة.")
    + '''
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <div class="prose">
          <p class="lead-em" style="font-size:1.2rem;color:var(--ink)">نعمل مع الشركات والمُموّلين والمستثمرين عندما يصبح الفهم المنظّم للوضع القانوني أساساً لقرار مهم.</p>
          <p>الأثر القانوني لا يظهر في لحظة الوثيقة، بل في لحظة القرار الذي يستند إليها. لذلك نصمّم عملنا حول القرار: نحدّد ما يستدعي الدراسة، ونضبط النطاق، ونحوّل البيانات المتفرقة إلى قراءة عملية تخدم اتخاذ القرار.</p>
        </div>
      </div>
      <aside class="split__aside reveal" data-d="1">
        <div class="stats" style="grid-template-columns:1fr">
          <div class="stat"><div class="stat__k">04</div><div class="stat__l">مكاتب: لندن · دبي · الرياض · نيويورك</div></div>
          <div class="stat"><div class="stat__k">02</div><div class="stat__l">خطّا خدمة: الدراسات القانونية واستشارات العقود</div></div>
          <div class="stat"><div class="stat__k">01</div><div class="stat__l">وعد مركزي: رؤية قانونية واضحة قبل القرار</div></div>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">01</span><span class="eyebrow">مبادئنا</span></div>
      <h2>ما تعنيه مبادئنا في عملنا</h2>
    </div>
    <div class="principles">
      <div class="principle reveal"><h3>الدقّة قبل السرعة</h3><p>نضبط النطاق ونراجع المعلومات بعناية، ونصرّح بما هو متاح وما هو غير متاح.</p></div>
      <div class="principle reveal" data-d="1"><h3>الوضوح قبل التعقيد</h3><p>نترجم المسائل القانونية إلى أولويات ومخرجات تساعد على اتخاذ القرار.</p></div>
      <div class="principle reveal" data-d="2"><h3>السرّية كالتزام</h3><p>نتعامل مع وثائق العميل ومعلوماته ضمن ترتيبات مهنية وإجرائية واضحة.</p></div>
      <div class="principle reveal" data-d="3"><h3>العملية في كل مخرَج</h3><p>نربط التحليل بخطوات معالجة مقترحة ومسؤوليات متابعة للنقاش والتنفيذ.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="problem">
      <div class="reveal">
        <div class="sec-head" style="margin-block-end:1.5rem">
          <div class="sec-head__top"><span class="idx">02</span><span class="eyebrow">حدود واضحة</span></div>
          <h2>ما لا ندّعيه</h2>
        </div>
        <div class="prose">
          <p>لا تضمن PACT نجاح تمويل أو بيع أو صفقة، ولا تقدّم الدراسات القانونية بوصفها بديلاً عن الفحص المالي أو الضريبي أو التجاري.</p>
          <p>يحدّد نطاق كل مهمة بوضوح، وتُعالَج المسائل التي تحتاج إلى اختصاص إضافي ضمن الترتيبات المهنية المناسبة.</p>
        </div>
      </div>
      <aside class="pullnote reveal" data-d="1">
        <span class="k">التموضع</span>
        <p>الدراسات القانونية وتشخيص الوضع القانوني هي الخدمة الرئيسة، والعناية القانونية الواجبة مسار متخصص ضمنها، واستشارات العقود خدمة ثانوية مكمّلة.</p>
      </aside>
    </div>
  </div>
</section>
'''
    + closing("استكشف الخدمة التي تناسب قرارك",
        "تعرّف إلى الدراسات القانونية واستشارات العقود، أو ابدأ بلقاء تمهيدي مباشرة.",
        primary=("legal-studies.html","الدراسات القانونية"), secondary=("contact.html","اطلب لقاءً تمهيدياً")))

# ---- insights ----
ARTICLES = [
    ("diagnosis","تشخيص الوضع القانوني","ما الفرق بين وجود مستندات كثيرة وامتلاك صورة قانونية جاهزة للقرار؟","تعريف مشكلة التشتت القانوني، ولماذا لا تتحوّل كثرة المستندات تلقائياً إلى قرار."),
    ("diagnosis","تشخيص الوضع القانوني","خمس إشارات تدل على أن منشأتك تحتاج إلى دراسة قانونية منظمة","بناء الوعي قبل طلب الخدمة عبر إشارات عملية يمكن ملاحظتها."),
    ("diagnosis","تشخيص الوضع القانوني","كيف تستعد المنشأة لجمع الوثائق قبل الدراسة القانونية؟","قائمة تحضيرية عامة غير قانونية تنظّم الاستعداد للدراسة."),
    ("decision","القرار والمخاطر","خريطة المخاطر القانونية: كيف تساعد الإدارة على ترتيب الأولويات؟","شرح المخرج التنفيذي وكيف يحوّل المخاطر إلى أولويات قابلة للفعل."),
    ("decision","القرار والمخاطر","ما الذي ينبغي أن يتضمّنه سجل المسائل القانوني؟","توضيح قيمة التنظيم والمتابعة في سجل مسائل واضح."),
    ("contracts","العقود والالتزامات","متى تحتاج الشركة إلى مراجعة عقودها الجوهرية؟","ربط مراجعة العقود بلحظات النمو والتغيير في الشركة."),
    ("contracts","العقود والالتزامات","لماذا لا تكون مراجعة العقد مجرد تعديل صياغة؟","توضيح التفكير التجاري والالتزامات خلف مراجعة العقود."),
    ("diagnosis","تشخيص الوضع القانوني","ما الذي يجعل نطاق الدراسة القانونية واضحاً؟","تثقيف العميل حول حدود الخدمة وأهمية النطاق المكتوب."),
    ("diagnosis","تشخيص الوضع القانوني","كيف تتعامل المنشآت مع الوثائق غير المتاحة أثناء الدراسة؟","إدارة فجوات المعلومات دون ادّعاءات، وبشفافية مهنية."),
    ("dd","العناية الواجبة","قبل دخول شريك: أسئلة قانونية تستحق التنظيم","محتوى توعوي موجّه للمُموّلين والمنشآت قبل الشراكة."),
    ("dd","العناية الواجبة","متى تكون العناية القانونية الواجبة مناسبة لقرارك الاستثماري؟","شرح موقع المسار المتخصص ضمن الخدمة وسياق الصفقة."),
    ("dd","العناية الواجبة","السرّية وتعارض المصالح: لماذا يسبقان مشاركة الملفات؟","بناء الثقة وشرح المنهجية قبل تبادل أي وثيقة."),
]
def art_cards():
    out=[]
    for i,(cat,catlabel,title,angle) in enumerate(ARTICLES):
        d = f' data-d="{(i%3)+1}"' if i%3 else ''
        out.append(f'''<a class="art reveal"{d} data-art="{cat}" href="#">
        <div class="art__cat">{catlabel}</div>
        <h3>{title}</h3>
        <p>{angle}</p>
        <div class="art__meta"><span>رؤية قانونية</span><span class="go">اقرأ ←</span></div>
      </a>''')
    return "\n      ".join(out)

PAGES["insights.html"] = dict(
    title="رؤى قانونية للشركات ￨ PACT",
    desc="مقالات عملية حول الدراسات القانونية وتشخيص الوضع القانوني والعناية الواجبة والعقود والالتزامات للشركات.",
    active="insights.html",
    body=page_hero("الرؤى", "رؤى قانونية",
        "رؤى تساعد المنشآت على الاستعداد قبل القرار",
        "نشارك رؤى عملية حول تنظيم الملفات القانونية، وتشخيص الوضع القانوني للمنشآت، والاستعداد للصفقات، وبناء العقود وإدارة الالتزامات. هدفنا أن تكون المعرفة مدخلاً إلى سؤال أفضل وقرار أكثر وضوحاً — لا بديلاً عن دراسة مهنية تتناسب مع كل حالة.")
    + f'''
<section class="section section--plain">
  <div class="wrap">
    <div class="chips reveal" role="group" aria-label="تصنيفات الرؤى">
      <button class="chip-btn" data-cat="all" aria-pressed="true">الكل</button>
      <button class="chip-btn" data-cat="diagnosis" aria-pressed="false">تشخيص الوضع القانوني</button>
      <button class="chip-btn" data-cat="dd" aria-pressed="false">العناية الواجبة</button>
      <button class="chip-btn" data-cat="contracts" aria-pressed="false">العقود والالتزامات</button>
      <button class="chip-btn" data-cat="decision" aria-pressed="false">القرار والمخاطر</button>
    </div>
    <div class="arts">
      {art_cards()}
    </div>
  </div>
</section>
'''
    + closing("تصلك رؤى PACT قبل القرار",
        "ابدأ بلقاء تمهيدي لمناقشة القرار الذي أمامك، أو تعرّف إلى خدماتنا.",
        secondary=("legal-studies.html","الدراسات القانونية")))

# ---- contact ----
PAGES["contact.html"] = dict(
    title="تواصل مع PACT",
    desc="اطلب لقاءً تمهيدياً مع PACT لمناقشة الدراسات القانونية أو العناية القانونية الواجبة للصفقات أو احتياجات عقود الشركات.",
    active="contact.html",
    body=page_hero("تواصل معنا", "تواصل",
        "لنبدأ من القرار الذي أمامك",
        "إذا كانت منشأتك تستعد لتوسّع أو شراكة أو استثمار أو ترتيب قانوني داخلي، أو كنت تحتاج إلى دعم منظم في العقود — فابدأ بلقاء تمهيدي. يساعدنا اللقاء على فهم السياق والقرار ونطاق المعلومات الأولي، وتحديد مدى ملاءمة الخدمة وخطوتها التالية.")
    + '''
<section class="section section--plain">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-aside reveal">
        <h2>اطلب لقاءً تمهيدياً</h2>
        <p>نتعرّف في اللقاء إلى القرار وسياق المنشأة ونطاق المعلومات المتوقّع، ثم نحدّد ما إذا كانت الدراسة مناسبة وما يلزم من نطاق وسرّية وترتيبات مهنية قبل البدء.</p>
        <div class="contact-info">
          <div class="item"><span class="lbl">الموقع</span><span class="val">pactadvisory.com</span></div>
          <div class="item"><span class="lbl">البريد الإلكتروني</span><span class="val">[ يُضاف بعد الاعتماد ]</span></div>
          <div class="item"><span class="lbl">لينكدإن</span><span class="val">الحساب الرسمي</span></div>
          <div class="item"><span class="lbl">ساعات الاستجابة</span><span class="val">[ تُضاف أيام وساعات العمل ]</span></div>
        </div>
        <div class="offices-line"><span>LONDON</span><span class="dot">·</span><span>DUBAI</span><span class="dot">·</span><span>RIYADH</span><span class="dot">·</span><span>NEW YORK</span></div>
      </div>

      <form class="form reveal" data-d="1" id="contactForm" novalidate>
        <div class="form__note"><b>ملاحظة قبل النموذج:</b> يرجى عدم إرسال وثائق سرية أو بيانات شخصية حساسة عبر النموذج. بعد تقييم أولي للطلب، ننسّق ترتيبات السرية والطريقة المناسبة لمشاركة المعلومات.</div>

        <div class="field-row">
          <div class="field"><label for="name">الاسم الكامل <span class="req">*</span></label><input id="name" name="name" type="text" autocomplete="name" required /></div>
          <div class="field"><label for="company">الشركة أو جهة العمل <span class="req">*</span></label><input id="company" name="company" type="text" autocomplete="organization" required /></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="role">المسمى الوظيفي</label><input id="role" name="role" type="text" autocomplete="organization-title" /></div>
          <div class="field"><label for="email">البريد الإلكتروني المهني <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required /></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="phone">رقم الهاتف</label><input id="phone" name="phone" type="tel" autocomplete="tel" /></div>
          <div class="field"><label for="interest">مجال الاهتمام <span class="req">*</span></label>
            <select id="interest" name="interest" required>
              <option value="" disabled selected>اختر مجال الاهتمام</option>
              <option>الدراسات القانونية / تشخيص الوضع القانوني</option>
              <option>العناية القانونية الواجبة لصفقة</option>
              <option>استشارات عقود الشركات</option>
              <option>استفسار عام</option>
            </select>
          </div>
        </div>
        <div class="field"><label for="context">سياق مختصر</label>
          <span class="hint">ما القرار أو التحدي الذي ترغب في مناقشته؟ يرجى عدم إدراج معلومات سرية أو وثائق.</span>
          <textarea id="context" name="context" rows="4"></textarea>
        </div>
        <div class="check">
          <input id="consent" name="consent" type="checkbox" required />
          <label for="consent">أوافق على معالجة بياناتي لغرض التواصل بشأن طلبي، وفق <a href="#">سياسة الخصوصية</a>.</label>
        </div>
        <button type="submit" class="btn btn--solid btn--block">أرسل الطلب <span class="ar">←</span></button>
        <div class="form__msg" id="formMsg" role="status" aria-live="polite"></div>
      </form>
    </div>
  </div>
</section>
''')

# ---- index ----
HOME_HERO = '''<section class="hero">
  <div class="hero__cols" aria-hidden="true">
    <svg preserveAspectRatio="xMaxYMid slice" viewBox="0 0 520 600">
      <line x1="60" y1="0" x2="60" y2="600"/><line x1="160" y1="0" x2="160" y2="600"/>
      <line x1="260" y1="0" x2="260" y2="600"/><line x1="360" y1="0" x2="360" y2="600"/><line x1="460" y1="0" x2="460" y2="600"/>
    </svg>
  </div>
  <svg class="hero__arc" viewBox="0 0 720 520" aria-hidden="true"><path d="M20 500 C 230 90, 490 90, 700 500"/><path d="M120 500 C 280 220, 440 220, 600 500" opacity=".55"/></svg>
  <svg class="hero__peak" viewBox="0 0 200 200" aria-hidden="true"><path d="M16 190 L100 14 L184 190" fill="none"/><polygon points="100,78 128,150 72,150"/></svg>
  <div class="hero__inner">
    <span class="eyebrow reveal">رؤية قانونية · أثر تجاري</span>
    <h1 class="reveal" data-d="1">رؤية قانونية واضحة قبل القرارات المفصلية</h1>
    <p class="hero__lead reveal" data-d="2">شركة متخصصة في الدراسات القانونية وتشخيص وتقييم الوضع القانوني للمنشآت. نحوّل الوثائق والبيانات القانونية المتفرقة إلى تقرير تنفيذي مرجعي يوضّح الصورة، ويرتب المخاطر بحسب أثرها وأولويتها، ويحدد فجوات المعلومات وخطوات المعالجة المقترحة.</p>
    <div class="hero__cta reveal" data-d="3">
      <a href="contact.html" class="btn btn--onbrand">اطلب لقاءً تمهيدياً <span class="ar">←</span></a>
      <a href="legal-studies.html" class="btn btn--onbrand-ghost">تعرّف إلى الدراسات القانونية</a>
    </div>
    <div class="hero__trust reveal" data-d="3">
      <b>الدراسات القانونية</b><span class="dot"></span><b>تشخيص الوضع القانوني</b><span class="dot"></span><b>العناية القانونية الواجبة</b>
    </div>
  </div>
</section>

<section class="pillars">
  <div class="pillars__inner">
    <div class="pillar reveal"><h3>الاستشارة القانونية</h3><p>مشورة استراتيجية للقرارات الحاسمة، ضمن نطاق واضح ولغة تنفيذية.</p></div>
    <div class="pillar reveal" data-d="1"><h3>العناية الواجبة</h3><p>تحليل دقيق ونتائج مسنَدة تدعم الصفقة من الفهم إلى القرار.</p></div>
    <div class="pillar reveal" data-d="2"><h3>الصفقات</h3><p>دعم منظّم للصفقات من ترتيب الهيكل حتى الإغلاق بثقة.</p></div>
  </div>
</section>'''

HOME_SECTIONS = '''<section class="section" id="problem">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">01</span><span class="eyebrow">المشكلة التي نحلها</span></div>
      <h2>وجود الوثائق لا يعني وضوح الصورة القانونية</h2>
    </div>
    <div class="problem">
      <div class="reveal">
        <p class="lead-em">قد تكون لدى المنشأة عقودٌ والتزامات وقرارات ومراسلات ومطالبات نظامية متعددة — لكنها لا تتجمع تلقائياً في صورة يمكن للإدارة أو المُموِّل أو المستثمر الاعتماد عليها عند اتخاذ قرار مهم.</p>
        <p style="margin-block-start:1.3em;color:var(--ink-soft)">وعندما تبقى البيانات القانونية موزّعة وغير مرتّبة، قد تتأخر القرارات أو تُبنى على معلومات غير مكتملة. الأثر لا يظهر في لحظة الوثيقة، بل في لحظة القرار الذي يستند إليها.</p>
      </div>
      <aside class="pullnote reveal" data-d="1">
        <span class="k">دور PACT</span>
        <p>ننظّم هذه الصورة ونحوّلها إلى قراءة قانونية عملية توضّح المسائل والأولويات وفجوات المعلومات ومسار المعالجة المقترح — لتكون أساساً موثوقاً للقرار.</p>
      </aside>
    </div>
  </div>
</section>

<section class="section" id="when">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">02</span><span class="eyebrow">متى نساعدك</span></div>
      <h2>في اللحظات التي تحتاج فيها إلى صورة قانونية أوضح</h2>
    </div>
    <div class="rows">
      <div class="row reveal"><div class="row__t"><h3>التوسّع أو تغيّر النشاط</h3></div><p class="row__d">افهم الالتزامات والمسائل التي تستحق ترتيباً ومعالجة قبل التنفيذ.</p></div>
      <div class="row reveal"><div class="row__t"><h3>دخول شريك أو مستثمر</h3></div><p class="row__d">جهّز صورة قانونية واضحة للحوار والشفافية والفحص المتبادل.</p></div>
      <div class="row reveal"><div class="row__t"><h3>صفقة تمويل أو استحواذ</h3></div><p class="row__d">عرّف مسار العناية القانونية الواجبة المناسب لسياق الصفقة ونطاقها.</p></div>
      <div class="row reveal"><div class="row__t"><h3>تغيير إداري أو إعادة ترتيب</h3></div><p class="row__d">كوّن رؤية مشتركة للوضع القانوني والأولويات والمسؤوليات.</p></div>
      <div class="row reveal"><div class="row__t"><h3>تراكم العقود أو المطالبات</h3></div><p class="row__d">انتقل من ردّ الفعل إلى خطة معالجة مرتّبة وقابلة للمتابعة.</p></div>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">03</span><span class="eyebrow">خدماتنا</span></div>
      <h2>خدمات مصمّمة للفهم والمعالجة والقرار</h2>
      <p class="lead">خدمة رئيسة تُحوّل الوضع القانوني إلى قراءة واضحة، ومسار متخصص للعناية الواجبة عند ارتباط الدراسة بصفقة، إضافة إلى استشارات العقود.</p>
    </div>
    <div class="services">
      <article class="card card--primary reveal">
        <span class="chip">الخدمة الرئيسة</span>
        <div class="card__tag">01 — Legal Studies</div>
        <h3>الدراسات القانونية وتشخيص الوضع القانوني</h3>
        <p>دراسة منظّمة للمنشأة ضمن نطاق فحص محدّد: العقود والالتزامات النظامية والمنازعات والمطالبات والهيكل والملكية والسياسات والوثائق ذات الصلة. ويشمل ذلك العناية القانونية الواجبة كمسار متخصص عند ارتباط الدراسة بصفقة أو تمويل أو استحواذ.</p>
        <a href="legal-studies.html" class="card__link">اكتشف الخدمة الرئيسة <span class="ar">←</span></a>
      </article>
      <article class="card reveal" data-d="1">
        <div class="card__tag">02 — Corporate Contracts</div>
        <h3>استشارات عقود الشركات</h3>
        <p>نساعد الشركات على صياغة ومراجعة عقودها وتنظيم نماذجها وملحقاتها ومتابعة التزاماتها ذات الأولوية ضمن نطاق واضح وقواعد استجابة محددة — لتبقى التعاقدات عملية ومنضبطة.</p>
        <a href="corporate-contracts.html" class="card__link">استكشف استشارات العقود <span class="ar">←</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section" id="how">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">04</span><span class="eyebrow">كيف نعمل</span></div>
      <h2>منهجية محدّدة من البداية إلى جلسة القرار</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="step__n">01</div><h3>نفهم القرار</h3><p>نبدأ بتأهيل الاحتياج وفهم القرار الذي يستدعي الدراسة ومدى ملاءمة الخدمة.</p></div>
      <div class="step reveal" data-d="1"><div class="step__n">02</div><h3>نحدّد النطاق</h3><p>نحدّد محاور الفحص والوثائق والمقابلات والحدود والزمن قبل بدء العمل.</p></div>
      <div class="step reveal" data-d="2"><div class="step__n">03</div><h3>ننظّم ونحلّل</h3><p>نجمع المعلومات بطريقة منضبطة، ونفهرسها، ونطبّق معايير التحليل المناسبة.</p></div>
      <div class="step reveal" data-d="3"><div class="step__n">04</div><h3>نُسلّم وخريطة الأولويات</h3><p>نقدّم تقريراً تنفيذياً مرجعياً وخريطة مخاطر وخطوات معالجة مقترحة.</p></div>
    </div>
    <div style="margin-block-start:2.7rem" class="reveal"><a href="how-we-work.html" class="btn btn--ghost">تعرّف إلى منهجية العمل <span class="ar">←</span></a></div>
  </div>
</section>

<section class="section" id="why">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="sec-head__top"><span class="idx">05</span><span class="eyebrow">لماذا PACT</span></div>
      <h2>لأن المخرَج يجب أن يساعدك على الفعل</h2>
      <p class="lead">لا نقيس جودة العمل بكثرة الملاحظات، بل بقدرتك على معرفة ما تعرفه، وما لا تعرفه، وما يمثّل خطراً فعلياً، وما ينبغي فعله الآن.</p>
    </div>
    <div class="principles">
      <div class="principle reveal"><h3>الدقّة</h3><p>نعمل ضمن نطاق مكتوب، ونوضّح الافتراضات والفجوات دون مبالغة في الوعود.</p></div>
      <div class="principle reveal" data-d="1"><h3>الوضوح</h3><p>نحوّل التعقيد إلى رؤية عملية تساعد على ترتيب الأولويات.</p></div>
      <div class="principle reveal" data-d="2"><h3>السرّية</h3><p>نحترم حساسية الوثائق والمعلومات، ونعالجها ضمن ترتيبات مهنية واضحة.</p></div>
      <div class="principle reveal" data-d="3"><h3>العملية</h3><p>نقدّم خطوات معالجة مقترحة ومساراً واضحاً للمتابعة والتنفيذ.</p></div>
    </div>
  </div>
</section>

<section class="section section--tight" id="insights">
  <div class="wrap">
    <div class="insights-head">
      <div class="sec-head reveal" style="margin:0">
        <div class="sec-head__top"><span class="idx">06</span><span class="eyebrow">رؤى قانونية</span></div>
        <h2>رؤى تساعد المنشآت على الاستعداد قبل القرار</h2>
      </div>
      <a href="insights.html" class="btn btn--ghost reveal" data-d="1">اقرأ أحدث الرؤى <span class="ar">←</span></a>
    </div>
    <div class="ins-list">
      <a href="insights.html" class="ins reveal"><span class="ins__n">01</span><span class="ins__t">ما الفرق بين وجود مستندات كثيرة وامتلاك صورة قانونية جاهزة للقرار؟</span><span class="ins__cat">تشخيص الوضع القانوني</span><span class="ins__go">←</span></a>
      <a href="insights.html" class="ins reveal" data-d="1"><span class="ins__n">02</span><span class="ins__t">خمس إشارات تدل على أن منشأتك تحتاج إلى دراسة قانونية منظمة</span><span class="ins__cat">تشخيص الوضع القانوني</span><span class="ins__go">←</span></a>
      <a href="insights.html" class="ins reveal" data-d="2"><span class="ins__n">03</span><span class="ins__t">متى تكون العناية القانونية الواجبة مناسبة لقرارك الاستثماري؟</span><span class="ins__cat">العناية الواجبة</span><span class="ins__go">←</span></a>
    </div>
  </div>
</section>'''

PAGES["index.html"] = dict(
    title="PACT ARC",
    desc="PACT — استشارات قانونية وعناية واجبة للمنشآت. رؤية قانونية. أثر تجاري.",
    active="index.html",
    body=HOME_HERO + "\n\n" + HOME_SECTIONS + "\n\n" + closing(
        "هل تحتاج إلى صورة قانونية أوضح؟",
        "ابدأ لقاءً تمهيدياً مع PACT لتحديد القرار الذي أمامك، ونطاق الدراسة المناسب، والمعلومات اللازمة للانطلاق.",
        secondary=("legal-studies.html","استكشف خدماتنا")))

# ---------------------------------------------------------------- write
def build():
    css = (ASSETS / "pact.css").read_text(encoding="utf-8")
    js = (ASSETS / "pact.js").read_text(encoding="utf-8")
    dist = ROOT / "dist"; dist.mkdir(exist_ok=True)
    for fname, cfg in PAGES.items():
        t, d, a, b = cfg["title"], cfg["desc"], cfg["active"], cfg["body"]
        # 1) repo source: fragment linking external assets
        (ROOT / fname).write_text(fragment(t, d, a, b), encoding="utf-8")
        # 2) dist: standalone deployable document, assets inlined
        (dist / fname).write_text(full_document(t, d, a, b, css, js), encoding="utf-8")
        print("wrote", fname)
    print(f"built {len(PAGES)} pages -> ./ (source) and ./dist (standalone)")

def artifact_fragment(fname):
    """Return a self-contained fragment (inline css/js, no skeleton) for publishing."""
    css = (ASSETS / "pact.css").read_text(encoding="utf-8")
    js = (ASSETS / "pact.js").read_text(encoding="utf-8")
    cfg = PAGES[fname]
    return fragment(cfg["title"], cfg["desc"], cfg["active"], cfg["body"], css=css, js=js)

if __name__ == "__main__":
    build()
