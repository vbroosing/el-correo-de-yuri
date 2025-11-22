from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),

    # AUTENTICACIÓN
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    path('informe-trabajadores/', views.informe_trabajadores, name='informe_trabajadores'),
    path('informe-horas-trabajadas/', views.informe_horas_trabajadas, name='informe_horas_trabajadas'),
    path('datos-filtrados/', views.datos_filtrados, name='datos_filtrados'),

    # FUNCIONES TRABAJADOR
    path('llenar-ficha-carga-familiar/', views.llenar_ficha_carga_familiar, name='llenar_ficha_carga_familiar'),
    path('seleccionar-cargas/', views.seleccionar_cargas_familiares, name='seleccionar_cargas_familiares'),
    path('seleccionar-contactos/', views.seleccionar_contactos_emergencia, name='seleccionar_contactos_emergencia'),
    path('modificar-datos-personales/', views.modificar_datos_personales, name='modificar_datos_personales'),
    path('marcado/', views.marcado, name='marcado'),

    # FUNCIONES PERSONAL RRHH
    path('llenar-ficha-trabajador/', views.llenar_ficha_trabajador, name='llenar_ficha_trabajador'),


]