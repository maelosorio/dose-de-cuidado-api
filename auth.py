import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from database import get_session
from models import Usuario

# Em produção (Render) essa chave vem de uma variável de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "chave-so-para-desenvolvimento")
ALGORITHM = "HS256"
EXPIRA_EM_MINUTOS = 60

seguranca = HTTPBearer()


def criar_token(usuario_id: UUID) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_EM_MINUTOS)
    dados = {"sub": str(usuario_id), "exp": expira}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca),
    session: Session = Depends(get_session),
) -> Usuario:
    try:
        dados = jwt.decode(credenciais.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = UUID(dados["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario