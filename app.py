import streamlit as st
import requests

st.title("🎮 Jeux Vidéo Difficiles - RAWG API")

# Récupérer la clé API depuis secrets
API_KEY = st.secrets["ARD_KEY_API"]

def chercher_jeux(query):
    url = f"https://api.rawg.io/api/games"
    params = {
        "key": API_KEY,
        "search": query,
        "ordering": "-rating",
        "page_size": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error(f"Erreur API: {response.status_code}")
        return []

query = st.text_input("Recherche un jeu (ex: Dark Souls) :")

if query:
    jeux = chercher_jeux(query)
    if jeux:
        for jeu in jeux:
            st.subheader(jeu["name"])
            st.image(jeu["background_image"], width=400)
            st.write(f"Note moyenne : {jeu['rating']}/5")
            st.write(f"Sorti le : {jeu['released']}")
            st.write(jeu["slug"])
            st.markdown("---")
    else:
        st.write("Aucun jeu trouvé.")
else:
    st.write("Tape un nom de jeu pour commencer la recherche.")
