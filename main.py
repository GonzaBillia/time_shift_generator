from fastapi import FastAPI
from application.routes.colaborador_routes import router as colaboradores_router

app = FastAPI(title="API de Colaboradores")

app.include_router(colaboradores_router)

@app.get("/")
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
