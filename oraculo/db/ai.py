from openai import OpenAI
import streamlit as st
import os
from db.database import engine
import pandas as pd

user = st.session_state['usuario']

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = st.secrets.get("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# prepara dados chat ================================================
df_reviews = pd.read_sql_table(
    table_name='reviews',
    con=engine
)
df_reviews = df_reviews[df_reviews['user_id'] == user.id].drop_duplicates(subset=["title"])

df_favs = pd.read_sql_table(
    "favorite_films",
    con=engine
)
df_favs = df_favs[df_favs['user_id'] == user.id].drop_duplicates(subset=["title"])




#FUNCS======

def perguntar_gpt(pergunta, historico=None):
    if historico is None:
        historico = []

    mensagens = [
        {"role": "system", "content": f"Você é um assistente especialista em filmes. Recomende filmes com base nas preferências do usuário, voce tem acesso a lista de filmes que ele marcou como favoritos {df_favs}, e a suas avaliacoes de filmes {df_reviews}. Sempre responda com educacao e animo, buscando sempre continuar a conversa. Todos os filmes presentes nas listas o usuario ja assistiu. responda sempre ele no mesmo idioma que ele faz as perguntas."}
    ]

    mensagens += historico
    mensagens.append({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=mensagens,
        temperature=0.7
    )

    return resposta.choices[0].message.content

def gerar_perfil_cinematografico(generos, diretores, media):
    prompt = f"""
    Com base nos dados abaixo, gere um perfil cinematográfico personalizado e profissional:

    Gêneros favoritos: {generos}
    Diretores favoritos: {diretores}
    Média das avaliações dadas: {media}

    Gere um texto curto, envolvente e analítico.
    """

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um crítico de cinema especialista em análise de perfil de público."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return resposta.choices[0].message.content