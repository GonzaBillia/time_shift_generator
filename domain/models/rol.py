class Rol:
    def __init__(self, id, nombre, principal=False, **kwargs):
        self.id = id  # Ahora tiene una referencia a la base de datos
        self.nombre = nombre
        self.principal = principal  # Indica si el rol es principal
        self.atributos_adicionales = kwargs  # Permite atributos personalizados
