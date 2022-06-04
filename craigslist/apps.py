from django.apps import AppConfig


class CraigslistConfig(AppConfig):
    """
    Configure default auto field and app name
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'craigslist'
