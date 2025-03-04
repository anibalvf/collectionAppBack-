from django.apps import AppConfig


class SeguridadConfig(AppConfig):
    name = 'seguridad'

    def ready(self):
        import seguridad.decorators