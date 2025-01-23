"""
ASGI config for HealthyYou project.

This file configures the ASGI (Asynchronous Server Gateway Interface) for the project,
exposing the ASGI application as a module-level variable named `application`.

ASGI is a specification for Python asynchronous web servers, allowing Django to handle
both traditional HTTP requests and asynchronous protocols like WebSockets.

For more details, refer to:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# Importing necessary modules
import os  # Provides a way to interact with the operating system
from django.core.asgi import get_asgi_application  # Handles the ASGI application

# Setting the default settings module for the ASGI application to HealthyYou's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthyYou.settings')

# Creating an ASGI application callable that will be used by ASGI servers
application = get_asgi_application()

