from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from equipment_inventory import views as equipment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('equipment_inventory.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('upload/empleados/', equipment_views.upload_empleados, name='upload_empleados'),
    path('upload/equipos/', equipment_views.upload_equipos, name='upload_equipos'),
    path('', equipment_views.homepage, name='homepage'),  # Redirige a la vista principal del carrusel
]