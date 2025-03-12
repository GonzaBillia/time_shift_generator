from datetime import date, time
from typing import List, Dict
from infrastructure.repositories import (
    colaborador_repo,
    colaborador_sucursal_repo,
    horario_preferido_colaborador_repo,
    empresas_repo,
    horario_repo,
    horas_extra_colaborador_repo,
    vacacion_colaborador_repo,
    tipo_colaborador_repo,
    rol_repo
)
from application.controllers.sucursal_controller import controlador_py_logger_get_by_id_sucursal
from domain.models.colaborador import Colaborador
from domain.models.tipo_colaborador import TipoEmpleado
from domain.models.rol import Rol
from application.services.horario_service import crear_horario, crear_horario_preferido, convertir_horario_a_dict
from infrastructure.schemas.horario import HorarioResponse
from infrastructure.schemas.horario_preferido_colaborador import HorarioPreferidoColaboradorResponse

colaborador_repo = colaborador_repo.ColaboradorRepository()
colaborador_sucursal_repo = colaborador_sucursal_repo.ColaboradorSucursalRepository()
horario_preferido_colaborador_repo = horario_preferido_colaborador_repo.HorarioPreferidoColaboradorRepository()
horario_repo = horario_repo.HorarioRepository()
horas_extra_colaborador_repo = horas_extra_colaborador_repo.HorasExtraColaboradorRepository()
vacacion_colaborador_repo = vacacion_colaborador_repo.VacacionColaboradorRepository()
tipo_colaborador_repo = tipo_colaborador_repo.TipoEmpleadoRepository()
rol_repo = rol_repo.RolRepository()
empresas_repo = empresas_repo.EmpresaRepository()

def get_colaborador_details(colaborador_id: int) -> Colaborador:
    # Obtener datos básicos del colaborador.
    colaborador_data = colaborador_repo.get_by_id(colaborador_id)
    if not colaborador_data:
        raise ValueError("Colaborador no encontrado")
    
    # Obtener sucursales y roles asociados.
    colaborador_sucursales = colaborador_sucursal_repo.get_by_colaborador(colaborador_id)
    sucursales = [controlador_py_logger_get_by_id_sucursal(cs.sucursal_id) for cs in colaborador_sucursales]
    roles = [rol_repo.get_by_id(cs.rol_colaborador_id) for cs in colaborador_sucursales]
    empresa = empresas_repo.get_by_id(colaborador_data.empresa_id)

    # --- Procesar horarios preferidos ---
    horario_preferido_data = horario_preferido_colaborador_repo.get_by_colaborador(colaborador_id)
    # Se construye una lista de HorarioPreferidoColaboradorResponse
    horario_preferido_response: List[HorarioPreferidoColaboradorResponse] = []
    dias_preferidos: List[int] = []
    for hp in horario_preferido_data:
        try:
            # Crear el objeto Horario para el horario preferido (sin fecha)
            h = crear_horario_preferido(
                sucursal_id=hp.sucursal_id,  # Usar el valor real de la DB
                colaborador_id=colaborador_id,
                dia_id=hp.dia_id,
                hora_inicio=hp.hora_inicio,
                hora_fin=hp.hora_fin,
                horario_corrido=hp.horario_corrido
            )
            # Extraer el primer bloque y construir el diccionario requerido.
            hora_inicio_obj, hora_fin_obj = h.bloques[0]
            h_dict = {
                "id": hp.id,
                "colaborador_id": h.colaborador_id,
                "sucursal_id": h.sucursal_id,
                "hora_inicio": hora_inicio_obj.isoformat() if hasattr(hora_inicio_obj, "isoformat") else hora_inicio_obj,
                "hora_fin": hora_fin_obj.isoformat() if hasattr(hora_fin_obj, "isoformat") else hora_fin_obj,
                "dia_id": h.dia_id,
                "horario_corrido": h.horario_corrido,
            }
            # Validar y transformar el diccionario al modelo de respuesta.
            h_response = HorarioPreferidoColaboradorResponse.model_validate(h_dict)
        except ValueError as e:
            raise ValueError(f"Error en horario preferido: {e}")
        horario_preferido_response.append(h_response)

        # Generar los días preferidos a partir de los horarios preferidos
        dias_preferidos = [hp.dia_id for hp in horario_preferido_response]
    
    # --- Procesar horarios asignados ---
    horario_asignado_data = horario_repo.get_by_colaborador(colaborador_id)
    # Se construye una lista de HorarioResponse
    horario_asignado_response: List[HorarioResponse] = []
    for ha in horario_asignado_data:
        try:
            h = crear_horario(
                sucursal_id=ha.sucursal_id,
                colaborador_id=colaborador_id,
                dia_id=ha.dia_id,
                fecha=ha.fecha,
                hora_inicio=ha.hora_inicio,
                hora_fin=ha.hora_fin,
                horario_corrido=ha.horario_corrido
            )
            hora_inicio_obj, hora_fin_obj = h.bloques[0]
            h_dict = {
                "id": ha.id,
                "colaborador_id": h.colaborador_id,
                "sucursal_id": h.sucursal_id,
                "hora_inicio": hora_inicio_obj.isoformat() if hasattr(hora_inicio_obj, "isoformat") else hora_inicio_obj,
                "hora_fin": hora_fin_obj.isoformat() if hasattr(hora_fin_obj, "isoformat") else hora_fin_obj,
                "dia_id": h.dia_id,
                "horario_corrido": h.horario_corrido,
                "fecha": h.fecha.isoformat() if h.fecha and hasattr(h.fecha, "isoformat") else h.fecha,
            }
            h_response = HorarioResponse.model_validate(h_dict)
        except ValueError as e:
            raise ValueError(f"Error en horario asignado: {e}")
        horario_asignado_response.append(h_response)
    
    # --- Procesar horas extra ---
    hs_extra_data = horas_extra_colaborador_repo.get_by_colaborador(colaborador_id)
    hs_extra: Dict[str, int] = {}
    for he in hs_extra_data:
        hs_extra[he.tipo] = hs_extra.get(he.tipo, 0) + he.cantidad

    # --- Procesar vacaciones ---
    vacaciones_data = vacacion_colaborador_repo.get_by_colaborador(colaborador_id)
    vacaciones = [v.fecha for v in vacaciones_data]

    # --- Procesar tipo de empleado ---
    tipo_empleado_data = tipo_colaborador_repo.get_by_id(colaborador_data.tipo_empleado_id)
    tipo_empleado = TipoEmpleado(
        id=tipo_empleado_data.id,
        tipo=tipo_empleado_data.tipo,
        horas_por_dia_max=tipo_empleado_data.horas_por_dia_max,
        horas_semanales=tipo_empleado_data.horas_semanales
    )

    # Construir y retornar la instancia del modelo Colaborador (dominio).
    # Ahora se asignan los horarios preferidos y asignados ya convertidos a sus respectivos modelos de respuesta.
    return Colaborador(
        id=colaborador_data.id,
        nombre=colaborador_data.nombre,
        legajo=colaborador_data.legajo,
        email=colaborador_data.email,
        telefono=colaborador_data.telefono,
        dni=str(colaborador_data.dni),
        empresa=empresa,
        sucursales=sucursales,
        roles=[Rol(id=r.id, nombre=r.nombre, principal=r.principal) for r in roles],
        horario_preferido=horario_preferido_response,  # Lista de HorarioPreferidoColaboradorResponse
        dias_preferidos=dias_preferidos,
        tipo_empleado=tipo_empleado,
        horario_asignado=horario_asignado_response,     # Lista de HorarioResponse
        hs_extra=hs_extra,
        vacaciones=vacaciones,
        horario_corrido=colaborador_data.horario_corrido
    )

def default_custom_encoder(obj):
    if isinstance(obj, time):
        return obj.isoformat()
    if isinstance(obj, tuple):
        return list(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def convertir_recursivamente(obj):
    """
    Recorre recursivamente la estructura de datos para convertir:
      - time -> isoformat()
      - tuple -> list (u otra estructura serializable)
    """
    if isinstance(obj, dict):
        return {k: convertir_recursivamente(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_recursivamente(item) for item in obj]
    elif isinstance(obj, tuple):
        return [convertir_recursivamente(item) for item in obj]
    elif isinstance(obj, time):
        return obj.isoformat()
    else:
        return obj