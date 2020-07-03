from django.contrib import admin
from django.urls import path
from django.conf import settings
from core.models import User, CoreCompanies
from core import views as core_views

urlpatterns = [

    #  -------------------------HOME-------------------------#
    path('dashboard/', core_views.dashboard.as_view(), name='dashboard'),

    #  -------------------------LOGIN------------------------#
    path('login/', core_views.Login.as_view(
        extra_context={'title': 'Login'}), name='login'),
    path('logout/', core_views.LogoutView.as_view(
        extra_context={'title': 'Logout'}), name='logout'),

    #  -------------------------USER MODEL------------------------#

    path('ListUser/', core_views.ListUser.as_view(
        extra_context={'heading': 'Usuarios', 'title': 'Usuarios'}), name='ListUser'),
    path('CreateUser/', core_views.CreateUser.as_view(
        extra_context={'heading': 'Creando Usuario', 'title': 'Crear Usuario'}), name='CreateUser'),
    path('EditUser/<int:pk>/', core_views.EditUser.as_view(
        extra_context={'heading': 'Editando Usuario', 'title': 'Editar Usuario'}, model=User), name='EditUser'),
    path('DeleteUser/<int:pk>/', core_views.DeleteUser.as_view(
        extra_context={'heading': 'Eliminando Usuario', 'title': 'Eliminar Usuario'}, model=User), name='DeleteUser'),

    #  -------------------------CORE COMPANY MODEL------------------------#

    path('CreateCompany/', core_views.CreateCompany.as_view(
        extra_context={'heading': 'Registrar Compañia', 'title': 'Registrar Compañia'}, model=CoreCompanies), name='CreateCompany'),
    path('ListCompany/', core_views.ListCompany.as_view(
        extra_context={'heading': 'Compañia', 'title': 'Compañia'}, model=CoreCompanies), name='ListCompany'),
     path('DetailCompany/<int:pk>/', core_views.DetailCompany.as_view(
        extra_context={'heading': 'Detalles de Compañia', 'title': 'Detalles de Compañia'}, model=CoreCompanies), name='DetailCompany'),
]