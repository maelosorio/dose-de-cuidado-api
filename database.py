from sqlmodel import SQLModel, create_engine

import models  # noqa: F401  (precisa importar pra o SQLModel conhecer as tabelas)

engine = create_engine("sqlite:///dose_de_cuidado.db")


def criar_tabelas():
    SQLModel.metadata.create_all(engine)