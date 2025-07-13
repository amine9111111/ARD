import streamlit as st
import random
import string

# Exemple réduit — remplace par ta vraie liste de 500 animés
anime_list = [
    "Attack on Titan",
    "Bleach",
    "Code Geass",
    "Death Note",
    "Evangelion",
    "Fullmetal Alchemist",
    "Gintama",
    "Haikyuu",
    "Inuyasha",
    "Jujutsu Kaisen",
    "K-On!",
    "Love Live!",
    "Mob Psycho 100",
    "Naruto",
    "One Piece",
    "Pokemon",
    "Queen’s Blade",
    "Re:Zero",
    "Sword Art Online",
    "Tokyo Ghoul",
    "Your Lie in April",
]

st.title("🎯 Devine l'anime !")

# Tirer un anime au hasard et garder en session
if "anime_courant" not in st.session_state:
    st.session_state.anime_courant = random.choice(anime_list)

anime_courant = st.session_state.anime_courant
lettre_indice = anime_courant[0].upper()

st.write(f"L'anime commence par la lettre : **{lettre_indice}**")

# Saisie utilisateur
reponse = st.text_input("Devine le nom complet de l'anime:")

if st.button("Valider"):
    if reponse.strip().lower() == anime_courant.lower():
        st.success("Bravo, c'est la bonne réponse ! 🎉")
        # Recommencer avec un autre anime
        st.session_state.anime_courant = random.choice(anime_list)
    else:
        st.error("Non, essaie encore !")

if st.button("Changer d'anime"):
    st.session_state.anime_courant = random.choice(anime_list)
    st.experimental_rerun()
