from django.apps import AppConfig


class InicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Inicio'
    
    def ready(self):
        import Aplicaciones.Inicio.signals # type: ignore
        
