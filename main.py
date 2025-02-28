from fastapi import FastAPI
from application.routes.colaborador_routes import router as colaboradores_router
from application.routes.tipo_colaborador_routes import router as tipo_colaboradores_router
from application.routes.horario_sucursal_routes import router as horario_sucursal_router
from application.routes.formatos_roles_routes import router as formatos_roles_router
from application.routes.espacio_disponible_sucursal_routes import router as espacio_disponible_sucursal_router
from application.routes.horas_extra_colaborador_routes import router as horas_extra_colaborador_router
from application.routes.horario_routes import router as horarios_router
from application.routes.sucursal_routes import router as sucursal_routes
from application.routes.empresa_routes import router as empresas_router
from application.routes.rol_routes import router as roles_router
from application.routes.dia_routes import router as dias_router
from application.routes.formato_routes import router as formatos_router

from application.config.logger_config import setup_logger

logger = setup_logger(__name__)
logger.info("Logger configurado correctamente")

app = FastAPI(title="API de Colaboradores")

app.include_router(colaboradores_router)
app.include_router(espacio_disponible_sucursal_router)
app.include_router(horas_extra_colaborador_router)
app.include_router(horario_sucursal_router)
app.include_router(empresas_router)
app.include_router(formatos_roles_router)
app.include_router(sucursal_routes)
app.include_router(horarios_router)
app.include_router(dias_router)
app.include_router(roles_router)
app.include_router(formatos_router)
app.include_router(tipo_colaboradores_router)

@app.get("/")
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
