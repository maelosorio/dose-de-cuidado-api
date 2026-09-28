from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pwdlib import PasswordHash
from sqlmodel import Session, select

from auth import criar_token, get_usuario_atual
from database import criar_tabelas, get_session
from models import Medicamento, Usuario
from schemas import (
    MedicamentoCriar,
    MedicamentoPublico,
    UsuarioCriar,
    UsuarioLogin,
    UsuarioPublico,
)

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


@app.post("/login")
def login(dados: UsuarioLogin, session: Session = Depends(get_session)):
    usuario = session.exec(
        select(Usuario).where(Usuario.email == dados.email)
    ).first()

    # Mesma mensagem para e-mail ou senha errados (não revela qual dos dois falhou)
    if not usuario or not senha_hash.verify(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    return {
        "mensagem": "Login realizado com sucesso",
        "access_token": criar_token(usuario.id),
        "token_type": "bearer",
    }


@app.post("/medicamentos", response_model=MedicamentoPublico, status_code=201)
def cadastrar_medicamento(
    dados: MedicamentoCriar,
    usuario: Usuario = Depends(get_usuario_atual),
    session: Session = Depends(get_session),
):
    medicamento = Medicamento(
        usuario_id=usuario.id,
        nome=dados.nome,
        dosagem=dados.dosagem,
        horarios=dados.horarios,
        frequencia=dados.frequencia,
    )
    session.add(medicamento)
    session.commit()
    session.refresh(medicamento)
    return medicamento