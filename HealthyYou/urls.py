from django.contrib.auth import views as auth_views

from django.urls import include, path
import django.contrib.admin as admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('tracker.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login after logout
]
