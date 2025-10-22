from django.apps import AppConfig

class TrackerConfig(AppConfig):
    # Specifies the default auto field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of your application
    name = 'tracker'
