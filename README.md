[![Launch App](https://img.shields.io/badge/🔗-Live%20Demo-blue)](https://aicareermentor.streamlit.app/)

## 🎓 Mentor Carieră AI

**Mentor Carieră AI** este o aplicație web scrisă în **Python**, proiectată sub forma unui site interactiv, care te ajută să descoperi cariera potrivită în funcție de profilul și preferințele tale.

---

## 🔑 Caracteristici principale

1. **Selecție personalizată de materii**  
   Alegi materiile favorite și prioritățile tale (creativitate, empatie, spirit de lider), iar algoritmul le ia în calcul pentru potrivirea cu diverse cariere.  

2. **Recomandări AI “on-the-fly”**  
   Folosește **Streamlit** pentru a genera rapid (în doar câteva secunde) top-ul a până la 5 cariere care se potrivesc cel mai bine profilului tău :contentReference[oaicite:0]{index=0}.

3. **Secțiuni extinse cu `st.expander`**  
   Fiecare carieră recomandată are o zonă collapsible pentru detalii (motivul potrivirii, pași concreți și top-facultăți) :contentReference[oaicite:1]{index=1}.

4. **Top facultăți recomandate**  
   Pentru fiecare carieră, afișăm primele 3 instituții de învățământ, cu logo/poză, linkuri și detalii (loc în clasament, descriere) :contentReference[oaicite:2]{index=2}.

5. **Descărcare recomandări**  
   Poți salva recomandările ca fișier text cu un singur clic, prin widget-ul `st.download_button` :contentReference[oaicite:3]{index=3}.

6. **Hartă interactivă (opțional)**  
   Integrează **Folium** pentru afișarea centrelor universitare pe harta României :contentReference[oaicite:4]{index=4}.

7. **HTTP & API calls**  
   Biblioteca **Requests** este utilizată pentru eventuale interacțiuni cu API-uri externe :contentReference[oaicite:5]{index=5}.

8. **Structură modulară**  
   - `career_data`: definiții detaliate ale carierelor  
   - `career_top_faculties`: lista instituțiilor de top  
   - Funcții de scor și de normalizare a intrărilor  

9. **Design și UX**  
   - Layout „wide” pentru o experiență desktop plăcută  
   - CSS personalizat pentru un look modern (fonturi Montserrat, paletă întunecată + accente aurii)  
   - Componente vizuale elegante și feedback instant (baloane, animații)

---

## 🛠️ Tehnologii folosite

- **[Streamlit](https://pypi.org/project/streamlit/)** (Open-source Python framework pentru rapid prototyping) :contentReference[oaicite:6]{index=6}  
- **[Folium](https://python-visualization.github.io/folium/)** (Hartă interactivă bazată pe Leaflet) :contentReference[oaicite:7]{index=7}  
- **[Requests](https://en.wikipedia.org/wiki/Requests_(software))** (HTTP client pentru Python) :contentReference[oaicite:8]{index=8}  
- **Python standard library**: `random` (alegeri AI variate) :contentReference[oaicite:9]{index=9}  
- **HTML/CSS** prin `streamlit.components.v1.html` pentru personalizare avansată

---

## 🚀 Cum funcționează

1. **Instalare**  
   ```bash
   git clone https://github.com/USERNAME/REPO.git
   cd REPO
   pip install -r requirements.txt
