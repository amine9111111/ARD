import streamlit as st
import requests

st.set_page_config(page_title="Carte Anime avec Groq", page_icon="🎴")
st.title("🎴 Générateur de carte d'identité Anime avec Groq")

API_KEY = st.secrets.get("ARD_KEY_API")

name = st.text_input("Nom du personnage :")
anime = st.text_input("Nom de l'anime :")
genre = st.selectbox("Genre :", ["Shonen", "Shojo", "Seinen", "Isekai", "Comédie", "Horreur", "Romance", "Autre"])
traits = st.multiselect("Traits de personnalité :", ["Courageux", "Intelligent", "Drôle", "Sérieux", "Mystérieux", "Gentil", "Impulsif", "Loyal"])

if st.button("Générer la carte"):
    if not API_KEY:
        st.error("Clé API Groq introuvable dans les secrets.")
    elif not (name and anime and traits):
        st.warning("Merci de remplir tous les champs.")
    else:
        prompt = (
            f"Génère une carte d'identité stylée pour un personnage d'anime nommé {name}, "
            f"de l'anime {anime}, genre {genre}. "
            f"Ses traits de personnalité : {', '.join(traits)}. "
            "Donne-moi nom, anime, stats, biographie courte, catchphrase."
        )
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            st.markdown("## 💳 Carte d'identité :")
            st.markdown(content)
        else:
            st.error(f"Erreur API : {response.status_code} - {response.text}")
