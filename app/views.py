from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .decorators import group_required, multi_group_required
from django.contrib import messages

# MODELOS
from app.models import Trabajador, Cargo, Carga_familiar

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
@multi_group_required(['Personal RRHH']) # Asumo que solo Personal RRHH puede crear
def llenar_ficha_trabajador(req):
    cargos = Cargo.objects.all()
    
    if req.method == 'POST':
        # 1. Recolección de datos y validación básica de presencia
        
        # Lista de campos POST requeridos (basados en tu modelo Trabajador)
        campos_requeridos = [
            'rut_trabajador', 'nombre_trabajador', 'apellidos_trabajador',
            'direccion_trabajador', 'sexo_trabajador', 'id_cargo'
        ]
        
        campos_trabajador = {}
        error = False
        
        for campo in campos_requeridos:
            valor = req.POST.get(campo, '').strip()
            if not valor:
                error = f'El campo "{campo}" es obligatorio.'
                break
            campos_trabajador[campo] = valor

        if error:
            # Si falta un campo, renderiza con el error
            return render(req, 'llenar-ficha-trabajador.html', {
                'error': error,
                'cargos': cargos,
                'valores_anteriores': req.POST # Para no perder lo que ya escribió el usuario
            })
        
        # 2. Validación de Llave Foránea (Cargo)
        try:
            id_cargo_str = campos_trabajador.pop('id_cargo') # Quitar el ID para obtener la instancia
            cargo_instance = Cargo.objects.get(id=int(id_cargo_str))
        except (Cargo.DoesNotExist, ValueError):
            return render(req, 'llenar-ficha-trabajador.html', {
                'error': 'El cargo seleccionado no es válido.',
                'cargos': cargos,
                'valores_anteriores': req.POST
            })
        
        # 3. Crear el Trabajador
        try:
            # La fecha_ingreso_trabajador tiene auto_now_add=True, no la necesitamos en el POST
            Trabajador.objects.create(
                id_cargo=cargo_instance, # Asignamos la instancia
                **campos_trabajador
            )
            # Redirigir al listado o a una página de éxito
            return redirect('trabajador_listado') # Necesitas una URL llamada 'trabajador_listado'
            
        except Exception as e:
             # Manejar posibles errores de base de datos o formato (ej. si el RUT ya existe)
            return render(req, 'llenar-ficha-trabajador.html', {
                'error': f'Error al guardar el trabajador: {e}',
                'cargos': cargos,
                'valores_anteriores': req.POST
            })

    else:
        # Solicitud GET
        return render(req, 'llenar-ficha-trabajador.html', {'cargos': cargos})

    
# PERFIL TRABAJADOR
@login_required
def llenar_ficha_carga_familiar(req):
    if req.method == 'POST':
        # Obtener datos del formulario
        nombre = req.POST.get('nombre_carga_familiar', '').strip()
        parentesco = req.POST.get('parentesco_carga_familiar', '').strip()
        rut = req.POST.get('rut_carga_familiar', '').strip()
        sexo = req.POST.get('sexo_carga_familiar', '').strip()

        # # Validación mínima (puedes mejorarla si necesitas)
        # if not (nombre and parentesco and rut and sexo):
        #     messages.error(req, "Por favor, complete todos los campos obligatorios.")
        #     return render(req, 'llenar-ficha-carga-familiar.html')

        try:
            # Encontrar al trabajador por nombre y apellido del usuario
            user = req.user
            trabajador = Trabajador.objects.get(nombre_trabajador=user.first_name, apellidos_trabajador=user.last_name)

            cargas_query = Carga_familiar.objects.filter(id_trabajador=trabajador)
            cargas_familiares = [
                {'nombre': carga.nombre_carga_familiar, 'relacion': carga.parentesco_carga_familiar}
                for carga in cargas_query
            ]

            # Crear y guardar la carga familiar
            Carga_familiar.objects.create(
                id_trabajador=trabajador,
                nombre_carga_familiar=nombre,
                parentesco_carga_familiar=parentesco,
                rut_carga_familiar=rut,
                sexo_carga_familiar=sexo
            )

            messages.success(req, "Carga familiar registrada exitosamente.")
            return render(req, 'seleccionar-cargas.html', {'cargas_familiares': cargas_familiares})
            

        except Trabajador.DoesNotExist:
            messages.error(req, "No se encontró un trabajador asociado a tu usuario. Verifica tu nombre y apellido en el perfil.")
            return render(req, 'seleccionar-cargas.html', {'cargas_familiares': cargas_familiares})

    # Si es GET, solo renderiza el formulario
    return render(req, 'llenar-ficha-carga-familiar.html')

@login_required
def seleccionar_cargas_familiares(req):

    if req.method == 'GET':
        # Obtener el nombre y apellido del usuario autenticado
        user = req.user
        nombre = user.first_name
        apellido = user.last_name

        try:
            # Buscar el trabajador por nombre y apellido
            trabajador = Trabajador.objects.get(nombre_trabajador=nombre, apellidos_trabajador=apellido)
            # Obtener sus cargas familiares
            cargas_query = Carga_familiar.objects.filter(id_trabajador=trabajador)
            # Formatear como lista de diccionarios
            cargas_familiares = [
                {'nombre': carga.nombre_carga_familiar, 'relacion': carga.parentesco_carga_familiar}
                for carga in cargas_query
            ]
        except Trabajador.DoesNotExist:
            # Si no existe el trabajador, devolver lista vacía o mensaje
            cargas_familiares = []
    else:
        # Si no es POST, también podrías aplicar la misma lógica o dejar vacío
        user = req.user
        nombre = user.first_name
        apellido = user.last_name
        try:
            trabajador = Trabajador.objects.get(nombre_trabajador=nombre, apellidos_trabajador=apellido)
            cargas_query = Carga_familiar.objects.filter(id_trabajador=trabajador)
            cargas_familiares = [
                {'nombre': carga.nombre_carga_familiar, 'relacion': carga.parentesco_carga_familiar}
                for carga in cargas_query
            ]
        except Trabajador.DoesNotExist:
            cargas_familiares = []

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