import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from db.session import le_todos_users, create_user
from db.init_db import init_db

init_db()

st.set_page_config(
    layout='wide',
    page_icon='📝'
)

st.session_state['criando'] = False
st.session_state['logado'] = False

st.title('Welcome')

def login():
    with st.container(border=True):
        usuarios = le_todos_users()
        usuarios = {usuario.name: usuario for usuario in usuarios}
        name = st.selectbox(
        'User',
            list(usuarios.keys()
                 )
        )
        password = st.text_input('password', type="password")
        if st.button('Login'):
            user = usuarios[name]
            if user.desencode(senha=password):
                st.success('Login completed')
                st.session_state['usuario'] = user
                st.session_state['id'] = user.id
                st.session_state['logado'] = True
            else:
                st.error('Incorect Password')

# Create account

def create():
    with st.container(border=True):
        st.markdown('Create account')
        name = st.text_input('Username')
        password = st.text_input('Password')
        email = st.text_input('Email')
        if st.button('Create'):
            create_user(name=name,
                        password=password,
                        email=email
            )
            st.success('Account created')


if __name__ == '__main__':
    with st.sidebar:
        option = st.selectbox('Options', ['Login', 'Create'])
    if option == 'Login':
        login()
    else:
        create()
