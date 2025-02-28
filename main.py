from fastapi import FastAPI
from application.routes.colaborador_routes import router as colaboradores_router
from application.routes.tipo_colaborador_routes import router as tipo_colaboradores_router
from application.routes.empresa_routes import router as empresas_router
from application.routes.dia_routes import router as dias_router
from application.config.logger_config import setup_logger

logger = setup_logger(__name__)
logger.info("Logger configurado correctamente")

app = FastAPI(title="API de Colaboradores")

app.include_router(colaboradores_router)
app.include_router(empresas_router)
app.include_router(dias_router)
app.include_router(tipo_colaboradores_router)

@app.get("/")
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
