from datetime import date, time
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


class MedicamentoCriar(SQLModel):
    nome: str
    dosagem: str
    horarios: str  # exemplo: "08:00,14:00,20:00"
    frequencia: str


class MedicamentoPublico(SQLModel):
    id: UUID
    usuario_id: UUID
    nome: str
    dosagem: str
    horarios: str
    frequencia: str


class DoseConfirmar(SQLModel):
    data: date
    hora: time


class DosePublico(SQLModel):
    id: UUID
    medicamento_id: UUID
    data: date
    hora: time
    status: str