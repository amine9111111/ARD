import streamlit as st

st.title("🔥 Les jeux vidéo les plus difficiles (accès sécurisé)")

# Récupérer la clé API depuis les secrets Streamlit
SECRET_API_KEY = st.secrets["ARD_KEY_API"]

# Champ pour entrer la clé
key_input = st.text_input("Entrez votre clé API pour accéder à l'app :", type="password")

jeux_difficiles = {
    "Dark Souls": {
        "description": "Un RPG exigeant où chaque erreur peut être fatale. Combats punitifs et exploration complexe.",
        "difficulte": 9.5
    },
    "Cuphead": {
        "description": "Un run & gun avec des boss très techniques et une exigence parfaite dans les réflexes.",
        "difficulte": 9.0
    },
    "Sekiro: Shadows Die Twice": {
        "description": "Un jeu d'action avec un système de combat punitif demandant timing et précision extrêmes.",
        "difficulte": 9.7
    },
    "Celeste": {
        "description": "Un jeu de plateforme précis où chaque saut doit être parfaitement maîtrisé.",
        "difficulte": 8.8
    },
    "Bloodborne": {
        "description": "Similaire à Dark Souls mais avec un gameplay plus agressif et des ennemis très agressifs.",
        "difficulte": 9.3
    },
    "Ninja Gaiden": {
        "description": "Un classique du jeu d’action réputé pour ses combats difficiles et ses ennemis redoutables.",
        "difficulte": 9.2
    },
    "Super Meat Boy": {
        "description": "Plateforme rapide et exigeante où les réflexes sont essentiels.",
        "difficulte": 8.9
    }
}

if key_input:
    if key_input == SECRET_API_KEY:
        jeu_choisi = st.selectbox("Choisis un jeu difficile :", list(jeux_difficiles.keys()))
        if jeu_choisi:
            st.subheader(jeu_choisi)
            st.write(jeux_difficiles[jeu_choisi]["description"])
            st.write(f"Note de difficulté : {jeux_difficiles[jeu_choisi]['difficulte']} / 10")
    else:
        st.error("Clé API incorrecte, accès refusé.")
else:
    st.info("Veuillez entrer votre clé API pour accéder à l'app.")
