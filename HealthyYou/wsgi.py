"""
WSGI config for HealthyYou project.

This file contains the configuration to serve the project using WSGI (Web Server Gateway Interface).
WSGI is the standard interface between web servers and Python web applications or frameworks.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os  # Importing OS module to interact with the operating system
from django.core.wsgi import get_wsgi_application  # Importing method to get the WSGI application

# Setting the default settings module for the 'HealthyYou' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthyYou.settings')

# Creating the WSGI application instance that the WSGI server will use to forward requests to the application
application = get_wsgi_application()
