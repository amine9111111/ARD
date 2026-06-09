import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Chargement du fichier .env pour le local
load_dotenv()

# =====================================================================
# CHANGER DE MODÈLE ICI 
# Tu as juste à remplacer le nom entre guillemets par celui de ton choix !
# Exemples dispos chez Groq : "mixtral-8x7b-32768", "gemma2-9b-it", "llama3-8b-8192"
# =====================================================================
MODELE_CHOISI = "mixtral-8x7b-32768" 

# Récupération de la clé API (Cloud + Local)
if "secrets" in st.__dict__ and "ARD_KEY_API" in st.secrets:
    API_KEY = st.secrets["ARD_KEY_API"]
else:
    API_KEY = os.getenv("ARD_KEY_API")

st.set_page_config(page_title="Mon Chatbot AI", page_icon="🤖")
st.title("🤖 Mon Chatbot Personnalisable")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Salut ! Je suis ton assistant IA running sur {MODELE_CHOISI}. Comment puis-je t'aider ?"}
    ]

# Affichage des anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if user_input := st.chat_input("Écris ton message ici..."):
    
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
                
                # Le payload utilise la variable définie tout en haut
                payload = {
                    "model": MODELE_CHOISI,
                    "messages": st.session_state.messages
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
