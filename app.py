import streamlit as st
import requests

st.title("📺 Liste d'animes par lettre")

lettre = st.text_input("Entrez une lettre (A-Z) :", max_chars=1).upper()

if lettre and lettre.isalpha():
    query = '''
    query ($search: String) {
      Page(page: 1, perPage: 10) {
        media(search: $search, type: ANIME) {
          id
          title {
            romaji
            english
          }
          genres
          description(asHtml: false)
          episodes
          averageScore
        }
      }
    }
    '''
    # On cherche animes dont le titre contient la lettre en début
    variables = {"search": lettre}
    
    response = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        animes = response.json()['data']['Page']['media']
        if animes:
            for anime in animes:
                st.subheader(anime['title']['romaji'])
                st.markdown(f"**Anglais :** {anime['title']['english'] or 'N/A'}")
                st.markdown(f"**Genres :** {', '.join(anime['genres'])}")
                st.markdown(f"**Épisodes :** {anime['episodes'] or 'N/A'}")
                st.markdown(f"**Note moyenne :** {anime['averageScore'] or 'N/A'}")
                st.markdown("---")
        else:
            st.info("Aucun anime trouvé pour cette lettre.")
    else:
        st.error(f"Erreur API : {response.status_code}")
else:
    st.info("Entre une lettre valide pour commencer la recherche.")
