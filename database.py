from sqlmodel import Session, SQLModel, create_engine

import models  # noqa: F401

engine = create_engine("sqlite:///dose_de_cuidado.db")


def criar_tabelas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session