from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

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
                        'error': 'El usuario ya existte',
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
    return redirect('home')

@login_required
def dashboard(req):
    return render(req, 'dashboard.html')

@login_required
def informe_trabajadores(req):
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
        }
    ]

    return render(req, 'datos-filtrados.html', {'trabajadores': trabajadores})

def datos_filtrados(req):

    trabajadores = req.trabajadores

    if req.method == 'POST':
        # Aquí aplicarías tus filtros reales según request.POST
        # Por ahora solo mostramos todos los datos
        pass

    contexto = {
        'trabajadores': trabajadores,
        'title': 'Datos Filtrados'
    }

    return render(req, 'datos-filtrados.html', contexto)