from django.forms import ValidationError

# Los validadores personalizados se definen aquí
# Un validador es una función o clase que verifica si un valor cumple con ciertos criterios

class MaxSizeFileValidator:
    """
    valida el tamaño máximo de un archivo cargado.
    El tamaño máximo se define en megabytes (MB).
    """
    def __init__(self, max_file_size = 5):
        self.max_file_size = max_file_size  # Size en MB

    def __call__(self, value):
        size = value.size
        max_size = self.max_file_size * 1048576  # Convierte los MB a bytes
        if size > max_size:
            raise ValidationError(f"El tamaño del archivo no puede ser mayor a {self.max_file_size} MB.")
        return value
        