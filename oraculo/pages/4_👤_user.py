import streamlit as st
from pathlib import Path
import sys
import pandas as pd

if not st.session_state.get("logado"):
    st.warning("Make login to continue.")
    st.stop()


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from db.session import engine, modifica_usuario, perfil_dados_usuario
from db.ai import gerar_perfil_cinematografico

user = st.session_state['usuario']
st.set_page_config(
    layout='centered',
    page_icon='👤'
)
df_favs = pd.read_sql_table(
    "favorite_films",
    con=engine
)
df_favs = df_favs[df_favs['user_id'] == user.id].drop_duplicates(subset=["title"])


st.title('Profile', text_alignment='center')
st.divider()
st.space()
st.subheader('Account', text_alignment='center')

st.markdown(f'Username: {user.name}')
st.markdown(f'email: {user.email}')
if st.button('Change'):
    name = st.text_input('New username')
    email = st.text_input('New email')
    if st.button('Save'):
        modifica_usuario(
                name=name,
                email=email
        )
st.divider()
st.subheader('Favorites genres', text_alignment='center')
df_favs
contagem = df_favs['genre'].value_counts().head(3)
st.write(contagem.index)

st.divider()
st.subheader("🎥 Seu Perfil Cinematográfico")

generos, diretores, media = perfil_dados_usuario(user.id)

if generos:
    with st.spinner("Analisando seu perfil..."):
        texto = gerar_perfil_cinematografico(generos, diretores, media)

    st.success(texto)

else:
    st.info("Adicione favoritos para gerar seu perfil.")