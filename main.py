from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import criar_tabelas


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"mensagem": "Dose de Cuidado API rodando!"}