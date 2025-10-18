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
    path('datos-filtrados/', views.datos_filtrados, name='datos_filtrados'),

]