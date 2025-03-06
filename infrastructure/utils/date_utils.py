# utils/date_utils.py
from datetime import date, timedelta

def get_next_date_for_dia(dia_id: int) -> date:
    """
    Retorna la próxima fecha cuyo weekday coincide con `dia_id`
    (donde lunes=0, domingo=6). Si hoy ya es ese día, retorna la próxima semana.
    """
    hoy = date.today()
    dias_a_agregar = (dia_id - hoy.weekday() + 7) % 7
    if dias_a_agregar == 0:
        dias_a_agregar = 7  # Forzamos que sea el próximo, no el mismo día.
    return hoy + timedelta(days=dias_a_agregar)
