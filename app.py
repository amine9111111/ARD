import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ARD_KEY_API")

st.set_page_config(page_title="Carte d'identité Anime", page_icon="🎴")
st.title("🎴 Générateur de Carte d'identité Anime")

name = st.text_input("Entrez le nom de votre personnage :")
anime = st.text_input("Nom de l'anime :")
genre = st.selectbox("Genre :", ["Shonen", "Shojo", "Seinen", "Isekai", "Comédie", "Horreur", "Romance", "Autre"])
personnalite = st.text_area("Décris sa personnalité :", max_chars=150)

if st.button("🎨 Générer la carte"):
    if not API_KEY:
        st.error("Clé API non trouvée. Assure-toi que 'ARD_KEY_API' est bien définie dans le fichier .env.")
    elif name and anime and personnalite:
        with st.spinner("Génération de la fiche..."):
            prompt = f"Génère une carte d'identité d'un personnage d'anime nommé {name} venant de l'anime {anime}. Il est de genre {genre}. Voici sa personnalité : {personnalite}. Donne-moi une fiche stylée avec son nom, son anime, ses stats, une courte biographie et une catchphrase stylée."
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                st.markdown("## 💳 Carte d'identité :")
                st.markdown(content)
            else:
                st.error("Erreur lors de l'appel à l'API.")

    else:
        st.warning("Remplis tous les champs avant de générer.")