import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

if not st.session_state.get("logado"):
    st.warning("Make login to continue.")
    st.stop()


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from db.session import le_lista, engine

st.set_page_config(
    layout='wide',
    page_icon='📈'
)
user = st.session_state['usuario']

st.title('Your statatics', text_alignment='center')
st.divider()

st.subheader('Your favorites genres', text_alignment='center')
listas = le_lista(user_id=user.id)
cols = st.columns(5)
df_favs = pd.read_sql_table(
    "favorite_films",
    con=engine
)
df_favs = df_favs[df_favs['user_id'] == user.id]
df_favs = df_favs.drop_duplicates(
    subset=["title"]
)
#st.dataframe(df_favs)
contagem = df_favs['genre'].value_counts()

fig, ax = plt.subplots()

ax.bar(
    contagem.index,
    contagem.values
)

ax.set_xlabel('genres')

plt.xticks(rotation=45)

col1, col2, col3 = st.columns(3)
with col2:
    st.pyplot(fig, use_container_width=True)

st.divider()
df_watched = pd.read_sql_table(
    table_name='watcheds',
    con=engine
)
df_watched = df_watched[df_watched['user_id'] == user.id]
df_watched = df_watched.drop_duplicates(
    subset=["title"]
)
max = df_watched.count()

st.subheader(f'Congratulations! You watched {max["id"]} movies 🎬', text_alignment='center')

st.divider()

st.subheader('And your favorite movies are', text_alignment='center')
st.space()

df_reviews = pd.read_sql_table(
    table_name='reviews',
    con=engine
)

df_reviews = df_reviews[df_reviews['user_id'] == user.id]
df_reviews = df_reviews.drop_duplicates(
    subset=["title"])
tops = (
    df_reviews
    .sort_values(by="rating", ascending=False)
    .head(3)
)

cols = st.columns(3)
for col, (_, filme) in zip(cols, tops.iterrows()):
    with col:
        st.image(filme["poster_link"], width=200)
        st.caption(filme["title"])
        st.caption(f"⭐ {filme['rating']}")

st.divider()


