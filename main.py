from fastapi import FastAPI
from application.routes.colaborador_routes import router as colaboradores_router
from application.routes.tipo_colaborador_routes import router as tipo_colaboradores_router
from application.routes.horario_sucursal_routes import router as horario_sucursal_router
from application.routes.formatos_roles_routes import router as formatos_roles_router
from application.routes.espacio_disponible_sucursal_routes import router as espacio_disponible_sucursal_router
from application.routes.horas_extra_colaborador_routes import router as horas_extra_colaborador_router
from application.routes.minimo_puestos_routes import router as minimo_puestos_router
from application.routes.puestos_cubiertos_por_hora_routes import router as puestos_cubiertos_router
from application.routes.horario_preferido_colaborador_routes import router as horario_preferido_colaborador_router
from application.routes.auth_routes import router as auth_router
from application.routes.usuario_routes import router as usuario_router
from application.routes.vta_hora_routes import router as vta_hora_router
from application.routes.horario_routes import router as horarios_router
from application.routes.sucursal_routes import router as sucursal_routes
from application.routes.empresa_routes import router as empresas_router
from application.routes.rol_routes import router as roles_router
from application.routes.dia_routes import router as dias_router
from application.routes.formato_routes import router as formatos_router

from fastapi.middleware.cors import CORSMiddleware

from application.config.logger_config import setup_logger

logger = setup_logger(__name__)
logger.info("Logger configurado correctamente")

app = FastAPI(title="API de Colaboradores")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(colaboradores_router)
app.include_router(espacio_disponible_sucursal_router)
app.include_router(horas_extra_colaborador_router)
app.include_router(puestos_cubiertos_router)
app.include_router(horario_sucursal_router)
app.include_router(empresas_router)
app.include_router(formatos_roles_router)
app.include_router(sucursal_routes)
app.include_router(horarios_router)
app.include_router(dias_router)
app.include_router(roles_router)
app.include_router(formatos_router)
app.include_router(tipo_colaboradores_router)
app.include_router(horario_preferido_colaborador_router)
app.include_router(minimo_puestos_router)
app.include_router(vta_hora_router)
app.include_router(auth_router)
app.include_router(usuario_router)

@app.get("/")
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
