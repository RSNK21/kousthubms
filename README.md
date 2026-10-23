# kousthub.in

Portfolio website of **Vidwan Kousthubh M S**, Karnataka classical vocalist, Mysuru.

A static, multi page site served by GitHub Pages at <https://kousthub.in>.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home (Mukha Mantapa): temple doorway hero, Rashi Mandapa (12 pillars, 12 swaras) |
| `about.html` | Journey, told as palm leaf manuscript leaves |
| `guru-parampara.html` | Teachers, as a lamp pillar lineage |
| `accolades.html` | 53 honours, laid out as courses of a temple wall, with filters |
| `stage.html` | Concerts, TV, radio and dance drama playbills |
| `sadhana.html` | Teaching, gamaka, Veda and a raga wheel sketch |
| `gallery.html` | Photo gallery with lightbox |
| `contact.html` | Letterhead styled contact page and enquiry form (opens the visitor's email app) |
| `credits.html` | Image, font and icon credits |

## Editing

All page text lives in `tools/build.py` and `tools/data.py` (accolades, gallery, credits).
After editing, regenerate the HTML:

```
python3 tools/build.py
```

Shared styles: `assets/css/site.css`. Behaviour: `assets/js/site.js`. Icons are Material Symbols SVGs in `assets/icons/`.

House rule: no em dashes anywhere on the site.

## Custom domain

`CNAME` contains `kousthub.in`. At the domain registrar, add these DNS records:

- `A` records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- `CNAME` record for `www`: `rsnk21.github.io`

Then in GitHub: Settings, Pages, confirm the custom domain and tick "Enforce HTTPS".
