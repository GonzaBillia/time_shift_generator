from fastapi import APIRouter
from application.controllers.colaborador_controller import get_colaborador_by_id_controller, get_colaborador_by_legajo_controller
from application.helpers.response_handler import error_response, success_response


router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@router.get("/id/{colaborador_id}")
def get_colaborador(colaborador_id: int):
    try:
        colaborador = get_colaborador_by_id_controller(colaborador_id)
        # Si estás usando Pydantic para serializar, podrías hacer:
        # return success_response("Colaborador encontrado", data=ColaboradorSchema.from_orm(colaborador).dict())
        # Aquí se asume que `colaborador` es un diccionario o se convierte a uno:
        return success_response("Colaborador encontrado", data=colaborador.__dict__)
    except Exception as e:
        return error_response(str(e), status_code=404)

@router.get("/legajo/{colaborador_legajo}")
def get_colaborador(colaborador_legajo: int):
    try:
        colaborador = get_colaborador_by_legajo_controller(colaborador_legajo)

        return success_response("Colaborador encontrado", data=colaborador.__dict__)
    except Exception as e:
        return error_response(str(e), status_code=404)

