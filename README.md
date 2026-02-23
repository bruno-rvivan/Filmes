# 🎬 Movie AI Dashboard

Aplicação web desenvolvida com **Streamlit**, **SQLAlchemy** e **OpenAI API** para gerenciamento e análise de preferências cinematográficas.

O sistema permite que usuários criem conta, salvem filmes favoritos, avaliem filmes e recebam recomendações personalizadas com Inteligência Artificial.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Criação de conta
- Login seguro com hash de senha (Passlib)

### ⭐ Sistema de Favoritos
- Adicionar filmes aos favoritos
- Marcar como assistido
- Avaliar filmes

### 📊 Dashboard Inteligente
- Total de favoritos
- Total assistidos
- Média das avaliações
- Gráfico de gêneros favoritos
- Top 5 diretores

### 🤖 Assistente com IA (GPT-4.1-mini)
- Chat interativo sobre filmes
- Recomendações personalizadas
- Perfil cinematográfico gerado automaticamente com base nos dados do usuário

---

## 🛠 Tecnologias Utilizadas

- Python
- Streamlit
- SQLAlchemy
- SQLite
- OpenAI API
- Pandas
- Matplotlib
- Passlib

---

## 📂 Estrutura do Projeto

├── db/
│ ├── models.py
│ ├── session.py
│ ├── ai.py
│
├── pages/
│ ├── login.py
│ ├── movie.py
│ ├── graphs.py
│ ├── user.py
│
├── imdb_top_1000.csv
├── requirements.txt
├── README.md

---

## ⚙️ Como Rodar Localmente

Clone o repositório:

```bash
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio

Instale as dependências:

pip install -r requirements.txt

Configure a chave da OpenAI:

Crie o arquivo:

.streamlit/secrets.toml

E adicione:

OPENAI_API_KEY="sua_chave"

Execute a aplicação:

streamlit run app.py

🌐 Deploy

Aplicação preparada para deploy no Streamlit Cloud.

Basta configurar a variável de ambiente:

OPENAI_API_KEY
🎯 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:

Estruturação de aplicação web com backend em Python

Integração com banco de dados relacional

Uso de ORM (SQLAlchemy)

Implementação de autenticação segura

Integração com modelos de linguagem (LLM)

Visualização de dados

👨‍💻 Autor

Bruno Rech Vivan
Projeto desenvolvido para evolução técnica e portfólio profissional.# Filmes
