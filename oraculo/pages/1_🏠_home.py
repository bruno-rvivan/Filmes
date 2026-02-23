import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import sys
from pathlib import Path
from utils import get_project_root

BASE_DIR = get_project_root()
CSV_PATH = BASE_DIR / "imdb_top_1000.csv"

df = pd.read_csv(CSV_PATH)

if not st.session_state.get("logado"):
    st.warning("Make login to continue.")
    st.stop()


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from db.ai import perguntar_gpt

user = st.session_state['usuario']

st.set_page_config(
    layout='wide',
    page_icon='🏠'
)

top5 = (
    df
    .dropna(subset=["IMDB_Rating"])
    .sort_values(by="IMDB_Rating", ascending=False)
    .head(5)
)
st.header('WELCOME', text_alignment='center')

st.divider()

st.subheader('On rise🔥', text_alignment='center')

cols = st.columns(5)

for col, (_, filme) in zip(cols, top5.iterrows()):
    with col:
        st.image(filme["Poster_Link"], width=200)
        st.caption(filme["Series_Title"])
        st.caption(f"⭐ {filme['IMDB_Rating']}")
        
st.divider()


# vizualizacao do chat =======

st.title("🤖 Assistant   ")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("What's your favorite movie?")

if pergunta:
    st.session_state.chat_history.append(
        {"role": "user", "content": pergunta}
    )

    with st.chat_message("user"):
        st.markdown(pergunta)


    try:
        resposta = perguntar_gpt(
                pergunta,
                historico=st.session_state.chat_history
            )

        st.session_state.chat_history.append(
                {"role": "assistant", "content": resposta}
            )

        with st.chat_message("assistant"):
            st.markdown(resposta)

    except Exception as e:
        st.error("Connection Error.")
