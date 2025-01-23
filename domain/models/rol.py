class Rol:
    def __init__(self, nombre, principal=False, **kwargs):
        self.nombre = nombre
        self.principal = principal  # Indica si el rol es principal
        self.atributos_adicionales = kwargs