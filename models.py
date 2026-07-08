from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Genero(Base):
    __tablename__ = 'generos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    livros: Mapped[list['Livro']] = relationship(back_populates='genero')

class Livro(Base):
    __tablename__ = 'livros'
    id: Mapped[int] = mapped_column(primary_key=True)   # chave primária
    titulo: Mapped[str]                                 # obrigatório
    autor: Mapped[str]
    ano: Mapped[int]
    nota: Mapped[float] = mapped_column(default=0)      # 0 a 10
    lido: Mapped[bool] = mapped_column(default=False)
    genero_id: Mapped[int] = mapped_column(ForeignKey('generos.id'))   # FK
    genero: Mapped['Genero'] = relationship(back_populates='livros')
