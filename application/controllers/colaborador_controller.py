from fastapi import HTTPException
from infrastructure.repositories.colaborador_repo import ColaboradorRepository  # Ajusta el path según tu estructura

def get_colaborador_by_id_controller(colaborador_id: int):
    colaborador = ColaboradorRepository.get_by_id(colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador

def get_colaborador_by_legajo_controller(colaborador_legajo: int):
    colaborador = ColaboradorRepository.get_by_legajo(colaborador_legajo)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador