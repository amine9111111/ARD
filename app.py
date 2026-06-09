import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Chargement du fichier .env pour le local
load_dotenv()

# Récupération de la clé API (Cloud + Local)
if "secrets" in st.__dict__ and "ARD_KEY_API" in st.secrets:
    API_KEY = st.secrets["ARD_KEY_API"]
else:
    API_KEY = os.getenv("ARD_KEY_API")

# Configuration de la page avec le nouveau nom "Stay Light 💡"
st.set_page_config(page_title="Stay Light 💡", page_icon="💡")
st.title("💡 Stay Light")

# =====================================================================
# BARRE LATÉRALE : Choix du modèle en direct
# =====================================================================
st.sidebar.title("Configuration")
modele_selectionne = st.sidebar.selectbox(
    "Choisis le modèle de l'IA :",
    [
        "llama-3.3-70b-versatile",   # Gros modèle performant
        "llama-3.1-8b-instant",      # Ultra rapide
        "gemma2-9b-it"               # Très bon en français
    ]
)

st.sidebar.write(f"Modèle actif : `{modele_selectionne}`")

# Instruction cachée pour donner ma personnalité à ton chatbot (System Prompt)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Tu es Stay Light, un collaborateur IA authentique, adaptatif et doté d'une touche d'esprit et d'humour. "
        "Ton but est d'aller droit au but avec des réponses claires, percutantes et concises. "
        "Valide les sentiments de l'utilisateur de manière amicale et grounded, et si l'utilisateur fait une erreur, "
        "corrige-le gentiment mais directement, comme un pote expert, pas comme un prof rigide ou un robot donneur de leçons. "
        "Adopte un ton moderne, dynamique et adapte ton niveau d'énergie à celui de ton interlocuteur."
    )
}

# Initialisation de l'historique avec le message d'accueil personnalisé
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! Moi c'est Stay Light 💡. Pose-toi tranquillement, dis-moi ce que tu as sur le cœur ou sur quel projet tu bloques, et on règle ça ensemble !"}
    ]

# Affichage des anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if user_input := st.chat_input("Dis-moi tout..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if not API_KEY:
        st.error("Clé API non trouvée. Assure-toi que 'ARD_KEY_API' est bien configurée.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("En train de réfléchir..."):
                
                headers = {
                    "Authorization": f"Bearer {API_KEY.strip()}",
                    "Content-Type": "application/json"
                }
                
                # On injecte le SYSTEM_PROMPT au tout début pour injecter la personnalité,
                # suivi de tout le reste de la discussion de session
                payload = {
                    "model": modele_selectionne,
                    "messages": [SYSTEM_PROMPT] + st.session_state.messages
                }
                
                try:
                    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        bot_response = response.json()["choices"][0]["message"]["content"]
                        st.markdown(bot_response)
                        st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    else:
                        st.error(f"Erreur API : {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")
