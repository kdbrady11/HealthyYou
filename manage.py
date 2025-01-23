#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Import necessary modules
import os  # For interacting with the operating system
import sys  # For accessing command-line arguments


def main():
    """
    Entry point for executing administrative tasks in a Django project.

    - Sets the default Django settings module for the application.
    - Checks if Django is installed and available.
    - Executes command-line commands such as running the server, migrations, etc.
    """
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthyYou.settings')

    try:
        # Import the function to execute commands from the command line
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an error if Django is not installed or not available
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the command-line arguments (e.g., runserver, migrate, etc.)
    execute_from_command_line(sys.argv)


# Ensure this script is executed as the main program
if __name__ == '__main__':
    main()
