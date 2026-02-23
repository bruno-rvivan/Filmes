from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from streamlit import title

from db.base import Base
from db.models import Usuarios, Favorite_films, Watched, Reviws
from pathlib import Path
from db.database import engine



DB_PATH = Path(__file__).resolve().parent / "films.db"
Base.metadata.create_all(bind=engine)

#FUNCS
def estatisticas_usuario(user_id):
    with Session(bind=engine) as session:
        total_favoritos = session.query(Favorite_films).filter_by(user_id=user_id).count()
        total_watched = session.query(Watched).filter_by(user_id=user_id).count()
        media_reviews = session.query(func.avg(Reviws.rating)).filter_by(user_id=user_id).scalar()

        return total_favoritos, total_watched, media_reviews


def perfil_dados_usuario(user_id):
    with Session(bind=engine) as session:
        favoritos = session.query(Favorite_films).filter_by(user_id=user_id).all()
        reviews = session.query(Reviws).filter_by(user_id=user_id).all()

        generos = [f.genre for f in favoritos if f.genre]
        diretores = [f.director for f in favoritos if f.director]
        notas = [r.rating for r in reviews if r.rating]

        media_notas = sum(notas)/len(notas) if notas else None

        return generos, diretores, media_notas




# FUNÇÕES USER ===========================================================================================

def create_user(
        name,
        password,
        email,
):
    with Session(bind=engine) as session:
        user = Usuarios(
            name=name,
            email=email,
        )
        user.encode(password)
        session.add(user)
        session.commit()


def le_todos_users():
    with Session(bind=engine) as session:
        comando_sql = select(Usuarios)
        users = session.execute(comando_sql).fetchall()
        users = [user[0] for user in users]
        return users

def le_user_id(id):
    with Session(bind=engine) as session:
        comando_sql = select(Usuarios).filter_by(id=id)
        users = session.execute(comando_sql).fetchall()
        users = [user[0] for user in users]
        return users

def modifica_usuario(id,
                     **kwargs
                     ):
    with Session(bind=engine) as session:
        comando_sql = select(Usuarios).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            for key, value in kwargs.items():
                setattr(usuario[0], key, value)
        session.commit()

# FUNCOES FAVORITOS ========================================================================

def favoritar_filme(user_id, title, director, genre, rating):
    with Session(bind=engine) as session:
        fav = Favorite_films(
            title=title,
            director=director,
            genre=genre,
            rating=rating,
            user_id=user_id
        )
        session.add(fav)
        session.commit()

def le_lista(user_id):
    with Session(bind=engine) as session:
        comando_sql = select(Favorite_films).filter_by(user_id=user_id)
        lists = session.execute(comando_sql).fetchall()
        lists = [user[0] for user in lists]
        return lists

# WATCHED =====================================================================

def add_watch(user_id, title, watched):
    with Session(bind=engine) as session:
        watch_list = Watched(
            user_id=user_id,
            title=title,
            watched=watched
        )
        session.add(watch_list)
        session.commit()

#reviews ==========================================================================

def add_review(user_id, title, rating, poster_link):
    with Session(bind=engine) as session:
        review = Reviws(
            title=title,
            user_id=user_id,
            rating=rating,
            poster_link=poster_link
        )
        session.add(review)
        session.commit()

# teste