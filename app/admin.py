from django.contrib import admin
from app.models import Area, Perfil, Trabajador, Telefono, Departamento, Cargo, Carga_familiar, Contacto_emergencia

# Register your models here.
admin.site.register(Area)
admin.site.register(Perfil)
admin.site.register(Trabajador)
admin.site.register(Telefono)
admin.site.register(Departamento)
admin.site.register(Cargo)    
admin.site.register(Carga_familiar)
admin.site.register(Contacto_emergencia)