import sys
import subprocess

def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure_package('streamlit')
ensure_package('folium')
ensure_package('requests')

import streamlit as st
import folium
from streamlit.components.v1 import html
import random
import requests

# Configurare pagină (titlu, iconiță, layout)
st.set_page_config(page_title="Mentor Carieră AI", page_icon="🎓", layout="wide")

# Ascundere elemente implicite Streamlit (meniu și footer)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Titlu și instrucțiuni de utilizare
st.markdown("# 🎓 Mentor Carieră AI")
st.markdown("_Completează, alege domeniul, apoi apasă **Vezi recomandări AI** — răspuns în ~5-10s._")

# Lista de materii posibile
subjects_list = ["Matematică", "Informatică", "Fizică", "Chimie", "Biologie",
                 "Limba și literatura română", "Istorie", "Geografie",
                 "Economie", "Arte"]

# Lista de cariere posibile
careers_list = ["Programator", "Medic", "Inginer", "Profesor", "Cercetător",
                "Artist", "Muzician", "Avocat", "Jurnalist", "Economist",
                "Antreprenor", "Psiholog", "Veterinar", "Arhitect", "Farmacist",
                "Contabil", "Scriitor", "Designer", "Analist de date", "Politician"]

# Definirea caracteristicilor fiecărei cariere
career_data = {
    "Programator": {
        "subjects": ["Matematică", "Informatică", "Fizică"],
        "mode": "Individual",
        "creativity": "med",
        "people": "low",
        "reason": "ai înclinație pentru logică și informatică",
        "steps": [
            "Învață bazele programării (ex: Python) prin cursuri online",
            "Realizează proiecte personale pentru portofoliu",
            "Aplică la internship-uri în dezvoltare software"
        ],
        "title": "Programator junior"
    },
    "Medic": {
        "subjects": ["Biologie", "Chimie"],
        "mode": "Team",
        "creativity": "med",
        "people": "high",
        "reason": "îți pasă de oameni și ești atras de științele vieții",
        "steps": [
            "Învață serios la biologie și chimie pentru admiterea la medicină",
            "Intră la o facultate de medicină și farmacie (6 ani de studiu)",
            "Urmează rezidențiatul într-o specializare medicală aleasă"
        ],
        "title": "Medic"
    },
    "Inginer": {
        "subjects": ["Matematică", "Fizică", "Informatică"],
        "mode": "Both",
        "creativity": "med",
        "people": "low",
        "reason": "ești orientat spre soluții practice și stăpânești științele exacte",
        "steps": [
            "Consolidează-ți cunoștințele de matematică și fizică prin proiecte practice",
            "Intră la o universitate tehnică (Politehnică) într-un domeniu de inginerie",
            "Participă la stagii sau proiecte de inginerie pentru experiență practică"
        ],
        "title": "Inginer"
    },
    "Profesor": {
        "subjects": ["Limba și literatura română", "Istorie", "Geografie"],
        "mode": "Team",
        "creativity": "med",
        "people": "high",
        "reason": "îți place să împărtășești cunoștințe și ai răbdare cu ceilalți",
        "steps": [
            "Studiază disciplina pe care vrei să o predai la o facultate de profil",
            "Urmează modulul pedagogic pentru a dobândi competențe didactice",
            "Fă practică într-o școală și implică-te în proiecte educative"
        ],
        "title": "Profesor"
    },
    "Cercetător": {
        "subjects": ["Biologie", "Chimie", "Fizică", "Informatică"],
        "mode": "Both",
        "creativity": "high",
        "people": "low",
        "reason": "ești curios din fire și pasionat de a descoperi lucruri noi",
        "steps": [
            "Urmează o facultate și apoi un program de masterat în domeniul care te pasionează",
            "Implică-te în proiecte de cercetare încă din timpul facultății",
            "Continuă cu un program de doctorat și publică rezultate în jurnale științifice"
        ],
        "title": "Cercetător"
    },
    "Artist": {
        "subjects": ["Arte"],
        "mode": "Individual",
        "creativity": "high",
        "people": "low",
        "reason": "ai talent creativ și dorința de a te exprima prin artă",
        "steps": [
            "Perfecționează-ți abilitățile artistice realizând un portofoliu de lucrări",
            "Urmează o facultate sau cursuri de artă pentru a-ți îmbunătăți tehnica",
            "Expune-ți creațiile în galerii sau online pentru a-ți face cunoscut talentul"
        ],
        "title": "Artist"
    },
    "Muzician": {
        "subjects": ["Arte"],
        "mode": "Both",
        "creativity": "high",
        "people": "low",
        "reason": "ai talent muzical și creativitate artistică",
        "steps": [
            "Studiază intens un instrument sau canto, sub îndrumarea unui profesor",
            "Urmează o facultate de muzică sau cursuri avansate de specialitate",
            "Participă la concursuri și concerte pentru a-ți lansa cariera muzicală"
        ],
        "title": "Muzician"
    },
    "Avocat": {
        "subjects": ["Istorie", "Limba și literatura română"],
        "mode": "Individual",
        "creativity": "med",
        "people": "med",
        "reason": "ai abilități de comunicare și te preocupă dreptatea",
        "steps": [
            "Pregătește-te la discipline socio-umane (istorie, logică) pentru admiterea la drept",
            "Finalizează studiile la o facultate de drept (4 ani) și efectuează stagiul (INM sau barou) pentru calificare",
            "Câștigă experiență lucrând într-un birou de avocatură sau prin internship-uri în domeniul juridic"
        ],
        "title": "Avocat"
    },
    "Jurnalist": {
        "subjects": ["Limba și literatura română", "Istorie", "Geografie"],
        "mode": "Both",
        "creativity": "high",
        "people": "med",
        "reason": "ești curios și ai talent la scris, dorind să informezi oamenii",
        "steps": [
            "Implică-te la revista școlii sau creează un blog pentru a exersa scrisul și documentarea",
            "Urmează o facultate de jurnalism sau comunicare pentru formare profesională",
            "Fă un stagiu într-o redacție locală sau la un post media pentru a dobândi experiență practică"
        ],
        "title": "Jurnalist"
    },
    "Economist": {
        "subjects": ["Matematică", "Economie"],
        "mode": "Individual",
        "creativity": "low",
        "people": "low",
        "reason": "ai gândire analitică și interes pentru afaceri și economie",
        "steps": [
            "Aprovizionează-te cu noțiuni de bază de economie și finanțe încă din liceu",
            "Urmează Academia de Studii Economice sau o facultate de profil economic",
            "Participă la internship-uri într-o bancă sau companie pentru a înțelege practic domeniul financiar"
        ],
        "title": "Economist"
    },
    "Antreprenor": {
        "subjects": ["Economie", "Informatică"],
        "mode": "Both",
        "creativity": "high",
        "people": "med",
        "reason": "îți asumi riscuri și ai viziune pentru a începe proiecte noi",
        "steps": [
            "Pornește un proiect mic sau o afacere pe cont propriu, chiar și experimental, pentru a învăța",
            "Caută mentori și programe de antreprenoriat (workshop-uri, incubatoare) de la care să obții îndrumare",
            "Fii perseverent: învață din eșecuri și îmbunătățește-ți constant ideile de afaceri"
        ],
        "title": "Antreprenor"
    },
    "Psiholog": {
        "subjects": ["Biologie", "Limba și literatura română"],
        "mode": "Individual",
        "creativity": "med",
        "people": "high",
        "reason": "ai empatie și ești interesat de mintea umană",
        "steps": [
            "Citește despre psihologie și încearcă să înțelegi comportamentul uman",
            "Urmează o facultate de psihologie și profită de practică pentru a-ți forma abilitățile",
            "Participă ca voluntar în proiecte de consiliere sau centre de suport pentru a câștiga experiență cu oamenii"
        ],
        "title": "Psiholog"
    },
    "Veterinar": {
        "subjects": ["Biologie", "Chimie"],
        "mode": "Both",
        "creativity": "low",
        "people": "high",
        "reason": "iubești animalele și ai cunoștințe de biologie",
        "steps": [
            "Fă voluntariat la un cabinet veterinar sau adăpost de animale pentru a căpăta experiență",
            "Urmează Facultatea de Medicină Veterinară (parte din universitățile de științe agricole și medicină veterinară)",
            "Specializează-te într-un domeniu (animale de companie, animale mari etc.) și obține licența de liberă practică"
        ],
        "title": "Medic veterinar"
    },
    "Arhitect": {
        "subjects": ["Matematică", "Arte"],
        "mode": "Both",
        "creativity": "high",
        "people": "med",
        "reason": "ai simț estetic și gândire spațială, combinând arta cu știința",
        "steps": [
            "Exersează desenul tehnic și proiectarea (poți urma cursuri de arhitectură pentru liceeni)",
            "Intră la o universitate de arhitectură (ex: „Ion Mincu” București) și finalizează studiile de licență și master",
            "Alătură-te unui birou de arhitectură ca stagiar pentru a învăța practic și obține drept de semnătură ca arhitect"
        ],
        "title": "Arhitect"
    },
    "Farmacist": {
        "subjects": ["Chimie", "Biologie"],
        "mode": "Individual",
        "creativity": "low",
        "people": "med",
        "reason": "ești atent la detalii și pasionat de chimie și sănătate",
        "steps": [
            "Pregătește-te la chimie pentru admiterea la facultatea de farmacie",
            "Urmează Facultatea de Farmacie (5 ani) pentru a deveni licențiat în farmacie",
            "Câștigă experiență lucrând într-o farmacie ca intern, apoi ca farmacist cu drept de liberă practică"
        ],
        "title": "Farmacist"
    },
    "Contabil": {
        "subjects": ["Matematică", "Economie"],
        "mode": "Individual",
        "creativity": "low",
        "people": "low",
        "reason": "ești organizat, atent la detalii și te descurci bine cu cifrele",
        "steps": [
            "Participă la un curs de contabilitate primară încă din liceu, dacă este posibil",
            "Urmează o facultate de contabilitate și informatică de gestiune sau un profil economic similar",
            "Obține o certificare profesională (ex: CECCAR) și caută un post de contabil junior pentru a acumula experiență"
        ],
        "title": "Contabil"
    },
    "Scriitor": {
        "subjects": ["Limba și literatura română", "Istorie", "Arte"],
        "mode": "Individual",
        "creativity": "high",
        "people": "low",
        "reason": "ai imaginație bogată și talent de a comunica idei în scris",
        "steps": [
            "Scrie constant – povestiri, poezii, articole – pentru a-ți dezvolta stilul",
            "Citește literatură variată pentru a-ți lărgi orizontul și a învăța de la autori consacrați",
            "Înscrie-te la concursuri literare sau ateliere de scriere creativă și încearcă să-ți publici lucrările"
        ],
        "title": "Scriitor"
    },
    "Designer": {
        "subjects": ["Arte", "Informatică"],
        "mode": "Individual",
        "creativity": "high",
        "people": "low",
        "reason": "ai ochi pentru estetică și creativitate în a realiza concepte vizuale",
        "steps": [
            "Învață instrumente de design grafic (ex: Photoshop, Illustrator) sau tehnici de design vestimentar, în funcție de domeniul ales",
            "Construiește-ți un portofoliu cu proiecte proprii pentru a-ți demonstra abilitățile",
            "Aplică la internship-uri sau joburi junior de designer pentru a obține experiență practică și a învăța din industrie"
        ],
        "title": "Designer"
    },
    "Analist de date": {
        "subjects": ["Matematică", "Informatică"],
        "mode": "Individual",
        "creativity": "med",
        "people": "low",
        "reason": "îți plac cifrele și identificarea tiparelor ascunse în date",
        "steps": [
            "Dezvoltă-ți cunoștințele de statistică și programare (ex: Python, R) prin cursuri online",
            "Urmează o specializare în data science sau informatică la facultate sau master",
            "Aplică abilitățile pe seturi de date reale (proiecte practice) și caută un internship ca analist de date"
        ],
        "title": "Analist de date"
    },
    "Politician": {
        "subjects": ["Istorie", "Geografie", "Limba și literatura română"],
        "mode": "Team",
        "creativity": "med",
        "people": "high",
        "reason": "îți dorești să contribui la societate și ai abilități de lider",
        "steps": [
            "Implică-te în consiliul elevilor sau în proiecte comunitare, ca să capeți experiență de leadership",
            "Studiază științe politice, administrație publică sau drept ca să înțelegi sistemul de guvernare",
            "Alătură-te unei organizații de tineret (de exemplu, unui partid politic) și construiește-ți rețeaua în domeniu"
        ],
        "title": "Politician"
    }
}

career_top_faculties = {
    "Programator": [
        {
            "name": "Universitatea Politehnica din București",
            "rank": "QS #1 Computer Science în România",
            "url": "https://www.upb.ro",
            "img": "https://acs.pub.ro/public/poster_acs_cover4-1024x715.jpg",
            "lat": 44.43833,
            "lon": 26.05139,
            "desc": "Cea mai prestigioasă universitate tehnică, cu programe solide de informatică și inginerie software."
        },
        {
            "name": "Universitatea Tehnică din Cluj-Napoca",
            "rank": "Top 3 CS în România",
            "url": "https://www.utcluj.ro",
            "img": "https://www.stiridecluj.ro/files/thumbs/259/7f5b4b6b8669164c4799fc52a86fd3f0.jpeg",
            "lat": 46.76920,
            "lon": 23.58550,
            "desc": "Renumită pentru centrele de cercetare în informatică și colaborările internaționale în software engineering."
        },
        {
            "name": "Universitatea din București",
            "rank": "Top 2 CS în România",
            "url": "https://unibuc.ro",
            "img": "https://img.a1.ro/?u=https%3A%2F%2Fa1.ro%2Fuploads%2Fmodules%2Fnews%2F0%2F2018%2F7%2F8%2F781881%2F1531058737d55e5112.jpg?w=1200&h=630&c=1",
            "lat": 44.43556,
            "lon": 26.10112,
            "desc": "Facultatea de Matematică și Informatică oferă cursuri avansate și proiecte de AI și Big Data."
        }
    ],
    "Medic": [
        {
            "name": "Universitatea de Medicină și Farmacie \"Carol Davila\" București",
            "rank": "#1 Medicină în România",
            "url": "https://umfcd.ro",
            "img": "https://umfcd.ro/wp-content/uploads/2018/10/743407-1532605235-listele-complete-cu-rezultatele-de-la-admiterea-la-medicina-bucuresti.jpg",
            "lat": 44.43528,
            "lon": 26.07000,
            "desc": "Una dintre cele mai vechi și prestigioase facultăți medicale, cu programe clinice extinse."
        },
        {
            "name": "Universitatea de Medicină și Farmacie Iuliu Hațieganu Cluj-Napoca",
            "rank": "Top 2 Medicină în România",
            "url": "https://www.umfcluj.ro",
            "img": "https://cdn.umfcluj.ro/uploads/2021/10/umfih-07.jpg",
            "lat": 46.76206,
            "lon": 23.58360,
            "desc": "Cunoscută pentru cercetare biomedicală și parteneriate cu spitale universitare de top."
        },
        {
            "name": "Universitatea de Medicină și Farmacie Grigore T. Popa Iași",
            "rank": "Top 3 Medicină în România",
            "url": "https://www.umfiasi.ro",
            "img": "https://news.umfiasi.ro/wp-content/uploads/2023/01/umf-iasi.jpg",
            "lat": 47.16015,
            "lon": 27.59581,
            "desc": "Pionier în educație medicală în Moldova, cu programe solide de cercetare clinică."
        }
    ],
    "Inginer": [
        {
            "name": "Universitatea Politehnica din București",
            "rank": "QS #1 Inginerie în România",
            "url": "https://www.upb.ro",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShu1KuSt9PuPhRBa0QO55ViyzNxMvCcX2U0g&s",
            "lat": 44.43833,
            "lon": 26.05139,
            "desc": "Lider în inginerie mecanică, electrotehnică și IT, cu laboratoare de ultimă generație."
        },
        {
            "name": "Universitatea Politehnica Timișoara",
            "rank": "Top 2 Inginerie în România",
            "url": "https://www.upt.ro",
            "img": "https://upt.ro/img/51445rectorat-upt-1.jpg",
            "lat": 45.75396,
            "lon": 21.22561,
            "desc": "Forte programe tehnice, proiecte Erasmus și cooperare cu industria europeană."
        },
        {
            "name": "Universitatea Tehnică din Cluj-Napoca",
            "rank": "Top 3 Inginerie în România",
            "url": "https://www.utcluj.ro",
            "img": "https://ie.utcluj.ro/files/Acasa/images/Facultatea2.jpg",
            "lat": 46.76920,
            "lon": 23.58550,
            "desc": "Renumită pentru departamentele de inginerie civilă și energetică."
        }
    ],
    "Profesor": [
        {
            "name": "Universitatea din București",
            "rank": "Top 1 Pedagogie în România",
            "url": "https://unibuc.ro",
            "img": "https://fpse.unibuc.ro/wp-content/uploads/2023/01/12094730_1482304882073084_3162350211045692050_o-624x243.jpg",
            "lat": 44.43556,
            "lon": 26.10112,
            "desc": "Facultatea de Psihologie și Științele Educației oferă formare pedagogică avansată."
        },
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca",
            "rank": "Top 2 Pedagogie în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://hartasanatatiimintale.ro/wp-content/uploads/2024/07/BCU.jpg",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Departament dedicat formării profesorilor, metodologii inovative de predare."
        },
        {
            "name": "Universitatea de Vest Timișoara",
            "rank": "Top 3 Pedagogie în România",
            "url": "https://www.uvt.ro",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKVsCJMr_0mo_FUAxiYX9tBgmFf5orFhhGWg&s",
            "lat": 45.74712,
            "lon": 21.23151,
            "desc": "Facultatea de Sociologie și Psihologie pregătește cadre didactice cu accent pe psihopedagogie."
        }
    ],
    "Cercetător": [
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca",
            "rank": "Top 1 cercetare universitara în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/UBB_Cluj_%282010%29.JPG",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Puternic în STEM, cu peste 200 de proiecte internaționale de cercetare."
        },
        {
            "name": "Universitatea din București",
            "rank": "Top 2 cercetare în România",
            "url": "https://unibuc.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/2/21/University_of_Bucharest_%281%29.jpg",
            "lat": 44.43556,
            "lon": 26.10112,
            "desc": "Excelență în științe sociale și natură, centre de cercetare multidisciplinare."
        },
        {
            "name": "Universitatea Alexandru Ioan Cuza Iași",
            "rank": "Top 3 cercetare în România",
            "url": "https://www.uaic.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/3/36/Palatul_Universitatii_din_Iasi.jpg",
            "lat": 47.16222,
            "lon": 27.58889,
            "desc": "Forte centre de cercetare în științe umaniste, chimie și biologie."
        }
    ],
    "Artist": [
        {
            "name": "Universitatea Națională de Arte București",
            "rank": "Top 1 Arte Vizuale în România",
            "url": "https://unarte.org",
            "img": "https://upload.wikimedia.org/wikipedia/commons/5/5a/UNArte_scoala.jpg",
            "lat": 44.44720,
            "lon": 26.09830,
            "desc": "Centrul principal de formare artistică, programe de licență și masterat diverse."
        },
        {
            "name": "Universitatea de Artă și Design Cluj-Napoca",
            "rank": "Top 2 Arte Vizuale în România",
            "url": "https://uad.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/0/0b/UAD_Cluj.jpg",
            "lat": 46.76960,
            "lon": 23.58300,
            "desc": "Renume pentru design grafic, arte plastice și arte decorative."
        },
        {
            "name": "Universitatea de Vest Timișoara - Facultatea de Arte și Design",
            "rank": "Top 3 Arte Vizuale în România",
            "url": "https://www.uvt.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/4/4f/UVT_corp_principal.jpg",
            "lat": 45.74712,
            "lon": 21.23151,
            "desc": "Programe interdisciplinare de arte vizuale, design și multimedia."
        }
    ],
    "Muzician": [
        {
            "name": "Universitatea Națională de Muzică București",
            "rank": "Top 1 Muzică în România",
            "url": "https://www.unmb.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/1/15/UNMB.jpg",
            "lat": 44.43918,
            "lon": 26.09700,
            "desc": "Lider în educație muzicală, studii superioare de interpretare și compoziție."
        },
        {
            "name": "Universitatea de Vest Timișoara - Facultatea de Muzică și Teatru",
            "rank": "Top 2 Muzică în România",
            "url": "https://www.uvt.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/4/4f/UVT_corp_principal.jpg",
            "lat": 45.74712,
            "lon": 21.23151,
            "desc": "Programe dedicate interpretării muzicale și muzicologiei."
        },
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca - Facultatea de Muzică și Teatru",
            "rank": "Top 3 Muzică în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/UBB_Cluj_%282010%29.JPG",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Renume pentru programe de muzică clasică și modernă, colaborări internaționale."
        }
    ],
    "Avocat": [
        {
            "name": "Universitatea din București - Facultatea de Drept",
            "rank": "Top 1 Drept în România",
            "url": "https://www.unibuc.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/2/21/University_of_Bucharest_%281%29.jpg",
            "lat": 44.43556,
            "lon": 26.10112,
            "desc": "Reputată pentru programele de licență și master în drept penal, civil și internațional."
        },
        {
            "name": "Academia de Studii Economice București - Facultatea de Drept",
            "rank": "Top 2 Drept în România",
            "url": "https://www.ase.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/3/33/ASE_Bucuresti.jpg",
            "lat": 44.44750,
            "lon": 26.09670,
            "desc": "Programe integrate de drept și economie, focus pe legislație comercială."
        },
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca - Facultatea de Drept",
            "rank": "Top 3 Drept în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/UBB_Cluj_%282010%29.JPG",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Curriculum axat pe drept european și dreptul omului."
        }
    ],
    "Jurnalist": [
        {
            "name": "SNSPA - Facultatea de Comunicare și Relații Publice",
            "rank": "Top 1 Jurnalism în România",
            "url": "https://snspa.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/8/84/SNSPA.jpg",
            "lat": 44.42800,
            "lon": 26.09000,
            "desc": "Program axat pe jurnalism multimedia și comunicare strategică."
        },
        {
            "name": "Universitatea din București - Facultatea de Jurnalism și Științele Comunicării",
            "rank": "Top 2 Jurnalism în România",
            "url": "https://unibuc.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/2/21/University_of_Bucharest_%281%29.jpg",
            "lat": 44.43556,
            "lon": 26.10112,
            "desc": "Specializări în jurnalism de investigație și media digitală."
        },
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca - Jurnalism",
            "rank": "Top 3 Jurnalism în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/UBB_Cluj_%282010%29.JPG",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Programe în jurnalism cultural și politic cu stagiaturi în mass-media locală."
        }
    ],
    "Economist": [
        {
            "name": "Academia de Studii Economice București",
            "rank": "Top 1 Economie în România",
            "url": "https://www.ase.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/3/33/ASE_Bucuresti.jpg",
            "lat": 44.44750,
            "lon": 26.09670,
            "desc": "Lider în științe economice, programe de finanțe, marketing și economie digitală."
        },
        {
            "name": "Universitatea Babeș-Bolyai Cluj-Napoca - Economie și Business",
            "rank": "Top 2 Economie în România",
            "url": "https://www.ubbcluj.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/6/6f/UBB_Cluj_%282010%29.JPG",
            "lat": 46.76767,
            "lon": 23.59137,
            "desc": "Departament cu cercetare puternică în economie comportamentală și data analytics."
        },
        {
            "name": "Universitatea Alexandru Ioan Cuza Iași - Economie",
            "rank": "Top 3 Economie în România",
            "url": "https://www.uaic.ro",
            "img": "https://upload.wikimedia.org/wikipedia/commons/3/36/Palatul_Universitatii_din_Iasi.jpg",
            "lat": 47.16222,
            "lon": 27.58889,
            "desc": "Programe de macroeconomie și politici economice, centre de analize economice."
        }
    ],
    # Poți continua pentru restul carierelor (Antreprenor, Psiholog, Veterinar, Arhitect, Farmacist, Contabil, Scriitor, Designer, Analist de date, Politician) în același format.
}


# După ce ai definit acest dict, în locul actualizării hărții
# folosește `career_top_faculties[sugested_career]` pentru a plasa
# marker-e cu imagine și link în popup.


# Imagini reprezentative pentru unele cariere (dacă disponibile)
career_images = {
    # "Programator": "https://upload.wikimedia.org/wikipedia/commons/d/da/Software_developer_at_work_02.jpg",
    # (Se pot adăuga imagini pentru restul carierelor dacă sunt disponibile)
}

# Durata studiilor necesare (ani, aproximativ) pentru unele cariere
study_years = {
    "Medic": 10,
    "Cercetător": 8,
    "Veterinar": 6,
    "Arhitect": 6,
    "Farmacist": 5,
    "Avocat": 5
}
# Pentru celelalte cariere care nu apar aici, vom considera implicit 4 ani (o licență)

# Formular de introducere a datelor utilizatorului
with st.form("input_form"):
    favorite_subjects = st.multiselect("Materii favorite:", options=subjects_list)
    work_mode = st.radio("Preferi să lucrezi:", ["Individual", "În echipă", "Ambele"], index=2)
    creativity_level = st.slider("Creativitate (0-10):", 0, 10, 5)
    people_level = st.slider("Dorința de a ajuta oamenii (0-10):", 0, 10, 5)
    leadership_level = st.slider("Spirit de lider / inițiativă (0-10):", 0, 10, 5)
    study_choice = st.radio("Cât de mult ești dispus să studiezi pentru cariera dorită?",
                             ["3-4 ani (doar licență)", "5-6 ani (master)", "7+ ani (doctorat/rezidențiat)"], index=1)
    preferred_career = st.selectbox("Domeniu preferat (opțional):", ["(Niciunul)"] + careers_list, index=0)
    submit = st.form_submit_button("Vezi recomandări AI")

# La apăsarea butonului, se procesează intrările și se generează recomandările
if submit:
    suggestions = []
    # Adaugă opțiunea preferată dacă a fost selectată
    if preferred_career and preferred_career != "(Niciunul)":
        if preferred_career in career_data:
            suggestions.append(preferred_career)
    # Calculează scorul de potrivire pentru fiecare carieră
    scores = []
    # Normalizează modul de lucru al utilizatorului pentru comparare
    user_mode_norm = "Team" if work_mode == "În echipă" else ("Individual" if work_mode == "Individual" else "Both")
    # Categorii pentru creativitate și dorința de a ajuta (low/med/high)
    if creativity_level >= 7:
        user_creativity_cat = "high"
    elif creativity_level >= 4:
        user_creativity_cat = "med"
    else:
        user_creativity_cat = "low"
    if people_level >= 7:
        user_people_cat = "high"
    elif people_level >= 4:
        user_people_cat = "med"
    else:
        user_people_cat = "low"
    # Interpretează preferința pentru durata studiilor
    if "7+" in study_choice:
        max_study = 999  # practic fără limită
    elif "5-6" in study_choice:
        max_study = 6
    else:
        max_study = 4
    # Evaluează fiecare carieră potențială
    for career_name, info in career_data.items():
        if career_name in suggestions:  # sare peste cariera preferată deja adăugată
            continue
        score = 0
        # Potrivirea materiilor
        if info["subjects"]:
            if set(favorite_subjects) & set(info["subjects"]):
                # adaugă puncte pentru fiecare materie care se potrivește
                score += 3 * len(set(favorite_subjects) & set(info["subjects"]))
            else:
                # dacă nu se potrivește nicio materie esențială (dacă există), penalizează puțin
                score -= 1
        # Potrivirea modului de lucru
        career_mode_norm = "Team" if info["mode"] in ["Team", "În echipă"] else ("Individual" if info["mode"] == "Individual" else "Both")
        if career_mode_norm == "Both" or user_mode_norm == "Both":
            score += 1  # flexibilitate
        else:
            if user_mode_norm == career_mode_norm:
                score += 2
            else:
                # penalizare dacă unul e strict individual și celălalt strict în echipă
                if (user_mode_norm == "Individual" and career_mode_norm == "Team") or (user_mode_norm == "Team" and career_mode_norm == "Individual"):
                    score -= 2
        # Potrivirea creativității
        demand_creat = info["creativity"]
        if demand_creat == "high":
            if user_creativity_cat == "high":
                score += 2
            elif user_creativity_cat == "med":
                score += 0
            else:
                score -= 3
        elif demand_creat == "med":
            if user_creativity_cat == "high":
                score += 1
            elif user_creativity_cat == "med":
                score += 2
            else:
                score -= 2
        elif demand_creat == "low":
            if user_creativity_cat == "high":
                score -= 1
            elif user_creativity_cat == "med":
                score += 0
            else:
                score += 2
        # Potrivirea dorinței de a ajuta (lucru cu oamenii)
        demand_people = info["people"]
        if demand_people == "high":
            if user_people_cat == "high":
                score += 2
            elif user_people_cat == "med":
                score += 0
            else:
                score -= 3
        elif demand_people == "med":
            if user_people_cat == "high":
                score += 1
            elif user_people_cat == "med":
                score += 2
            else:
                score -= 2
        elif demand_people == "low":
            if user_people_cat == "high":
                score -= 1
            elif user_people_cat == "med":
                score += 0
            else:
                score += 2
        # Potrivirea spiritului de lider
        if leadership_level >= 7:
            if career_name in ["Antreprenor", "Politician"]:
                score += 2
            if career_name in ["Avocat", "Profesor"]:
                score += 1
        elif leadership_level <= 3:
            if career_name in ["Antreprenor", "Politician", "Avocat"]:
                score -= 2
        # Potrivirea cu durata studiilor dorită
        required_years = study_years.get(career_name, 4)
        if max_study < required_years:
            score -= 2  # cariera necesită studii mai lungi decât e dispus utilizatorul
        elif max_study >= 7 and required_years >= 7:
            score += 1  # utilizatorul e dispus la studii lungi și cariera cere studii lungi
        scores.append((score, career_name))
    # Sortează carierele descrescător după scor
    scores.sort(reverse=True, key=lambda x: x[0])
    # Selectează primele 2 opțiuni (cele mai potrivite)
    for sc, career_name in scores[:2]:
        suggestions.append(career_name)
        if len(suggestions) >= 2:
            break
    # Elimină dublurile (dacă cariera preferată apărea și în top scor)
    suggestions = list(dict.fromkeys(suggestions))
    suggestions = suggestions[:2]

    # Afișează recomandările dacă există
    if suggestions:
        st.markdown("## 🔍 Iată recomandările Mentorului AI:")
        # Definim iconițe pentru cariere (emoji relevante)
        career_icons = {
            "Programator": "🚀", "Medic": "🩺", "Inginer": "⚙️", "Profesor": "📚", "Cercetător": "🔬",
            "Artist": "🎨", "Muzician": "🎵", "Avocat": "⚖️", "Jurnalist": "📰", "Economist": "💼",
            "Antreprenor": "💡", "Psiholog": "🧠", "Veterinar": "🐾", "Arhitect": "📐", "Farmacist": "💊",
            "Contabil": "📊", "Scriitor": "✒️", "Designer": "🎨", "Analist de date": "📈", "Politician": "🏛️"
        }
        for career_name in suggestions:
            info = career_data[career_name]
            title = info["title"]
            reason = info["reason"]
            # Personalizează motivul dacă utilizatorul are anumite materii relevante
            if info["subjects"]:
                common_subj = [s for s in favorite_subjects if s in info["subjects"]]
                if common_subj:
                    if career_name == "Medic":
                        reason = "îți pasă de oameni și ești pasionat de biologie și chimie"
                    elif career_name == "Programator":
                        if "Informatică" in common_subj and "Matematică" in common_subj:
                            reason = "ai înclinație pentru matematică și informatică"
                        elif "Informatică" in common_subj:
                            reason = "ai pasiune pentru informatică și gândire logică"
                        elif "Matematică" in common_subj:
                            reason = "ai gândire logică, dovadă fiind aptitudinea la matematică"
                    elif career_name == "Avocat":
                        if "Istorie" in common_subj:
                            reason = "cunoștințele tale de istorie și cultura generală te vor ajuta în domeniul juridic"
                        elif "Limba și literatura română" in common_subj:
                            reason = "stăpânești limba română, esențială pentru argumentarea juridică"
                    elif career_name == "Arhitect" and {"Matematică", "Arte"} <= set(common_subj):
                        reason = "combini talentul artistic cu logica matematică - exact ce trebuie pentru arhitectură"
            steps = info["steps"]
            icon = career_icons.get(career_name, "🖋️")
            # Afișează cariera cu imagine și text alăturat
            col1, col2 = st.columns([1, 3])
            #with col1:
            #    if career_name in career_images:
            #        st.image(career_images[career_name], caption=career_name, width=200)
            st.markdown(f"**{icon} {title}** — {reason}")
            steps_markdown = "\n".join([f"{idx}. {step}" for idx, step in enumerate(steps, 1)])
            st.markdown(steps_markdown)
            # iterăm facultățile din career_top_faculties
            st.markdown(f"### 🎓 Facultăți de top pentru {career_name} 📚")
            for fac in career_top_faculties.get(career_name, []):
                # Creăm două coloane: prima pentru imagine, a doua pentru text
                col_img, col_text = st.columns([1, 4])
                with col_img:
                    # folosim HTML direct pentru a ne asigura că src e pus corect
                    st.markdown(
                        f"<img src='{fac['img']}' height='120' style='border-radius:8px;'/>",
                        unsafe_allow_html=True
                    )
                with col_text:
                    st.markdown(
                        f"**[{fac['name']}]({fac['url']})**  \n\n"
                        f"{fac['rank']}  \n\n"
                        f"{fac['desc']}"
                    )
            st.markdown("---")

        # Mesaj de încurajare personalizat (sfat AI) cu variante
        advice_lines = []
        advice_lines.append("Crede în tine!")
        if len(favorite_subjects) >= 2:
            subj1, subj2 = favorite_subjects[0], favorite_subjects[1]
            advice_lines.append(f"Faptul că îți plac atât **{subj1}** cât și **{subj2}** îți oferă o perspectivă unică.")
        elif len(favorite_subjects) == 1:
            subj = favorite_subjects[0]
            advice_lines.append(f"Pasiunea ta pentru **{subj}** este un atu important.")
        # Sinergii speciale între arte și științe
        if "Arte" in favorite_subjects and set(favorite_subjects) & {"Matematică", "Informatică", "Fizică", "Chimie", "Biologie"}:
            advice_lines.append("Inspirația din arte îți poate aduce un plus de creativitate în domeniul tehnic.")
        # Mențiuni despre creativitate și empatie dacă sunt foarte pronunțate
        if people_level >= 8 and creativity_level >= 8:
            advice_lines.append("Ai atât empatie, cât și creativitate – calități rare care te vor purta spre succes.")
        else:
            if people_level >= 8:
                advice_lines.append("Empatia și dorința ta de a-i ajuta pe alții te vor ghida către o carieră de succes.")
            if creativity_level >= 8:
                advice_lines.append("Creativitatea ta îți va da puterea să găsești soluții originale în tot ceea ce faci.")
        advice_lines.append("Nu uita, ești la început de drum: continuă să înveți și să crești, iar succesul nu va întârzia să apară!")
        # Varianta 1: mesaj complet
        message1 = " ".join(advice_lines)
        # Varianta 2: mesaj alternativ
        message2_lines = []
        message2_lines.append("Crede în tine!")
        if len(favorite_subjects) >= 2:
            subj1, subj2 = favorite_subjects[0], favorite_subjects[1]
            message2_lines.append(f"Dacă îți plac atât {subj1} cât și {subj2}, înseamnă că ai perspective multiple în viață.")
        elif len(favorite_subjects) == 1:
            subj = favorite_subjects[0]
            message2_lines.append(f"Pasiunea ta pentru {subj} îți va fi un ghid de nădejde în carieră.")
        if people_level >= 8 and creativity_level >= 8:
            message2_lines.append("În plus, combinația de empatie și creativitate îți oferă un avantaj unic.")
        elif people_level >= 8:
            message2_lines.append("Empatia ta față de ceilalți este remarcabilă și te va diferenția.")
        elif creativity_level >= 8:
            message2_lines.append("Creativitatea ta te va ajuta să găsești soluții originale la provocări.")
        message2_lines.append("Mergi înainte cu încredere și perseverență, iar succesul te așteaptă!")
        message2 = " ".join(message2_lines)
        # Varianta 3: mesaj alternativ
        message3_lines = []
        if len(favorite_subjects) >= 2:
            subj1, subj2 = favorite_subjects[0], favorite_subjects[1]
            message3_lines.append(f"Pasiunea ta pentru {subj1} și {subj2} îți oferă un avantaj pe care puțini îl au.")
        elif len(favorite_subjects) == 1:
            subj = favorite_subjects[0]
            message3_lines.append(f"Pasiunea ta pentru {subj} va fi motorul reușitei tale.")
        if people_level >= 8 and creativity_level >= 8:
            message3_lines.append("Faptul că ești atât empatic(ă) cât și creativ(ă) te va diferenția în orice domeniu.")
        else:
            if people_level >= 8:
                message3_lines.append("Empatia ta deosebită te va ghida către o carieră împlinită.")
            if creativity_level >= 8:
                message3_lines.append("Creativitatea ta este un atu de preț în drumul spre succes.")
        message3_lines.append("Ai tot ce îți trebuie pentru a reuși - continuă să înveți și vei ajunge departe!")
        message3 = " ".join(message3_lines)
        # Alege una dintre variante în mod aleatoriu
        advice_options = [message1, message2, message3]
        advice_message = random.choice(advice_options)
        st.markdown(f"<div style='background-color: rgba(76, 175, 80, 0.1); padding: 15px; border-radius: 5px;'>💬 <b>Sfat AI personalizat:</b> {advice_message}</div>", unsafe_allow_html=True)
        # Oferă opțiunea de a descărca recomandările ca fișier text
        download_lines = []
        for career_name in suggestions:
            info = career_data[career_name]
            title = info["title"]
            reason = info["reason"]
            steps = info["steps"]
            download_lines.append(f"{title} - {reason}")
            for idx, step in enumerate(steps, 1):
                download_lines.append(f"    {idx}. {step}")
            download_lines.append("")  # linie goală între recomandări
        download_lines.append("Mult succes în carieră!")
        download_content = "\n".join(download_lines)
        st.download_button("Descarcă recomandările", data=download_content, file_name="recomandari.txt", mime="text/plain")
    else:
        st.write("Nu s-au găsit recomandări pe baza datelor introduse. Încearcă alte combinații de opțiuni.")
