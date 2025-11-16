from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def group_required(group_name):
    """
    Decorador para restringir el acceso a vistas según el grupo
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Asegura que el usuario esté autenticado
        def _wrapped_view(request, *args, **kwargs):
            # Si es superuser, permitir acceso
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar si el usuario pertenece al grupo requerido
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied  # Lanza un error 403
        return _wrapped_view
    return decorator

def multi_group_required(group_names):
    """
    Decorador para permitir acceso a múltiples grupos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Si es superuser, permitir acceso
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar si el usuario pertenece a alguno de los grupos permitidos
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
            
        return _wrapped_view
    return decorator