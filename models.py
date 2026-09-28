from datetime import date, time
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str
    email: str
    senha: str


class Medicamento(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    usuario_id: UUID = Field(foreign_key="usuario.id")
    nome: str
    dosagem: str
    horarios: str  # exemplo: "08:00,14:00,20:00"
    frequencia: str


class Dose(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    medicamento_id: UUID = Field(foreign_key="medicamento.id")
    data: date
    hora: time
    status: str  # "concluido" ou "nao_realizado"