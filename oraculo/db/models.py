from sqlalchemy import String, Integer, Float,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from passlib.hash import pbkdf2_sha256

class Usuarios(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    def encode(self, senha):
        self.password = pbkdf2_sha256.hash(senha)

    def desencode(self, senha):
        return pbkdf2_sha256.verify(senha, self.password)

    def __repr__(self):
        return f"usuario {self.id} - {self.name} - {self.email}"

class Favorite_films(Base):
    __tablename__ = "favorite_films"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    director: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))


class Watched(Base):
    __tablename__ = "watcheds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    watched: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

class Reviws(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    poster_link: Mapped[str] = mapped_column(String, nullable=False)
