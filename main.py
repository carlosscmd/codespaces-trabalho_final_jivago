from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)   # cria as tabelas no Supabase
    yield

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')                               # raiz → redireciona para a lista
def home():
    return RedirectResponse(url='/livros')
# READ — lista todos os filmes
@app.get('/livros')
def listar(request: Request, session: Session = Depends(get_session)):
    livros = session.scalars(select(models.Livro)).all()
    return templates.TemplateResponse(request, 'lista.html', {'livros': livros})

# CREATE — formulário vazio
@app.get('/livros/novo')
def form_novo(request: Request):
    return templates.TemplateResponse(request, 'form.html', {'livro': None})

# CREATE — grava no banco
@app.post('/livros')
def criar(
    titulo: str = Form(...), autor: str = Form(...), ano: int = Form(...),
    genero: str = Form(...), nota: float = Form(0), lido: bool = Form(False),
    session: Session = Depends(get_session),
):
    livro = models.Livro(titulo=titulo, autor=autor, ano=ano,
                         genero=genero, nota=nota, lido=lido)
    session.add(livro)
    session.commit()
    return RedirectResponse(url='/livros', status_code=303)
# UPDATE — formulário preenchido
@app.get('/livros/{livro_id}/editar')
def form_editar(livro_id: int, request: Request, session: Session = Depends(get_session)):
    livro = session.get(models.Livro, livro_id)
    return templates.TemplateResponse(request, 'form.html', {'livro': livro})

# UPDATE — salva as alterações
@app.post('/livros/{livro_id}/editar')
def atualizar(
    livro_id: int,
    titulo: str = Form(...), autor: str = Form(...), ano: int = Form(...),
    genero: str = Form(...), nota: float = Form(0), lido: bool = Form(False),
    session: Session = Depends(get_session),
):
    livro = session.get(models.Livro, livro_id)
    livro.titulo, livro.autor, livro.ano = titulo, autor, ano
    livro.genero, livro.nota, livro.lido = genero, nota, lido
    session.commit()
    return RedirectResponse(url='/livros', status_code=303)

# DELETE — remove do banco
@app.post('/livros/{livro_id}/excluir')
def excluir(livro_id: int, session: Session = Depends(get_session)):
    livro = session.get(models.Livro, livro_id)
    session.delete(livro)
    session.commit()
    return RedirectResponse(url='/livros', status_code=303)

