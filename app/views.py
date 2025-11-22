from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .decorators import group_required, multi_group_required

# MODELOS
from app.models import Trabajador, Cargo

# HOME
@login_required
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
    return render(req, 'home.html')
    # return redirect('home.html')

# TRANSVERSALES
@login_required
def dashboard(req):
    # Verificar si el usuario es superuser
    if req.user.is_superuser:
        es_jefe_rrhh = True
        es_personal_rrhh = True
        es_trabajador = True
    else:
        # Verificar si el usuario pertenece a ciertos grupos
        es_jefe_rrhh = req.user.groups.filter(name='Jefe RRHH').exists()
        es_personal_rrhh = req.user.groups.filter(name='Personal RRHH').exists()
        es_trabajador = req.user.groups.filter(name='Trabajador').exists()
    context = {
        'es_jefe_rrhh': es_jefe_rrhh,
        'es_personal_rrhh': es_personal_rrhh,
        'es_trabajador': es_trabajador,
    }
    return render(req, 'dashboard.html', context)
    # return render(req, 'dashboard.html', {'notificaciones_pendientes': True})

# PERFIL JEFE RRHH
@login_required
@multi_group_required(['Jefe RRHH', 'Personal RRHH'])
def informe_trabajadores(req):
    return render(req, 'informe-trabajadores.html')


@login_required
@multi_group_required(['Jefe RRHH', 'Personal RRHH'])
def datos_filtrados(req):
    
    # CONEXIÓN SIN FILTROS DE BUSQUEDA
    trabajadores = Trabajador.objects.filter()
    cargos = Cargo.objects.filter()

    filtros = {
        'sexo_trabajador': req.GET.get('sexo', '').strip(),
        'id_cargo': req.GET.get('cargo', '').strip(),
        'departamento': req.GET.get('departamento', '').strip(),
        'area': req.GET.get('area', '').strip(),
    }

    # Aplicar filtros no vacíos
    for campo, valor in filtros.items():
        if valor != '':
            trabajadores = trabajadores.filter(**{campo: valor})

    print(trabajadores)
    return render(req, 'datos-filtrados.html', {
        'trabajadores': trabajadores,
        'filtros': filtros,
    })

@login_required
def informe_horas_trabajadas(req):
    return render(req, 'informe-horas-trabajadas.html')

# PERFIL PERSONAL RRHH
@login_required
def llenar_ficha_trabajador(req):
    if req.method == 'POST':
        # Obtener el ID del cargo seleccionado
        id_cargo_str = req.POST.get('id_cargo', '').strip()

        if not id_cargo_str:
            # Obtener los cargos para volver a mostrarlos en el template
            cargos = Cargo.objects.all()
            return render(req, 'llenar-ficha-trabajador.html', {
                'error': 'Debes seleccionar un cargo.',
                'cargos': cargos
            })

        try:
            cargo = Cargo.objects.get(id=int(id_cargo_str))
        except (Cargo.DoesNotExist, ValueError):
            cargos = Cargo.objects.all()
            return render(req, 'llenar-ficha-trabajador.html', {
                'error': 'El cargo seleccionado no es válido.',
                'cargos': cargos
            })

        # Crear el diccionario con los datos del trabajador
        campos_trabajador = {
            'rut_trabajador': req.POST.get('rut_trabajador', '').strip(),
            'nombre_trabajador': req.POST.get('nombre_trabajador', '').strip(),
            'apellidos_trabajador': req.POST.get('apellidos_trabajador', '').strip(),
            'direccion_trabajador': req.POST.get('direccion_trabajador', '').strip(),
            'fecha_ingreso_trabajador': req.POST.get('fecha_ingreso_trabajador', '').strip(),
            'sexo_trabajador': req.POST.get('sexo_trabajador', '').strip(),
            'id_cargo': cargo  # Instancia válida de Cargo
        }

        # Crear el trabajador en la base de datos
        trabajador = Trabajador.objects.create(**campos_trabajador)
         # Para solicitudes GET, obtener los cargos y renderizar el formulario
        cargos = Cargo.objects.all()
        return render(req, 'llenar-ficha-trabajador.html', {'cargos': cargos})

       
    else:
        # Para solicitudes GET, obtener los cargos y renderizar el formulario
        cargos = Cargo.objects.all()
        return render(req, 'llenar-ficha-trabajador.html', {'cargos': cargos})


    
# PERFIL TRABAJADOR
@login_required
def seleccionar_cargas_familiares(req):
    cargas_familiares = [
    {'nombre': 'María López', 'relacion': 'Esposa'},
    {'nombre': 'Carlos Ruiz', 'relacion': 'Hijo'},
    {'nombre': 'Ana Torres', 'relacion': 'Madre'},
    {'nombre': 'Luis Pérez', 'relacion': 'Hermano'},
    {'nombre': 'Alberta Jara', 'relacion': 'Hija'}
    ]
    return render(req, 'seleccionar-cargas.html', {'cargas_familiares': cargas_familiares})

@login_required
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

def marcado(req):
    return render(req, 'marcado.html')