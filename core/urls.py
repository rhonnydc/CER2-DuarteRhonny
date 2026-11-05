from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/categoria/<int:categoria_id>/', views.catalogo, name='catalogo_categoria'),
    path('lugar/<int:lugar_id>/', views.detalle, name='detalle'),
    path('gestion/', views.gestion, name='gestion'),
    path('gestion/agregar/', views.agregar_lugar, name='agregar_lugar'),
    path('gestion/editar/<int:lugar_id>/', views.editar_lugar, name='editar_lugar'),
    path('ingresar/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
]
