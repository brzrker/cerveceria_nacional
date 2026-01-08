from django.apps import AppConfig

# Configuración de la aplicación
# Aquí se define la configuración de la aplicación, como su nombre y opciones específicas

# La clase AppConfig es la configuración predeterminada para la aplicación
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Clases y Modelos'
