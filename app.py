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

# Configuration de la page
st.set_page_config(page_title="Stay Light 💡", page_icon="💡", layout="centered")

# Injection CSS via st.html en une seule ligne pour éviter les bugs sur Streamlit Cloud
st.html("<style>.block-container { padding-top: 2rem; max-width: 800px; } .stChatMessage { border-radius: 15px; margin-bottom: 10px; }</style>")

# =====================================================================
# SIDEBAR (Configuration cachée sur le côté)
# =====================================================================
st.sidebar.title("⚙️ Configuration")
modele_selectionne = st.sidebar.selectbox(
    "Modèle de l'IA :",
    [
        "llama-3.3-70b-versatile",   
        "llama-3.1-8b-instant",      
        "gemma2-9b-it"               
    ]
)
st.sidebar.caption(f"Propulsé par Groq • Modèle actif : `{modele_selectionne}`")

# =====================================================================
# EN-TÊTE DE L'APPLICATION
# =====================================================================
st.title("💡 Stay Light")
st.caption("Ton assistant IA authentique, direct et avec un brin d'humour.")

# Personnalité de Stay Light (System Prompt)
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

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Message d'accueil si la discussion commence à peine
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="💡"):
        st.markdown("Salut ! Moi c'est **Stay Light** 💡. Pose-toi tranquillement, dis-moi ce que tu as sur le cœur ou sur quel projet tu bloques, et on règle ça ensemble !")
    
    # Suggestions d'action rapide mises à jour
    st.markdown("### 🚀 Quelques idées pour commencer :")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Aide-moi à réviser des choses basiques 🧠"):
            st.session_state.prompt_automatique = "Aide-moi à réviser des notions de base et des sujets importants (comme le français, les maths ou l'histoire)."
            st.rerun()
    with col2:
        if st.button("Aide-moi à réviser mon Brevet 📝"):
            st.session_state.prompt_automatique = "Donne-moi des conseils et une méthode efficace pour réviser mon Brevet"
            st.rerun()

# Affichage des messages de l'historique
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "💡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Gestion des suggestions ou de l'entrée classique
if "prompt_automatique" in st.session_state:
    user_input = st.session_state.pop("prompt_automatique")
else:
    user_input = st.chat_input("Dis-moi tout...")

# Traitement du message
if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if not API_KEY:
        st.error("Clé API manquante dans tes configurations.")
    else:
        with st.chat_message("assistant", avatar="💡"):
            with st.spinner("Stay Light réfléchit..."):
                headers = {
                    "Authorization": f"Bearer {API_KEY.strip()}",
                    "Content-Type": "application/json"
                }
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
                        st.error(f"Erreur API : {response.status_code}")
                except Exception as e:
                    st.error(f"Erreur réseau : {e}")
