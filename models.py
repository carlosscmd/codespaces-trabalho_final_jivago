from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(primary_key=True)   # chave primária
    titulo: Mapped[str]                                 # obrigatório
    autor: Mapped[str]
    ano: Mapped[int]
    genero: Mapped[str]                                 # por enquanto, texto
    nota: Mapped[float] = mapped_column(default=0)      # 0 a 10
    lido: Mapped[bool] = mapped_column(default=False)
