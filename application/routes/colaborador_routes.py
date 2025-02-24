from fastapi import APIRouter
from application.controllers.colaborador_controller import get_colaborador_by_id_controller, get_colaborador_by_legajo_controller

router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@router.get("/id/{colaborador_id}")
def get_colaborador(colaborador_id: int):
    return get_colaborador_by_id_controller(colaborador_id)

@router.get("/legajo/{colaborador_legajo}")
def get_colaborador(colaborador_legajo: int):
    return get_colaborador_by_legajo_controller(colaborador_legajo)
