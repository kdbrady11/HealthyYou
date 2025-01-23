from django.apps import AppConfig  # Import AppConfig to configure the application


# Configuration class for the 'tracker' application
class TrackerConfig(AppConfig):
    # Specifies the default field type for automatically added primary key fields
    default_auto_field = 'django.db.models.BigAutoField'

    # The name attribute defines the application name (used in the project settings)
    name = 'tracker'
