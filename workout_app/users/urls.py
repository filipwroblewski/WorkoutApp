from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# Define URL patterns for the users app
urlpatterns = [
    path('', views.index, name="index"),  # Map the root URL to the index view
    path('login', views.login_view, name="login"),  # Map the /login URL to the login_view
    path('logout', views.logout_view, name="logout"),  # Map the /logout URL to the logout_view
    path('register/', views.register_view, name='register'),  # Map the /register URL to the register_view
]

# Add URL patterns for serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
