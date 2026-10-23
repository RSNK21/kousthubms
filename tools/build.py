#!/usr/bin/env python3
"""Static site builder for kousthub.in

Run:  python3 tools/build.py
Writes the HTML pages into the repository root. Edit the content
in this file (or in tools/data.py) and run again. No dependencies.
"""
import os, re, json, html
from data import ACCOLADES, TIERS, CREDITS, GALLERY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://kousthub.in"


def has(path):
    return os.path.exists(os.path.join(ROOT, path))


def temple(name, fallback):
    """Use a downloaded temple / mural image if present, else a fallback."""
    p = "assets/img/temple/" + name
    return p if has(p) else fallback


# ---------------------------------------------------------------- icons
_icon_cache = {}


def icon(name, extra=""):
    if name not in _icon_cache:
        s = open(os.path.join(ROOT, "assets/icons", name + ".svg"), encoding="utf-8").read().strip()
        s = re.sub(r'\s(width|height)="[^"]*"', "", s)
        _icon_cache[name] = s
    return _icon_cache[name].replace("<svg ", '<svg class="ic%s" aria-hidden="true" focusable="false" fill="currentColor" ' % (" " + extra if extra else ""), 1)


# ---------------------------------------------------------------- nav
PAGES = [
    ("index.html", "Home", "ಮುಖಮಂಟಪ", "home"),
    ("about.html", "Journey", "ಜೀವನಪಥ", "person"),
    ("guru-parampara.html", "Guru Parampara", "ಗುರುಪರಂಪರೆ", "self_improvement"),
    ("accolades.html", "Accolades", "ಪುರಸ್ಕಾರ", "emoji_events"),
    ("stage.html", "Stage", "ವೇದಿಕೆ", "mic"),
    ("sadhana.html", "Sadhana", "ಸಾಧನೆ", "library_music"),
    ("gallery.html", "Gallery", "ಚಿತ್ರಶಾಲೆ", "photo_library"),
    ("contact.html", "Contact", "ಸಂಪರ್ಕ", "mail"),
]
TIER_COLORS = ["var(--terracotta)", "var(--kumkuma-700)", "var(--terracotta-700)", "#9a6a12", "var(--leaf)", "var(--neeli-900)", "var(--kumkuma)", "var(--terracotta-900)"]

FONTS = ("https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400..900;1,400..700"
         "&family=Alegreya+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400"
         "&family=Benne&family=EB+Garamond:ital,wght@0,400..800;1,400..800"
         "&family=Playfair+Display:ital,wght@0,400..900;1,400..700"
         "&family=Smooch+Sans:wght@300..800&family=Tiro+Kannada:ital@0;1&display=swap")


def head(title, desc, page, og_img="assets/img/photos/tambura-portrait.jpg"):
    url = SITE + "/" + ("" if page == "index.html" else page)
    full_title = title if page == "index.html" else f"{title} | Kousthubh M S"
    ld = ""
    if page == "index.html":
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Person", "name": "Kousthubh M S",
            "alternateName": "ಕೌಸ್ತುಭ್ ಎಂ. ಎಸ್.", "jobTitle": "Karnataka Classical Vocalist",
            "url": SITE, "image": SITE + "/assets/img/photos/tambura-portrait.jpg",
            "birthPlace": "Mysuru, Karnataka", "email": "mailto:kousthubms@gmail.com",
            "alumniOf": ["The National Institute of Engineering, Mysuru", "Rasarishi Institution (Hampi Kannada University)"],
        }, ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#B5543A">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def topbar(page):
    items = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{en}<span lang="kn">{kn}</span></a></li>'
        for href, en, kn, ic in PAGES)
    tiers = ""
    n = len(PAGES)
    # top of the gopura is the last page; the doorway is Home
    for i, (href, en, kn, ic) in enumerate(reversed(PAGES)):
        idx = i + 1
        tiers += (f'<li style="--i:{idx}"><a class="tier" style="--tc:{TIER_COLORS[(n - 1 - i) % len(TIER_COLORS)]}" href="{href}"'
                  f'{" aria-current=\"page\"" if href == page else ""}><span class="en">{en}</span><span class="knl" lang="kn">{kn}</span></a></li>')
    return f"""<header class="topbar">
  <div class="wrap inner">
    <a class="brand" href="index.html" aria-label="Kousthubh M S, home">
      <img src="assets/img/ornament/hamsa.webp" alt="" width="52" height="33">
      <span class="nm">Kousthubh M S<small lang="kn">ಕೌಸ್ತುಭ್ ಎಂ. ಎಸ್.</small></span>
    </a>
    <nav class="mainnav" aria-label="Main"><ul>{items}</ul></nav>
    <button class="gopura-btn" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="gopura">{icon("temple_hindu")}<span class="lbl">Gopura</span><span class="sr">Open site menu</span></button>
  </div>
</header>
<div class="gopura" id="gopura" role="dialog" aria-modal="true" aria-label="Site menu shaped as a gopura" aria-hidden="true">
  <div class="sky"></div>
  <button class="icon-btn close" type="button" aria-label="Close menu">{icon("close")}</button>
  <nav aria-label="Gopura">
    <div class="kalasha" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="shala" aria-hidden="true"></div>
    <ol>{tiers}</ol>
    <div class="dvara"><a href="index.html" aria-label="Enter through the doorway: home">Mahadvara</a></div>
    <p class="hint">Climb the gopura. Each tier is a page.</p>
  </nav>
</div>
"""


def footer():
    links = "".join(f'<li><a href="{h}">{en} <span lang="kn" class="kn">· {kn}</span></a></li>' for h, en, kn, ic in PAGES)
    return f"""<footer class="site-foot">
  <div class="plinth-cap"></div>
  <div class="plinth" role="img" aria-label="Carved elephant frieze, the base course of a Karnataka temple"></div>
  <div class="wrap">
    <div class="cols">
      <div>
        <p class="brandline">Vidwan Kousthubh M S<small lang="kn">ವಿದ್ವಾನ್ ಕೌಸ್ತುಭ್ ಎಂ. ಎಸ್.</small></p>
        <p style="font-family:var(--f-ui);font-size:.98rem;color:var(--sand-300)">Karnataka Classical Vocalist, Mysuru.<br>Akashavani (All India Radio, Prasar Bharati): B High Grade Artist.</p>
      </div>
      <div><h4>Pages</h4><ul>{links}</ul></div>
      <div class="contact-mini">
        <h4>Reach out</h4>
        <ul>
          <li><a href="mailto:kousthubms@gmail.com">{icon("mail")} kousthubms@gmail.com</a></li>
          <li><a href="tel:+919739728057">{icon("call")} +91 97397 28057</a></li>
          <li><a href="tel:+919380622058">{icon("call")} +91 93806 22058</a></li>
          <li>{icon("location_on")} Srirampura, Mysuru 570023</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>2026</span> Kousthubh M S. All rights reserved.</span>
      <span><a href="credits.html">Image and font credits</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def page_hero(eyebrow, title, kn, lede, bg):
    return f"""<section class="page-hero">
  <div class="bg" style="background-image:url('{bg}')"></div>
  <div class="pillar l" aria-hidden="true"></div><div class="pillar r" aria-hidden="true"></div>
  <div class="wrap">
    <div class="torana" aria-hidden="true"></div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}<span class="kn-sub" lang="kn">{kn}</span></h1>
    <p class="lede">{lede}</p>
  </div>
</section>
<div class="band-strip" aria-hidden="true"></div>
"""


def write(name, body):
    out = os.path.join(ROOT, name)
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)


VS = "assets/img/temple/vidyashankara.jpg"
MURAL = temple("mysore-painting.jpg", "assets/img/ornament/frieze-figures.jpg")
MURAL2 = temple("vijayanagara-painting.jpg", MURAL)

# ================================================================ HOME
def home():
    p = "index.html"
    milestones = [
        ("2025", "Akashavani B High Grade", "Graded B High by All India Radio, Mysuru (Prasar Bharati).", "radio", "var(--neeli)"),
        ("2024", "M.A. in Music, A+ grade", "Rasarishi Institution, affiliated to Hampi Kannada University.", "school", "var(--kumkuma)"),
        ("2019", "First rank, Senior grade", "Karnataka Music (Vocal), KSEEB, Government of Karnataka. Distinction.", "workspace_premium", "var(--leaf)"),
        ("2019", "M.C.A. with Distinction", "The National Institute of Engineering, Mysuru (VTU, Belagavi).", "history_edu", "var(--terracotta)"),
    ]
    ms = "".join(f"""<article class="ms-card reveal" style="--c:{c}"><div class="ic-wrap">{icon(ic)}</div><div class="yr">{y}</div><h3>{t}</h3><p>{d}</p></article>""" for y, t, d, ic, c in milestones)

    cards = [
        ("about.html", "Journey", "ಜೀವನಪಥ", "From a grandmother's Gita to the concert stage.", "assets/img/thumbs/by-the-lake.jpg", "Kousthubh standing by a lake in Mysuru"),
        ("guru-parampara.html", "Guru Parampara", "ಗುರುಪರಂಪರೆ", "The teachers who lit each lamp along the way.", "assets/img/thumbs/with-guru-tambura.jpg", "Kousthubh on stage beside his guru"),
        ("accolades.html", "Accolades", "ಪುರಸ್ಕಾರ", "Fifty three honours, carved course by course.", "assets/img/thumbs/graduation-shawl.jpg", "Kousthubh wearing a ceremonial shawl"),
        ("stage.html", "Stage", "ವೇದಿಕೆ", "Concerts, radio, television and dance drama.", "assets/img/thumbs/concert-orange.jpg", "Kousthubh singing in concert"),
        ("sadhana.html", "Sadhana", "ಸಾಧನೆ", "Teaching, gamaka, Veda and Raga Iconification.", "assets/img/thumbs/traditional-attire.jpg", "Kousthubh in traditional attire"),
        ("gallery.html", "Gallery", "ಚಿತ್ರಶಾಲೆ", "Moments from the stage and beyond.", "assets/img/thumbs/vocal-support.jpg", "Two vocalists performing together"),
    ]
    pc = "".join(f"""<a class="p-card reveal" href="{h}"><div class="ph"><img src="{im}" alt="{alt}" loading="lazy" width="720" height="540"></div><div class="tx"><b>{t}</b><i lang="kn">{kn}</i><span>{d}</span></div><span class="go">{icon("arrow_forward")}</span></a>""" for h, t, kn, d, im, alt in cards)

    body = head("Kousthubh M S | Karnataka Classical Vocalist, Mysuru",
                "Vidwan Kousthubh M S is a Karnataka classical (Carnatic) vocalist from Mysuru, an Akashavani B High Grade artist and disciple of Sangeetha Vidwan Dr. R.S. Nandakumar.", p)
    body += topbar(p)
    body += f"""<main id="main">
<section class="home-hero">
  <div class="sky" aria-hidden="true"></div>
  <div class="vimana" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <div class="vidwan">Vidwan</div>
      <h1 class="wordmark" aria-label="Kousthubh M S">K<span class="o" aria-hidden="true"><img src="assets/img/ornament/tambura.webp" alt="" width="900" height="303"></span>usthubh<span class="ms">M S</span></h1>
      <p class="hero-kn" lang="kn">ಕೌಸ್ತುಭ್ ಎಂ. ಎಸ್.</p>
      <p class="hero-role">Karnataka classical vocalist from Mysuru. Disciple of Sangeetha Vidwan Dr. R.S. Nandakumar. Teacher, seeker and a voice shaped by bhakti.</p>
      <div class="air-badge"><span class="dot">{icon("radio")}</span><span><b>Akashavani B High Grade Artist</b><span>All India Radio, Prasar Bharati</span></span></div>
      <div class="hero-actions">
        <a class="btn" href="about.html">{icon("auto_stories")} Read his journey</a>
        <a class="btn outline" href="contact.html">{icon("mail")} Invite for a concert</a>
      </div>
    </div>
    <div class="shrine" aria-label="Portrait of Kousthubh with a tambura, framed like a temple doorway between two carved pillars">
      <div class="pl l" aria-hidden="true"></div>
      <div class="doorway">
        <div class="inner"><img src="assets/img/photos/tambura-portrait.jpg" alt="Kousthubh M S seated with a tambura, wearing a white kurta and a silk angavastra" width="651" height="1014" fetchpriority="high"></div>
        <span class="deepa l" aria-hidden="true"></span><span class="deepa r" aria-hidden="true"></span>
      </div>
      <div class="pl r" aria-hidden="true"></div>
    </div>
  </div>
  <div class="plinth-cap"></div>
  <div class="plinth" role="img" aria-label="Carved elephant frieze"></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Four carved milestones</span><h2>A voice built on discipline<span class="kn-sub" lang="kn">ಶಿಸ್ತಿನ ಮೇಲೆ ಕಟ್ಟಿದ ಕಂಠ</span></h2></div>
    <div class="milestones">{ms}</div>
  </div>
</section>

<div class="band-diamond" aria-hidden="true"></div>
<section class="section tint">
  <div class="wrap mandapa-grid">
    <div>
      <span class="eyebrow">The Rashi Mandapa</span>
      <h2>Twelve pillars, twelve swaras<span class="kn-sub" lang="kn">ಹನ್ನೆರಡು ಕಂಬ, ಹನ್ನೆರಡು ಸ್ವರಸ್ಥಾನ</span></h2>
      <p>The Vidyashankara temple at Sringeri holds twelve pillars, each carved for a sign of the zodiac. Through the year, the first rays of the sun fall on the pillar of the month. Karnataka music also rests on twelve: the twelve swarasthanas of the octave.</p>
      <p>Here the two meet. The glowing pillar is today's sign. Touch any pillar to hear its swara, tuned to a shruti of D, as a tambura would sound it.</p>
      <p class="rashi-readout" id="rashi-out" aria-live="polite">Touch any pillar to hear its swara.</p>
      <div class="drone-row">
        <button class="btn gold" type="button" data-drone aria-pressed="false">{icon("graphic_eq")} <span class="lbl">Play tambura drone</span></button>
        <a class="btn tonal" href="sadhana.html#ragas">{icon("music_note")} See ragas as shapes</a>
      </div>
    </div>
    <div class="ring" id="ring">
      <div class="floor" aria-hidden="true"></div>
      <div class="sunray" aria-hidden="true"></div>
      <div class="center" aria-hidden="true"><div><b lang="kn">ಸ</b><small>Shadja, the tonic</small></div></div>
    </div>
  </div>
</section>
<div class="band-diamond" aria-hidden="true"></div>

<section class="section">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Walk the prakaras</span><h2>Enter the mandapa<span class="kn-sub" lang="kn">ಮಂಟಪವನ್ನು ಪ್ರವೇಶಿಸಿ</span></h2><p class="lede">Each page is a corridor of the temple. Wander in any order.</p></div>
    <div class="prakara">{pc}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="mural reveal">
      <div class="bg" style="background-image:url('{MURAL}')"></div>
      <span class="attrib">Saint Tyagaraja, raga Dhanyasi</span>
      <p class="epigraph" lang="kn">ಸಂಗೀತ ಜ್ಞಾನಮು ಭಕ್ತಿ ವಿನಾ<br>ಸನ್ಮಾರ್ಗಮು ಗಲದೇ ಮನಸಾ</p>
      <p class="iast">saṅgīta jñānamu bhakti vinā sanmārgamu galadē manasā</p>
      <p style="max-width:56ch;color:var(--sand-200)">"O mind, can knowledge of music lead to the right path without devotion?" Kousthubh sings with this question close to heart: music, for him, is a path of bhakti and of all round cultural growth.</p>
      <a class="btn gold" href="stage.html">{icon("mic")} His music on stage</a>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ ABOUT
def about():
    p = "about.html"
    leaves = [
        ("Roots in Mysuru", "ಮೈಸೂರಿನ ಬೇರು",
         "<p>Kousthubh was born on 28 August 1996 in Mysuru, the cultural capital of Karnataka. His family traces its ancestry to the historic Halli Mysore. From his childhood, his parents, Sri H.N. Subbanna and Smt. H.N. Nagalakshmi, made sure he received an education that would grow his love for music, art and Indian values.</p><p>That gentle, rooted upbringing is still the first thing people notice about him: a calm and serene presence, on stage and off it.</p>",
         ("assets/img/photos/by-the-lake.jpg", "Kousthubh in a light kurta and mundu, standing by a lake under a monsoon sky", "Near home, under a Mysuru monsoon sky.")),
        ("A grandmother's voice", "ಅಜ್ಜಿಯ ಧ್ವನಿ",
         "<p>His first teacher was his grandmother, Smt. Kaveramma. From the age of five, he has recited what she taught him: the Srimad Bhagavadgita, Samskrutha shlokas and the Soundaryalahari. As a child he won more than twenty prizes at Bhagavadgita recital competitions across Mysuru.</p><p>He also studied the Vedas under Veda Vidwan H.S. Balakrishna. The clarity of text and pronunciation he learned here lives in every kriti he sings today.</p>",
         ("assets/img/photos/traditional-attire.jpg", "Kousthubh in a traditional white panche and uttariya with a gold border", "In traditional attire.")),
        ("Two disciplines, one mind", "ಎರಡು ಶಿಸ್ತು, ಒಂದೇ ಮನಸ್ಸು",
         "<p>He completed his foundational music training under Smt. Jyothi Shankar, and in 2019 secured a distinction and the <b>first rank</b> in the Board's Senior grade examination in Karnataka Music (Vocal), KSEEB, Government of Karnataka.</p><p>In the same year he earned his <b>M.C.A. with distinction</b> from The National Institute of Engineering, Mysuru (VTU, Belagavi). Logic and laya, code and kriti: he has never seen them as opposites.</p>",
         ("assets/img/photos/graduation-shawl.jpg", "Kousthubh smiling, wearing a cream kurta and a saffron ceremonial stole", "A day of honour.")),
        ("In the gurukula", "ಗುರುಕುಲದಲ್ಲಿ",
         "<p>In 2024 he completed his <b>Master of Music (M.A. in Music) with an A+ grade</b> at the Rasarishi Institution, affiliated to Hampi Kannada University, under the guidance of the eminent musician and musicologist, Sangeetha Vidwan Dr. R.S. Nandakumar.</p><p>He accompanies his guru in all his concerts, providing shruthi and vocal support, and continues to learn in the old and disciplined way of the Gurukula.</p>",
         ("assets/img/photos/with-guru-concert.jpg", "Kousthubh in a saffron kurta providing vocal support at a concert", "Providing vocal support on stage.")),
        ("A voice on the air", "ಆಕಾಶವಾಣಿಯ ಕಂಠ",
         "<p>Akashavani, All India Radio, first recognised him in 2015 with a first prize in folk music. In 2025, All India Radio Mysuru graded him a <b>B High Grade Artist</b> (Prasar Bharati).</p><p>His songs have been featured in the award winning All India Radio programme <i>Vachana Pada Vaidya</i>, and on SVBC television in <i>Nada Neerajanam</i>, Tirupati.</p>",
         ("assets/img/photos/at-the-mic-2.jpg", "Kousthubh singing into a microphone in a white kurta", "At the microphone.")),
        ("Teacher and seeker", "ಗುರು ಮತ್ತು ಸಾಧಕ",
         "<p>He is a prominent faculty member at <b>SaPa International</b>, where he teaches Carnatic music to many gifted students. He is now learning bhajans and philosophical compositions such as the <i>Adhyatma Geethavali</i> of the Adhyatma Prakashana Karyalaya of His Holiness Sri Sacchidanandendra Saraswathi Swami.</p><p>His current research looks at <b>Raga Iconification</b> and at the special compositions of Karnataka composers.</p>",
         None),
    ]
    lv = ""
    for i, (t, kn, txt, fig) in enumerate(leaves, 1):
        f = ""
        if fig:
            f = f'<figure><img src="{fig[0]}" alt="{fig[1]}" loading="lazy"><figcaption>{fig[2]}</figcaption></figure>'
        lv += f"""<article class="leaf reveal{'' if fig else ' nofig'}"><div class="num" aria-hidden="true">{i:02d}</div><div class="lines"><h3>{t}<span class="kn-sub" lang="kn">{kn}</span></h3>{txt}</div>{f}</article>"""
    facts = [
        ("Born", "28 August 1996, Mysuru", "var(--terracotta)"),
        ("Guru", "Sangeetha Vidwan Dr. R.S. Nandakumar", "var(--kumkuma)"),
        ("Radio grade", "Akashavani B High (2025)", "var(--neeli)"),
        ("Music degree", "M.A. Music, A+ (2024)", "var(--leaf)"),
        ("Engineering", "M.C.A., Distinction (2019)", "#9a6a12"),
        ("Teaches at", "SaPa International", "var(--terracotta-700)"),
    ]
    fc = "".join(f'<div class="fact" style="--c:{c}"><dt>{a}</dt><dd>{b}</dd></div>' for a, b, c in facts)
    body = head("Journey", "The life and training of Karnataka classical vocalist Kousthubh M S of Mysuru, told as leaves of a palm-leaf manuscript.", p, "assets/img/photos/by-the-lake.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Tala patra · the palm-leaf story", "His Journey", "ಜೀವನಪಥ", "Six leaves, strung on one thread. Read his story the way old manuscripts were read: one leaf at a time.", "assets/img/ornament/frieze-wall.jpg")}
<section class="section">
  <div class="wrap">
    <dl class="facts reveal" style="margin:0 0 48px">{fc}</dl>
    <div class="tala string">{lv}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="mural reveal">
      <div class="bg" style="background-image:url('{MURAL2}')"></div>
      <span class="attrib">His aspiration</span>
      <h2 style="color:var(--arishina-300);max-width:22ch">Music that helps a whole culture grow</h2>
      <p style="max-width:62ch;color:var(--sand-100)">Kousthubh is building his career with one wish: that his music should foster all round cultural and holistic development. People who hear him speak of the richness of his voice, his innate sense of proportion and the feeling he brings to every phrase. He hopes to be a vocalist admired as much for his adherence to Indian traditions and values as for his singing.</p>
      <a class="btn gold" href="guru-parampara.html">{icon("self_improvement")} Meet his teachers</a>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ GURU
def guru():
    p = "guru-parampara.html"
    gurus = [
        ("The first teacher", "Smt. Kaveramma", "ಶ್ರೀಮತಿ ಕಾವೇರಮ್ಮ", "Grandmother", "var(--kesari)",
         "From the age of five she taught him the Srimad Bhagavadgita, Samskrutha shlokas and the Soundaryalahari. Her teaching gave him the habit of clear diction and the love of the sacred word."),
        ("Veda", "Veda Vidwan H.S. Balakrishna", "ವೇದ ವಿದ್ವಾನ್ ಎಚ್. ಎಸ್. ಬಾಲಕೃಷ್ಣ", "Vedic studies", "var(--leaf)",
         "Under him Kousthubh studied the Vedas, learning svara, rhythm and the discipline of oral tradition."),
        ("Foundations of music", "Smt. Jyothi Shankar", "ಶ್ರೀಮತಿ ಜ್ಯೋತಿ ಶಂಕರ್", "Junior and Senior grades", "var(--neeli)",
         "His foundational music education was completed under her. It led to a first class in the Junior grade and the first rank in the Senior grade examination of the Government of Karnataka."),
        ("Guru", "Sangeetha Vidwan Dr. R.S. Nandakumar", "ಸಂಗೀತ ವಿದ್ವಾನ್ ಡಾ. ಆರ್. ಎಸ್. ನಂದಕುಮಾರ್", "Eminent musician and musicologist", "var(--kumkuma)",
         'India\'s eminent musician and musicologist. Under his guidance Kousthubh completed his M.A. in Music with an A+ grade (2024). He accompanies his guru in all his concerts, providing shruthi and vocal support, and continues to learn from him in the Gurukula way. <a href="https://rsnandakumar.in" target="_blank" rel="noopener">rsnandakumar.in ' + icon("open_in_new") + '</a>'),
        ("Philosophy in song", "Adhyatma Geethavali", "ಅಧ್ಯಾತ್ಮ ಗೀತಾವಳಿ", "Adhyatma Prakashana Karyalaya", "var(--terracotta)",
         "He is currently learning bhajans and philosophical compositions such as the Adhyatma Geethavali of the Adhyatma Prakashana Karyalaya of His Holiness Sri Sacchidanandendra Saraswathi Swami."),
    ]
    g = "".join(f"""<article class="guru reveal" style="--c:{c}"><div class="lamp" aria-hidden="true"></div><div class="card temple"><span class="role">{role}</span><h3>{name}</h3><span class="kn" lang="kn">{kn}</span><p style="margin:0 0 6px;font:600 .95rem var(--f-ui);color:var(--muted)">{sub}</p><p style="margin:0">{txt}</p></div></article>""" for role, name, kn, sub, c, txt in gurus)
    body = head("Guru Parampara", "The teachers of Kousthubh M S: his grandmother Smt. Kaveramma, Veda Vidwan H.S. Balakrishna, Smt. Jyothi Shankar and Sangeetha Vidwan Dr. R.S. Nandakumar.", p, "assets/img/photos/with-guru-tambura.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Deepa stambha · the lamp pillar", "Guru Parampara", "ಗುರುಪರಂಪರೆ", "A lamp is lit from a lamp. These are the teachers whose flames he carries.", "assets/img/ornament/pillar-hall.jpg")}
<section class="section">
  <div class="wrap guru-feature">
    <div class="arch-photo reveal"><img style="object-position:35% 70%" src="assets/img/photos/with-guru-tambura.jpg" alt="Kousthubh holding the tambura on stage while his guru sings into the microphone beside him" loading="lazy"></div>
    <div>
      <span class="eyebrow">The Gurukula way</span>
      <h2>Learning by living beside the guru<span class="kn-sub" lang="kn">ಗುರುವಿನ ಸನ್ನಿಧಿಯಲ್ಲಿ ಕಲಿಕೆ</span></h2>
      <p>In the Gurukula system a student does not only take lessons. He sits beside the guru on stage, holds the shruthi, sings along when needed, listens to every choice the guru makes and slowly absorbs a whole way of thinking about music.</p>
      <p>Kousthubh has chosen this old and disciplined path. Holding the tambura for his guru in concert after concert, he has learned what no classroom can teach: how a raga unfolds in front of a living audience.</p>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap" style="max-width:860px">
    <div class="section-head"><span class="eyebrow">Five flames</span><h2>His teachers<span class="kn-sub" lang="kn">ಗುರುಗಳು</span></h2></div>
    <div class="parampara">{g}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Shishya on stage</span><h2>Shruthi and vocal support<span class="kn-sub" lang="kn">ಶ್ರುತಿ ಮತ್ತು ಗಾಯನ ಸಹಕಾರ</span></h2></div>
    <div class="photo-duo">
      <figure class="reveal"><img class="tall" src="assets/img/photos/with-guru-concert.jpg" alt="Kousthubh in a saffron kurta providing vocal support behind the lead singer" loading="lazy"><figcaption>Vocal support in concert.</figcaption></figure>
      <figure class="reveal"><img src="assets/img/photos/srividya-nadavidya-stage.jpg" alt="A wide view of a concert stage with yellow drapes, accompanists and tamburas" loading="lazy"><figcaption>On stage at a lecture concert.</figcaption></figure>
      <figure class="reveal"><img src="assets/img/photos/vocal-support.jpg" alt="Two vocalists in white kurtas singing at microphones" loading="lazy"><figcaption>Singing together, voice beside voice.</figcaption></figure>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ ACCOLADES
PRIZE_COLOR = {"first": "var(--kumkuma)", "second": "var(--neeli)", "third": "var(--leaf)", "cert": "var(--terracotta)", "top": "var(--terracotta-900)", "feature": "var(--kesari)"}
PRIZE_ICON = {"first": "emoji_events", "second": "military_tech", "third": "military_tech", "cert": "workspace_premium", "top": "school", "feature": "mic"}


def accolades():
    p = "accolades.html"
    counts = {t["key"]: 0 for t in TIERS}
    for a in ACCOLADES:
        counts[a["cat"]] += 1
    total = len(ACCOLADES)
    firsts = sum(1 for a in ACCOLADES if a["kind"] == "first")
    gita = counts["gita"]
    chips = f'<button class="chip" type="button" data-f="all" aria-pressed="true">{icon("filter_list")} All <span class="count">{total}</span></button>'
    chips += "".join(f'<button class="chip" type="button" data-f="{t["key"]}" aria-pressed="false">{t["short"]} <span class="count">{counts[t["key"]]}</span></button>' for t in TIERS)
    bands = ""
    for t in TIERS:
        items = [a for a in ACCOLADES if a["cat"] == t["key"]]
        panels = ""
        for a in items:
            c = PRIZE_COLOR[a["kind"]]
            panels += f"""<div class="panel{' star' if a.get('star') else ''}" style="--c:{c}"><span class="prize">{icon(PRIZE_ICON[a['kind']])}{html.escape(a['prize'])}</span><span class="org">{html.escape(a['org'])}</span><span class="cat">{html.escape(a['what'])}</span>{f'<span class="date">{html.escape(a["date"])}</span>' if a.get('date') else ''}</div>"""
        bands += f"""<section class="tier-band" data-cat="{t['key']}" aria-label="{t['title']}"><header><h3>{t['title']}</h3><span class="kn" lang="kn">{t['kn']}</span><span class="motif">{t['motif']}</span></header><div class="panels">{panels}</div></section>"""
    stats = [
        (total, "honours, prizes and features", "var(--terracotta)"),
        (firsts, "first prizes", "var(--kumkuma)"),
        (gita, "Bhagavadgita recital honours, from 2004", "var(--leaf)"),
        ("A+", "M.A. Music, 2024", "var(--neeli)"),
    ]
    st = "".join(f'<div class="stat reveal" style="--c:{c}"><b>{n}</b><span>{l}</span></div>' for n, l, c in stats)
    body = head("Accolades", "Prizes, grades, honours and features earned by Karnataka classical vocalist Kousthubh M S, from childhood Bhagavadgita recitals to an Akashavani B High grade.", p, "assets/img/photos/graduation-shawl.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Bhitti · the temple wall", "Accolades", "ಪುರಸ್ಕಾರಗಳು", "A Karnataka temple wall is read from the ground up: elephants at the base for strength, then horses, scrolls and figures. His honours are carved the same way.", "assets/img/ornament/frieze-wall.jpg")}
<section class="section">
  <div class="wrap">
    <div class="stats">{st}</div>
    <div class="chips" id="acc-chips" role="group" aria-label="Filter by course">{chips}</div>
    <p style="font:500 .95rem var(--f-ui);color:var(--muted);margin:14px 0 24px">The foundation is at the bottom. Scroll down to reach the elephant course.</p>
    <div class="wall">{bands}<div class="wall-base" role="img" aria-label="Elephant frieze at the base of the wall"></div></div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ STAGE
def stage():
    p = "stage.html"
    bills = [
        ("tv", "SVBC TV · Tirupati", "Nada Neerajanam", "Featured as vocal accompaniment to his guru, Sangeetha Vidwan Dr. R.S. Nandakumar.", "var(--neeli)"),
        ("theater_comedy", "SVBC TV · Tirupati", "Narada in Narada Koravanji", "Lead role in the dance drama Narada Koravanji, telecast in Nada Neerajanam.", "var(--kumkuma)"),
        ("theater_comedy", "Bengaluru", "Yugala Bahula Mukula Festival", "Lead role in a prestigious dance drama presented by Sadhana Sangama Trust.", "var(--kumkuma)"),
        ("theater_comedy", "ISKCON · Mysuru", "Sri Krishna Janmashtami", "Lead role in the dance drama for the Janmashtami celebrations.", "var(--kumkuma)"),
        ("radio", "All India Radio · Mysuru", "Vachana Pada Vaidya", "His songs featured in this award winning programme, and at Desi Adda, Samskara Bharati and other venues.", "var(--neeli)"),
        ("temple_hindu", "Mysuru Dasara · 2015", "Grand festival concert", "Karnataka classical concert with his guru. Certificate of Excellence, 15 October 2015.", "var(--terracotta)"),
        ("school", "Kanchipuram · January 2017", "Tyagaraja Aradhana", "Invited by Kanchi Kamakoti Shankara University, Kanchipuram, to take part in its first Tyagaraja Aradhana celebrations.", "var(--leaf)"),
        ("record_voice_over", "Across Karnataka", "Vocal support in major concerts", "Shruthi and vocal support for Dr. R.S. Nandakumar in his concerts.", "var(--terracotta)"),
    ]
    b = "".join(f"""<article class="bill reveal" style="--c:{c}"><span class="where">{icon(ic)}{w}</span><h3>{t}</h3><p>{d}</p></article>""" for ic, w, t, d, c in bills)
    reps = [
        ("Karnataka Shastriya Sangeetha", "ಕರ್ನಾಟಕ ಶಾಸ್ತ್ರೀಯ ಸಂಗೀತ", "library_music", "linear-gradient(150deg,#8E3B24,#B5543A)"),
        ("Bhakti Sangeetha", "ಭಕ್ತಿ ಸಂಗೀತ", "spa", "linear-gradient(150deg,#B3132C,#EE7B1C)"),
        ("Janapada, folk song", "ಜಾನಪದ ಗೀತೆ", "diversity_3", "linear-gradient(150deg,#3d6420,#4E7A2B)"),
        ("Desha Bhakti, patriotic song", "ದೇಶಭಕ್ತಿ ಗೀತೆ", "light_mode", "linear-gradient(150deg,#183E5C,#2F7DB5)"),
        ("Gamaka vachana", "ಗಮಕ ವಾಚನ", "auto_stories", "linear-gradient(150deg,#7a560c,#E5A11A)"),
        ("Nritya nataka, dance drama", "ನೃತ್ಯ ನಾಟಕ", "theater_comedy", "linear-gradient(150deg,#5A2415,#8A0E21)"),
    ]
    r = "".join(f'<div class="rep reveal" style="background:{g}">{icon(ic)}<b>{t}</b><i lang="kn">{kn}</i></div>' for t, kn, ic, g in reps)
    body = head("Stage", "Concerts, television, radio and dance drama by Karnataka classical vocalist Kousthubh M S.", p, "assets/img/photos/concert-orange.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Ranga mantapa · the stage hall", "On Stage", "ವೇದಿಕೆ", "Classical kutcheris, radio and television, folk and devotional evenings, and lead roles in dance drama.", "assets/img/ornament/eave-kudu.jpg")}
<section class="section">
  <div class="wrap">
    <div class="photo-duo">
      <figure class="reveal"><img class="tall" src="assets/img/photos/concert-orange.jpg" alt="Kousthubh in a saffron kurta singing seated cross legged with an ensemble" loading="lazy"><figcaption>Singing with an ensemble.</figcaption></figure>
      <figure class="reveal"><img class="tall" src="assets/img/photos/with-dancer.jpg" alt="Kousthubh beside a Bharatanatyam dancer in full costume" loading="lazy"><figcaption>After a dance drama performance.</figcaption></figure>
      <figure class="reveal"><img class="tall" src="assets/img/photos/dance-drama-stage.jpg" alt="Kousthubh in a saffron kurta on stage with two dancers" loading="lazy" style="object-position:30% 50%"><figcaption>With fellow artists on stage.</figcaption></figure>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="curtain">
      <span class="eyebrow" style="color:var(--arishina-300)">Playbills</span>
      <h2>Stages he has sung on<span class="kn-sub" lang="kn" style="color:var(--sand-200)">ಹಾಡಿದ ವೇದಿಕೆಗಳು</span></h2>
      <div class="bills">{b}</div>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Repertoire</span><h2>Many streams, one voice<span class="kn-sub" lang="kn">ಹಲವು ಧಾರೆ, ಒಂದೇ ಕಂಠ</span></h2><p class="lede">He has performed concerts of devotional songs, patriotic songs and folk songs, alongside his classical training.</p></div>
    <div class="repertoire">{r}</div>
  </div>
</section>
<section class="section">
  <div class="wrap" style="text-align:center">
    <h2>Invite Kousthubh to sing<span class="kn-sub" lang="kn">ಕಾರ್ಯಕ್ರಮಕ್ಕೆ ಆಹ್ವಾನಿಸಿ</span></h2>
    <p class="lede" style="margin-inline:auto">Concerts, bhajan evenings, festivals, lecture demonstrations and dance drama music.</p>
    <a class="btn" href="contact.html">{icon("mail")} Send an enquiry</a>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ SADHANA
def sadhana():
    p = "sadhana.html"
    ragas = [("mayamalavagowla", "Mayamalavagowla"), ("shankarabharanam", "Shankarabharanam"), ("kalyani", "Kalyani"), ("kharaharapriya", "Kharaharapriya"), ("mohana", "Mohana"), ("hindola", "Hindola")]
    rb = "".join(f'<button class="chip" type="button" data-raga="{k}" aria-pressed="false">{n}</button>' for k, n in ragas)
    body = head("Sadhana", "Teaching at SaPa International, gamaka, Vedic learning and research into Raga Iconification by Kousthubh M S.", p, "assets/img/photos/traditional-attire.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Sadhana · daily practice", "Teaching and Research", "ಸಾಧನೆ", "Practice is never finished. He teaches, studies, recites and researches, all as one sadhana.", "assets/img/ornament/frieze-figures.jpg")}
<section class="section">
  <div class="wrap split">
    <div class="gold-frame reveal"><img src="assets/img/photos/at-the-mic.jpg" alt="Kousthubh singing at a microphone in a white kurta" loading="lazy"></div>
    <div>
      <span class="eyebrow">Teaching</span>
      <h2>Faculty, SaPa International<span class="kn-sub" lang="kn">ಸಪ ಇಂಟರ್‌ನ್ಯಾಷನಲ್</span></h2>
      <p>Kousthubh is a prominent faculty member at SaPa International, where he teaches Carnatic music to many aspiring and gifted students.</p>
      <p>He teaches the way he was taught: patiently, with attention to sahitya and pronunciation, to shruthi and to the shape of each phrase. For students who want to begin or deepen their study, he is glad to talk.</p>
      <a class="btn" href="contact.html">{icon("school")} Ask about lessons</a>
    </div>
  </div>
</section>
<div class="band-petal" aria-hidden="true"></div>
<section class="section tint" id="ragas">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Research</span><h2>Raga Iconification<span class="kn-sub" lang="kn">ರಾಗ ಪ್ರತಿಮೀಕರಣ</span></h2>
    <p class="lede">He is currently working on projects in Raga Iconification and on the special musical compositions of Karnataka composers. The sketch below is only a playful illustration, not the research itself: each raga drawn as a shape on the wheel of twelve swaras.</p></div>
    <div class="raga-lab">
      <svg class="raga-wheel" id="raga-wheel" viewBox="0 0 420 420" role="img" aria-label="Twelve swarasthanas arranged in a circle; the selected raga is drawn as a polygon joining its swaras"></svg>
      <div>
        <div class="raga-name" id="raga-name" aria-live="polite">Mayamalavagowla</div>
        <p class="raga-meta" id="raga-meta"></p>
        <div class="chips" role="group" aria-label="Choose a raga to draw and hear its arohana">{rb}</div>
        <p style="font:500 .95rem var(--f-ui);color:var(--muted);margin-top:14px">{icon("graphic_eq")} Tap a raga to hear its arohana, plucked like a tambura string.</p>
      </div>
    </div>
  </div>
</section>
<div class="band-petal" aria-hidden="true"></div>
<section class="section">
  <div class="wrap split r">
    <div class="gold-frame reveal"><img src="assets/img/photos/traditional-attire.jpg" alt="Kousthubh in traditional white panche and uttariya" loading="lazy" style="aspect-ratio:4/5;object-fit:cover"></div>
    <div>
      <span class="eyebrow">Gamaka</span>
      <h2>The art of the sung epic<span class="kn-sub" lang="kn">ಗಮಕ ಕಲೆ</span></h2>
      <p>Gamaka is Karnataka's own art of singing and explaining epic poetry. Kousthubh has passed all four examinations in gamaka with first class.</p>
      <div class="gamaka-steps" aria-label="Four gamaka examinations, each passed in first class">
        <span style="--c:var(--leaf)">Prathama</span><span style="--c:var(--neeli)">Pravesha</span><span style="--c:var(--terracotta)">Proudha</span><span style="--c:var(--kumkuma)">Kaajaana</span>
      </div>
      <h3 style="margin-top:28px">Veda, shloka and stotra</h3>
      <p>The Bhagavadgita, Samskrutha shlokas and the Soundaryalahari learned from his grandmother; the Vedas learned under Veda Vidwan H.S. Balakrishna; and today, the Adhyatma Geethavali of the Adhyatma Prakashana Karyalaya. Each one feeds his singing.</p>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ GALLERY
def gallery():
    p = "gallery.html"
    figs = ""
    for g in GALLERY:
        figs += f"""<figure class="reveal"><button type="button" data-full="{g['full']}" data-cap="{html.escape(g['cap'])}" aria-label="Open photo: {html.escape(g['cap'])}"><img src="{g['thumb']}" alt="{html.escape(g['alt'])}" loading="lazy"></button><figcaption>{html.escape(g['cap'])}</figcaption></figure>"""
    body = head("Gallery", "Photographs of Karnataka classical vocalist Kousthubh M S in concert, in dance drama and at home in Mysuru, with carvings from Karnataka temples.", p, "assets/img/photos/vocal-support.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Chitrashala · the picture hall", "Gallery", "ಚಿತ್ರಶಾಲೆ", "Moments from the stage, from home, and from the carved walls that inspire this site.", "assets/img/ornament/pillar-row.jpg")}
<section class="section">
  <div class="wrap"><div class="masonry">{figs}</div></div>
</section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="icon-btn x" type="button" aria-label="Close">{icon("close")}</button>
  <button class="icon-btn prev" type="button" aria-label="Previous photo">{icon("chevron_left")}</button>
  <img src="" alt="">
  <button class="icon-btn next" type="button" aria-label="Next photo">{icon("chevron_right")}</button>
  <p class="cap"></p>
</div>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ CONTACT
def contact():
    p = "contact.html"
    body = head("Contact", "Contact Vidwan Kousthubh M S, Karnataka classical vocalist, Mysuru, for concerts, lessons and collaborations.", p, "assets/img/photos/portrait-smile.jpg")
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Samparka · reaching out", "Contact", "ಸಂಪರ್ಕ", "For concerts, festivals, lecture demonstrations, recordings and lessons.", "assets/img/ornament/eave-kudu.jpg")}
<section class="section">
  <div class="wrap">
    <div class="letter reveal">
      <div class="head"></div>
      <img class="swirl" src="assets/img/ornament/letterhead-swirl.webp" alt="" aria-hidden="true">
      <div class="body">
        <div>
          <div class="lh-name"><span class="vidwan">Vidwan</span><p class="wordmark lhw" aria-label="Kousthubh M S">K<span class="o" aria-hidden="true"><img src="assets/img/ornament/tambura.webp" alt="" width="900" height="303"></span>usthubh<span class="ms">M S</span></p></div>
          <p style="font:500 1.05rem var(--f-ui);color:var(--muted);margin:18px 0 26px">Karnataka Classical Musician<br>Akashavani, All India Radio, Prasar Bharati: B High Grade Artist</p>
          <div class="contact-list">
            <a class="c-item" href="mailto:kousthubms@gmail.com" style="--c:var(--kumkuma)"><span class="ci">{icon("mail")}</span><span><b>kousthubms@gmail.com</b><span>Write anytime</span></span></a>
            <a class="c-item" href="tel:+919739728057" style="--c:var(--leaf)"><span class="ci">{icon("call")}</span><span><b>+91 97397 28057</b><span>Call</span></span></a>
            <a class="c-item" href="tel:+919380622058" style="--c:var(--neeli)"><span class="ci">{icon("call")}</span><span><b>+91 93806 22058</b><span>Call</span></span></a>
            <div class="c-item" style="--c:var(--terracotta)"><span class="ci">{icon("location_on")}</span><span><b>Srirampura, Mysuru</b><span>Karnataka 570023, India</span></span></div>
          </div>
          <p style="margin-top:18px"><button class="btn tonal" type="button" data-copy="kousthubms@gmail.com">{icon("mail")} Copy email address</button></p>
        </div>
        <form class="form" id="enquiry">
          <h2 style="font-size:1.8rem">Send an enquiry<span class="kn-sub" lang="kn">ವಿಚಾರಣೆ ಕಳುಹಿಸಿ</span></h2>
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-org">Organisation or place</label><input id="f-org" name="org" autocomplete="organization"></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-type">Kind of programme</label><select id="f-type" name="type"><option>Classical concert</option><option>Bhajan or devotional evening</option><option>Festival or utsava</option><option>Lecture demonstration</option><option>Dance drama music</option><option>Music lessons</option><option>Other</option></select></div>
          <div class="field"><label for="f-date">Preferred date</label><input id="f-date" name="date" type="date"></div>
          <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="msg" required></textarea></div>
          <button class="btn" type="submit">{icon("arrow_forward")} Compose email</button>
          <p style="font:400 .88rem var(--f-ui);color:var(--muted);margin:0">This opens your own email app with the message ready to send. Nothing is stored on this site.</p>
        </form>
      </div>
      <div class="foot"><span>{icon("mail")} kousthubms@gmail.com</span><span>{icon("location_on")} Srirampura, Mysuru 570023</span><span>{icon("call")} +91 97397 28057 · +91 93806 22058</span></div>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write(p, body)


# ================================================================ CREDITS
def credits():
    p = "credits.html"
    li = "".join(f'<li><b>{html.escape(c["what"])}</b>: {c["by"]}</li>' for c in CREDITS if c.get("show", True) and (not c.get("file") or has(c["file"])))
    body = head("Credits", "Credits for photographs, fonts and icons used on kousthub.in.", p)
    body += topbar(p)
    body += f"""<main id="main">
{page_hero("Kritajnata · gratitude", "Credits", "ಕೃತಜ್ಞತೆ", "With thanks to the photographers, type designers and open projects behind this site.", "assets/img/ornament/frieze-wall.jpg")}
<section class="section"><div class="wrap" style="max-width:860px"><div class="card temple"><ul class="credits">{li}</ul></div></div></section>
</main>
"""
    body += footer()
    write(p, body)


def notfound():
    body = head("Page not found", "This page could not be found.", "404.html")
    body = body.replace('href="assets/', 'href="/assets/').replace("src=\"assets/", "src=\"/assets/")
    tb = topbar("").replace('href="', 'href="/').replace('href="/https', 'href="https').replace('src="assets/', 'src="/assets/')
    ft = footer().replace('href="', 'href="/').replace('href="/https', 'href="https').replace('href="/mailto', 'href="mailto').replace('href="/tel', 'href="tel').replace('src="assets/', 'src="/assets/')
    body += tb + f"""<main id="main"><section class="page-hero"><div class="wrap"><div class="torana" aria-hidden="true"></div><span class="eyebrow">404</span><h1>This corridor is closed<span class="kn-sub" lang="kn">ಈ ಪ್ರಾಕಾರ ಮುಚ್ಚಿದೆ</span></h1><p class="lede">The page you looked for is not here. Return to the main hall.</p><a class="btn" href="/">{icon("home")} Go home</a></div></section></main>""" + ft
    write("404.html", body)


if __name__ == "__main__":
    home(); about(); guru(); accolades(); stage(); sadhana(); gallery(); contact(); credits(); notfound()
