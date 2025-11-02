from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# MODELOS
from app.models import Trabajador

# HOME
def home(req):
    return render(req, 'home.html')

# AUTENTICACIÓN
def signup(req):
    form = UserCreationForm(req.POST)  # Instanciando el form
    
    if req.method == 'POST':
        try:
            if req.POST['password1'] == req.POST['password2']:
                try:
                    # registrar Usuario
                    user = User.objects.create_user(username=req.POST['username'], password=req.POST['password1'])
                    user.save()

                    # iniciando sesion
                    login(req, user)

                    return redirect('dashboard') 
                except IntegrityError:
                    return render(req, 'signup.html', {
                        'form': form,
                        'error': 'El usuario ya existe',
                    })
            else:
                return render(req, 'signup.html', {
                        'form': form,
                        'error': 'Las contraseñas no coinciden.',
                    })
        except:
            return redirect('signup')
    
    elif req.method == 'GET':
        return render(req, 'signup.html', {'form': form})  # Pasamos el formulario al template

def signin(req):
    form = AuthenticationForm()

    if req.method == 'GET':
        return render(req, 'signin.html', {'form': form})
    else:
        try:
            user = authenticate(req, username=req.POST['username'], password=req.POST['password'])
            if user is None:
                return render(req, 'signin.html', {'form': form, 'error': 'Usuario no registrado'})
            else:

                login(req, user)
                return redirect('dashboard')
        except:
            return redirect('signin')

@login_required
def signout(req):
    logout(req)
    return redirect('home.html')

# TRANSVERSALES
@login_required
def dashboard(req):
    return render(req, 'dashboard.html')

# PERFIL JEFE RRHH
@login_required
def informe_trabajadores(req):
    return render(req, 'informe-trabajadores.html')

@login_required
def datos_filtrados(req):

     # AQUI FALTA LA CONEXION CON LA DB
    trabajadores = [
        {
            'nombre': 'Juan Pérez',
            'rut': '12.345.678-9',
            'sexo': 'M',
            'cargo': 'Ingeniero de Software',
            'departamento': 'Tecnología'
        },
        {
            'nombre': 'María López',
            'rut': '98.765.432-1',
            'sexo': 'F',
            'cargo': 'Analista de Datos',
            'departamento': 'Análisis'
        },
        {
            'nombre': 'Carlos Ruiz',
            'rut': '23.456.789-0',
            'sexo': 'M',
            'cargo': 'Diseñador UI/UX',
            'departamento': 'Diseño'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        },
        {
            'nombre': 'Ana Torres',
            'rut': '34.567.890-1',
            'sexo': 'F',
            'cargo': 'Gerente de Proyectos',
            'departamento': 'Gestión'
        }
    ]

    
    filtros = {
        'sexo': req.GET.get('sexo', 'M').strip(),
        'cargo': req.GET.get('cargo', '').strip(),
        'departamento': req.GET.get('departamento', '').strip(),
        'area': req.GET.get('area', '').strip(),
    }

    # Aplicar filtros no vacíos
    for campo, valor in filtros.items():
        if valor:
            trabajadores = trabajadores.filter(**{campo: valor})

    return render(req, 'datos-filtrados.html', {
        'trabajadores': trabajadores,
        'filtros': filtros,
    })

@login_required
def informe_horas_trabajadas(req):
    return render(req, 'informe-horas-trabajadas.html')

# PERFIL PERSONAL RRHH

# PERFIL TRABAJADOR

def seleccionar_cargas_familiares(req):
    cargas_familiares = [
    {'nombre': 'María López', 'relacion': 'Esposa'},
    {'nombre': 'Carlos Ruiz', 'relacion': 'Hijo'},
    {'nombre': 'Ana Torres', 'relacion': 'Madre'},
    {'nombre': 'Luis Pérez', 'relacion': 'Hermano'},
    {'nombre': 'Alberta Jara', 'relacion': 'Hija'}
    ]
    return render(req, 'seleccionar-cargas.html', {'cargas_familiares': cargas_familiares})

def seleccionar_contactos_emergencia(req):
    contactos_emergencia = [
    {'nombre': 'María López', 'relacion': 'Esposa'},
    {'nombre': 'Carlos Ruiz', 'relacion': 'Hijo'},
    {'nombre': 'Ana Torres', 'relacion': 'Madre'},
    {'nombre': 'Luis Pérez', 'relacion': 'Hermano'},
    {'nombre': 'Alberta Jara', 'relacion': 'Hija'}
    ]
    return render(req, 'seleccionar-contactos.html', {'contactos_emergencia': contactos_emergencia})

def modificar_datos_personales(req):
    return render(req, 'modificar-datos-personales.html')