from django.contrib.auth import views as auth_views  # Import Django's built-in authentication views
from django.contrib import admin  # Import Django admin module
from django.contrib.auth.views import LogoutView  # Import logout view for handling user logouts
from django.urls import path, include  # Import path and include for URL routing
from tracker import views  # Import views from the tracker app (e.g., homepage view)

# Define URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site route
    path('', views.homepage, name='homepage'),  # Route for the homepage
    path('dashboard/', include('tracker.urls')),  # Includes URLs for the dashboard (handled in tracker.urls)
    path('accounts/', include('django.contrib.auth.urls')),
    # Includes built-in auth routes (login, logout, password reset, etc.)
    path('logout/', views.logout_view, name='logout'),  # Custom logout view
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),  # Protected login route requiring authenticated access
    path('logout/', LogoutView.as_view(), name='logout'),  # Use Django's built-in logout view
]

