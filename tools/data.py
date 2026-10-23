# Content data for kousthub.in. Edit here, then run: python3 tools/build.py

# Courses of the temple wall, listed top to bottom (foundation last)
TIERS = [
    {"key": "features", "short": "Concerts and media", "title": "Concerts, television and dance drama", "kn": "ಕಛೇರಿ, ದೂರದರ್ಶನ, ನೃತ್ಯನಾಟಕ", "motif": "Nartaki course · dancers"},
    {"key": "honours", "short": "Honours", "title": "Pratibha Puraskara honours", "kn": "ಪ್ರತಿಭಾ ಪುರಸ್ಕಾರ", "motif": "Simha course · lions"},
    {"key": "stage", "short": "Light, devotional, patriotic", "title": "Light, devotional and patriotic music", "kn": "ಸುಗಮ, ಭಕ್ತಿ, ದೇಶಭಕ್ತಿ", "motif": "Latha course · creepers"},
    {"key": "folk", "short": "Folk music", "title": "Folk music", "kn": "ಜಾನಪದ ಸಂಗೀತ", "motif": "Ashva course · horses"},
    {"key": "gita", "short": "Bhagavadgita recital", "title": "Srimad Bhagavadgita recital", "kn": "ಶ್ರೀಮದ್ ಭಗವದ್ಗೀತಾ ಪಠಣ", "motif": "Hamsa course · swans"},
    {"key": "degree", "short": "Degrees and grades", "title": "Degrees, grades and gradations", "kn": "ಪದವಿ ಮತ್ತು ಶ್ರೇಣಿ", "motif": "Gaja course · elephants"},
]

def A(cat, org, what, prize, kind, date="", star=False):
    return {"cat": cat, "org": org, "what": what, "prize": prize, "kind": kind, "date": date, "star": star}

ACCOLADES = [
    # Foundation: degrees and grades
    A("degree", "Akashavani, All India Radio Mysuru, Prasar Bharati", "Gradation as a vocal artist", "B High Grade Artist", "top", "2025", True),
    A("degree", "Rasarishi Institution, affiliated to Hampi Kannada University", "Master of Music (M.A. in Music)", "A+ Grade", "top", "2024", True),
    A("degree", "KSEEB, Government of Karnataka", "Senior grade examination, Karnataka Music: Vocal", "Distinction, First Rank in the Board", "top", "2019", True),
    A("degree", "The National Institute of Engineering, Mysuru (VTU, Belagavi)", "Master of Computer Applications", "Distinction", "top", "2019", True),
    A("degree", "Directorate General, All India Radio", "Folk music", "First prize, Akashavani Grade B Artist", "first", "8 May 2015"),
    A("degree", "Government of Karnataka", "Junior music examination, Vocal", "First Class, 80%", "cert"),
    A("degree", "Gamaka examinations", "Gamaka Prathama, Pravesha, Proudha and Kaajaana", "First Class", "cert"),
    # Folk
    A("folk", "Kannada and Culture Department, Bengaluru", "State level Kalapratibhotsava: Folk music", "First Prize", "first", "19 January 2008"),
    A("folk", "University of Mysore, Inter Collegiate Cultural Meet", "Folk music", "First Prize", "first", "9 October 2015"),
    A("folk", "Vidya Vardhaka Sangha (R), Mysuru", "Folk music", "Certificate of Excellence and Appreciation", "cert", "11 February 2011"),
    A("folk", "K.M. Praveen Kumar Charitable Trust, Mysuru", "Folk music", "First Prize", "first", "2 October 2009"),
    A("folk", "Department of Educational Office, South Zone, Mysuru", "Pratibha Karanji: Folk music", "Second Prize", "second", "6 October 2009"),
    A("folk", "University of Mysore, T.T.L. College, Mysuru", "Folk music", "Third Prize", "third", "15 October 2015"),
    A("folk", "Vijayanagar Cultural Organization (R), Mysuru", "Folk music", "Third Prize", "third", "23 November 2008"),
    A("folk", "Mukhya Prana Kannada Paper, Mysuru", "Folk music", "Third Prize", "third", "August 2007"),
    A("folk", "Government of Karnataka, Kannada and Culture Department", "District level Kala Pratibhotsava: Folk music", "First Prize", "first", "14 December 2007"),
    # Light, devotional, patriotic
    A("stage", "Mysore Dasara Mahotsava", "Light music", "Certificate of Excellence", "cert", "6 October 2013"),
    A("stage", "S.B.R.R. Mahajana First Grade College, Mysuru", "Patriotic songs", "Second Prize", "second", "8 August 2010"),
    A("stage", "Life Insurance Corporation, Mysuru", "Devotional music", "Second Prize", "second", "8 September 2010"),
    A("stage", "Department of Kannada and Culture, Mysuru", "District level: Patriotic music", "First Prize", "first"),
    A("stage", "Government of Karnataka, Dept. of Kannada and Culture, Mysuru", "Geetha Gayana Tarabethi camp", "Certificate of Excellence", "cert", "9 February 2016"),
    # Bhagavadgita recital
    A("gita", "Divyadhwani Sampada, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "26 December 2004"),
    A("gita", "Mata Amritanandamayi Math, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "2 October 2005"),
    A("gita", "Sri Maruti Yoga Kendra Trust, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "4 December 2005"),
    A("gita", "Vivekananda Kendra, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "1 January 2006"),
    A("gita", "Sri Sharada Samskrutha Pathashaala, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "15 January 2006"),
    A("gita", "Sri Narayanananda Universal Yoga Ashrama, Mysuru", "District level Bhagavadgita recitation", "Second Prize", "second", "22 January 2006"),
    A("gita", "ISKCON Heritage Fest, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "10 August 2006"),
    A("gita", "Department of Educational Office, South Zone, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "9 September 2006"),
    A("gita", "ISKCON Heritage Fest, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "9 October 2006"),
    A("gita", "Swararnava Kala Mandira, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "29 October 2006"),
    A("gita", "Vidyavardhaka Sangha, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "14 November 2006"),
    A("gita", "Divyadhwani Sampada, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "3 December 2006"),
    A("gita", "Krishnamurthypuram Ram Mandira, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "31 December 2006"),
    A("gita", "ISKCON Heritage Fest, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "2 August 2007"),
    A("gita", "Pramathi Hillview Academy, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "19 August 2007"),
    A("gita", "Sri Sharada Samskrutha Pathashaala, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "12 January 2008"),
    A("gita", "Department of Educational Office, South Zone, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "13 September 2008"),
    A("gita", "Vidwan A. Shrinivasaraghavacharya Centenary Celebrations", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "12 December 2008"),
    A("gita", "Vidyavardhaka Sangha, Mysuru", "Srimad Bhagavadgita shloka recital", "First Prize", "first", "14 November 2009"),
    A("gita", "ISKCON Heritage Fest, Mysuru", "Srimad Bhagavadgita shloka recital", "Second Prize", "second", "10 August 2010"),
    # Honours
    A("honours", "Aadarsha Seva Organization (R), Mysuru", "Pratibha Puraskar", "Aadarsha Pratibha Award", "cert"),
    A("honours", "Agastya Credit Co-operative Society (R), Mysuru", "Pratibha Puraskar", "Pratibha Award", "cert"),
    A("honours", "Kannada and Cultural Trust, Mysuru", "Pratibha Puraskar", "Kannada Keertisri Award", "cert"),
    A("honours", "Mysore Sahitya Samskruthika Pratishthana", "Pratibha Puraskar", "Yuvashree Award", "cert"),
    # Features
    A("features", "Mysore Dasara Grand Festival", "Karnataka classical concert with Guru Dr. R.S. Nandakumar", "Certificate of Excellence", "cert", "15 October 2015"),
    A("features", "SVBC TV, Tirupati", "Nada Neerajanam: vocal accompaniment to Guru Dr. R.S. Nandakumar", "Featured", "feature"),
    A("features", "SVBC TV, Tirupati", "Narada Koravanji dance drama, Nada Neerajanam", "Lead role", "feature"),
    A("features", "Sadhana Sangama Trust, Bengaluru", "Yugala Bahula Mukula Festival dance drama", "Lead role", "feature"),
    A("features", "ISKCON, Mysuru", "Sri Krishna Janmashtami dance drama", "Lead role", "feature"),
    A("features", "All India Radio, Mysuru", "Award winning programme Vachana Pada Vaidya; also Desi Adda, Samskara Bharati and more", "Songs featured", "feature"),
    A("features", "Major concerts across Karnataka", "Vocal support to Guru Dr. R.S. Nandakumar", "Vocal support", "feature"),
    A("features", "Kanchi Kamakoti Shankara University, Kanchipuram", "First Tyagaraja Aradhana celebrations", "Invited artist", "feature", "January 2017"),
]

GALLERY = [
    {"thumb": "assets/img/thumbs/tambura-portrait.jpg", "full": "assets/img/photos/tambura-portrait.jpg", "cap": "With the tambura.", "alt": "Kousthubh seated with a tambura, in white with a silk angavastra"},
    {"thumb": "assets/img/thumbs/concert-orange.jpg", "full": "assets/img/photos/concert-orange.jpg", "cap": "In concert with an ensemble.", "alt": "Kousthubh in a saffron kurta singing seated on stage"},
    {"thumb": "assets/img/thumbs/portrait-smile.jpg", "full": "assets/img/photos/portrait-smile.jpg", "cap": "A smile between songs.", "alt": "Close portrait of Kousthubh smiling"},
    {"thumb": "assets/img/thumbs/with-guru-tambura.jpg", "full": "assets/img/photos/with-guru-tambura.jpg", "cap": "Holding the shruthi beside his guru.", "alt": "Kousthubh holding a tambura beside a senior vocalist singing at a microphone"},
    {"thumb": "assets/img/thumbs/vocal-support.jpg", "full": "assets/img/photos/vocal-support.jpg", "cap": "Two voices, one raga.", "alt": "Two vocalists in white kurtas singing at microphones"},
    {"thumb": "assets/img/thumbs/with-dancer.jpg", "full": "assets/img/photos/with-dancer.jpg", "cap": "After a dance drama.", "alt": "Kousthubh beside a Bharatanatyam dancer in costume"},
    {"thumb": "assets/img/thumbs/at-the-mic.jpg", "full": "assets/img/photos/at-the-mic.jpg", "cap": "At the microphone.", "alt": "Kousthubh singing at a microphone in a white kurta"},
    {"thumb": "assets/img/thumbs/dance-drama-stage.jpg", "full": "assets/img/photos/dance-drama-stage.jpg", "cap": "On stage with fellow artists.", "alt": "Kousthubh in a saffron kurta with two dancers on stage"},
    {"thumb": "assets/img/thumbs/with-guru-concert.jpg", "full": "assets/img/photos/with-guru-concert.jpg", "cap": "Vocal support in concert.", "alt": "Kousthubh in a saffron kurta singing behind the lead vocalist"},
    {"thumb": "assets/img/thumbs/by-the-lake.jpg", "full": "assets/img/photos/by-the-lake.jpg", "cap": "By the lake, at home in Mysuru.", "alt": "Kousthubh standing by a lake"},
    {"thumb": "assets/img/thumbs/srividya-nadavidya-stage.jpg", "full": "assets/img/photos/srividya-nadavidya-stage.jpg", "cap": "A lecture concert stage.", "alt": "Wide view of a concert stage with yellow drapes"},
    {"thumb": "assets/img/thumbs/graduation-shawl.jpg", "full": "assets/img/photos/graduation-shawl.jpg", "cap": "A day of honour.", "alt": "Kousthubh in a cream kurta and saffron stole"},
    {"thumb": "assets/img/thumbs/traditional-attire.jpg", "full": "assets/img/photos/traditional-attire.jpg", "cap": "In traditional attire.", "alt": "Kousthubh in a white panche and uttariya"},
    {"thumb": "assets/img/thumbs/at-the-mic-2.jpg", "full": "assets/img/photos/at-the-mic-2.jpg", "cap": "Mid phrase.", "alt": "Kousthubh singing into a microphone"},
    {"thumb": "assets/img/ornament/frieze-wall.jpg", "full": "assets/img/ornament/frieze-wall.jpg", "cap": "Temple wall friezes: elephants, horsemen, scrolls and deities.", "alt": "Carved temple wall with layered friezes"},
    {"thumb": "assets/img/ornament/pillar-hall.jpg", "full": "assets/img/ornament/pillar-hall.jpg", "cap": "A lathe turned stone pillar catching the light.", "alt": "Lathe turned stone pillar in a temple hall"},
    {"thumb": "assets/img/ornament/frieze-figures.jpg", "full": "assets/img/ornament/frieze-figures.jpg", "cap": "Carved figures on a temple frieze.", "alt": "Row of carved figures on a temple frieze"},
]

CREDITS = [
    {"what": "Photographs of Kousthubh", "by": "From the family collection and the artist's bio data. All rights reserved."},
    {"what": "Temple carvings, pillar and border ornaments", "by": "Photographs and cutouts supplied by the family."},
    {"what": "Letterhead tambura and design", "by": "From Kousthubh's personal letterhead."},
    {"what": "Fonts", "by": 'EB Garamond, Alegreya, Alegreya Sans, Playfair Display, Smooch Sans, Benne and Tiro Kannada, all served by <a href="https://fonts.google.com" target="_blank" rel="noopener">Google Fonts</a> under the SIL Open Font License.'},
    {"what": "Icons", "by": '<a href="https://github.com/google/material-design-icons" target="_blank" rel="noopener">Material Symbols by Google</a>, Apache License 2.0.'},
]

# Wikimedia Commons images (added when present in assets/img/temple/)
WIKI = [
    ("assets/img/temple/vidyashankara.jpg", "Vidyashankara temple, Sringeri", "Vidyashankara_Temple_at_Shringeri.jpg", "Calvinkrishy", "CC BY-SA 2.5", "https://creativecommons.org/licenses/by-sa/2.5/"),
]
try:
    from wiki_extra import WIKI_EXTRA
    WIKI += WIKI_EXTRA
except ImportError:
    pass
for f, what, name, author, lic, licurl in WIKI:
    CREDITS.append({"file": f, "what": what, "by": f'Photo by {author}, <a href="https://commons.wikimedia.org/wiki/File:{name}" target="_blank" rel="noopener">Wikimedia Commons</a>, <a href="{licurl}" target="_blank" rel="noopener">{lic}</a>. Colour toned for this site.'})
