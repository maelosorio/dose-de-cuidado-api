from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pwdlib import PasswordHash
from sqlmodel import Session, select

from database import criar_tabelas, get_session
from models import Usuario
from schemas import UsuarioCriar, UsuarioPublico

senha_hash = PasswordHash.recommended()


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"mensagem": "Dose de Cuidado API rodando!"}


@app.post("/usuarios", response_model=UsuarioPublico, status_code=201)
def cadastrar_usuario(dados: UsuarioCriar, session: Session = Depends(get_session)):
    # Verifica se o e-mail já está cadastrado
    existente = session.exec(
        select(Usuario).where(Usuario.email == dados.email)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=senha_hash.hash(dados.senha),
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario