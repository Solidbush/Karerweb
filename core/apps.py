from django.apps import AppConfig


class KarerWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Объект'

    def ready(self) -> None:
        import jet.utils

        from .utils import get_app_list
        jet.utils.get_app_list = get_app_list
