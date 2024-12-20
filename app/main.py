from fastapi import FastAPI
from app.routes import cep, download


app = FastAPI()

app.include_router(cep.router)
app.include_router(download.router, prefix="/download")

app.get("/")
def home():
    return {"message": "Bem-vindo à Central de Consultas de CEPs"}
