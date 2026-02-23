import streamlit as st
import pandas as pd
import sys
from pathlib import Path

if not st.session_state.get("logado"):
    st.warning("Make login to continue.")
    st.stop()


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from db.session import favoritar_filme, add_watch, add_review
from db.init_db import init_db

init_db()

st.set_page_config(
    layout='wide',
    page_icon='🎬'
)

df = pd.read_csv('imdb_top_1000.csv')
user = st.session_state['usuario']
with st.sidebar:
    filme = st.selectbox('select',df['Series_Title'])
    df_selecionado = df[df['Series_Title'] == filme]

col1, col2 = st.columns(2)
with col1:
    st.markdown('Movies')
with col2:
    st.markdown(f'👤 {user.name}', text_alignment='right')
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.image(df_selecionado['Poster_Link'].iloc[0], width=210)
with col2:
    st.subheader(f"{df_selecionado['Series_Title'].iloc[0]} ({df_selecionado['Released_Year'].iloc[0]})")
    st.info(f'⭐ {df_selecionado['IMDB_Rating'].iloc[0]} | {df_selecionado['Genre'].iloc[0]}')
    st.markdown(df_selecionado['Overview'].iloc[0])

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Add movie to favorites ♥️',):
        favoritar_filme(
            title=df_selecionado['Series_Title'].iloc[0],
            director=df_selecionado['Director'].iloc[0],
            genre=df_selecionado['Genre'].iloc[0],
            rating=df_selecionado['IMDB_Rating'].iloc[0],
            user_id=user.id
        )

with col3:
    if st.button('Watched 👓'):
        add_watch(
            user_id=user.id,
            title=df_selecionado["Series_Title"].iloc[0],
            watched='yes'
        )

col1, col2, col3 = st.columns(3)
    
st.subheader("⭐ Your review")

nota = st.select_slider(
    "Your review",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
)

if st.button('Save review'):
    st.success('Review saved!')
    add_review(
        user_id=user.id,
        title=df_selecionado["Series_Title"].iloc[0],
        rating=nota,
        poster_link=df_selecionado["Poster_Link"].iloc[0]
    )



st.divider()


st.subheader('Similar movies', text_alignment='center')
#filtro

genre = df_selecionado['Genre'].iloc[0]

df_genre = df[df['Genre'] == genre]

titulo_selecionado = df_selecionado["Series_Title"].iloc[0]

df_sem_filme = df[df["Series_Title"] != titulo_selecionado]

top5_genre = (
    df_sem_filme[df_sem_filme["Genre"] == genre]
    .dropna(subset=["Poster_Link"])
    .sort_values(by="IMDB_Rating", ascending=False)
    .head(5)
)
#fim filtro

cols = st.columns(5)
for col, (_, filme) in zip(cols, top5_genre.iterrows()):
    with col:
        st.image(filme["Poster_Link"], width=200)
        st.caption(filme["Series_Title"])
        st.caption(f"⭐ {filme['IMDB_Rating']}")

