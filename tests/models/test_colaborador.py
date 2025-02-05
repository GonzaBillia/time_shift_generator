import pytest
from datetime import date, time
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO

@pytest.fixture
def horarios_asignados():
    """
    Genera un array de horarios con:
    - 3 días trabajando 7 horas (Lunes a Miércoles).
    - 3 días trabajando 8 horas (Jueves a Sábado).
    """
    horarios = [
        Horario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        Horario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        Horario(
            fecha=date(2025, 1, 8),  # Miércoles
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        Horario(
            fecha=date(2025, 1, 9),  # Jueves
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
        Horario(
            fecha=date(2025, 1, 10),  # Viernes
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
        Horario(
            fecha=date(2025, 1, 11),  # Sábado
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
    ]
    return horarios

@pytest.fixture
def colaborador_tiempo_completo(horarios_asignados):
    return Colaborador(
        nombre="Juan Pérez",
        legajo=1234,
        email="juan.perez@example.com",
        telefono="+123456789",
        dni="12.345.678",
        roles=["Desarrollador"],
        horario_preferido=None,
        dias_preferidos=[0, 1, 2, 3, 4],
        horas_semanales=45,
        hs_extra={"devolver": 0, "cobrar": 0},
        vacaciones=[],
        horario_asignado=horarios_asignados,
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8
    )

# Pruebas sobre calcular_horas_totales_semanales
def test_calcular_horas_totales_semanales_con_horarios(colaborador_tiempo_completo):
    """
    Valida que el cálculo de horas semanales sea correcto con los horarios asignados:
    - 3 días trabajando 7 horas.
    - 3 días trabajando 8 horas.
    Total: 45 horas.
    """
    assert colaborador_tiempo_completo.calcular_horas_totales_semanales() == 45.0

# Pruebas sobre verificar_horas_semanales
def test_verificar_horas_semanales_dentro_del_limite(colaborador_tiempo_completo):
    """
    Verifica que el colaborador no exceda el límite de 45 horas semanales.
    """
    assert colaborador_tiempo_completo.verificar_horas_semanales()

# Pruebas sobre verificar_horas_diarias
def test_verificar_horas_diarias_dentro_del_limite(colaborador_tiempo_completo):
    """
    Verifica que en ningún día el colaborador exceda el límite de 8 horas diarias.
    """
    assert colaborador_tiempo_completo.verificar_horas_diarias()

def test_verificar_horas_diarias_excede_limite(colaborador_tiempo_completo):
    """
    Verifica el caso en el que se asigna un horario que excede las horas diarias máximas.
    """
    horario_excedido = Horario(
        fecha=date(2025, 1, 12),  # Domingo
        bloques=[(time(9, 0), time(19, 0))]  # 10 horas
    )
    colaborador_tiempo_completo.horario_asignado.append(horario_excedido)
    assert not colaborador_tiempo_completo.verificar_horas_diarias()

# Pruebas sobre agregar_horario
def test_agregar_horario_excede_horas_semanales(colaborador_tiempo_completo):
    """
    Verifica que no se pueda agregar un horario si excede las horas semanales asignadas.
    """
    horario_largo = Horario(
        fecha=date(2025, 1, 12),  # Domingo
        bloques=[(time(9, 0), time(18, 0))]  # 9 horas
    )

    try:
        colaborador_tiempo_completo.agregar_horario(horario_largo)
        # Si no lanza la excepción, falla el test
        assert False, "Se esperaba un ValueError, pero el horario se agregó exitosamente."
    except ValueError as e:
        # Validar que el mensaje de la excepción sea el correcto
        assert str(e) == "Agregar este horario excede las horas semanales asignadas.", \
            "El mensaje de ValueError no coincide con el esperado."

