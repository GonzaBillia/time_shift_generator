from fastapi import FastAPI
from application.routes.colaborador_routes import router as colaboradores_router
from application.config.logger_config import setup_logger

logger = setup_logger(__name__)
logger.info("Logger configurado correctamente")

app = FastAPI(title="API de Colaboradores")

app.include_router(colaboradores_router)

@app.get("/")
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
