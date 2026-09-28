from uuid import UUID

from sqlmodel import SQLModel


class UsuarioCriar(SQLModel):
    nome: str
    email: str
    senha: str


class UsuarioLogin(SQLModel):
    email: str
    senha: str


class UsuarioPublico(SQLModel):
    id: UUID
    nome: str
    email: str