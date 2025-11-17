from django.db import models

# ENTIDADES INDEPENDIENTES
class Area(models.Model):
    nombre_area = models.CharField(max_length=100)
    def __str__(self): return f'{self.nombre_area}'

class Perfil(models.Model):
    nombre_perfil = models.CharField(max_length=100)
    def __str__(self): return f'{self.nombre_perfil}'

class Telefono(models.Model):
    numero_telefono = models.CharField(max_length=20)
    def __str__(self): return f'{self.numero_telefono}'

# ENTIDADES CON DEPENDENCIA SIMPLE
class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=100)
    id_area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre_departamento}'
   
class Cargo(models.Model):
    nombre_cargo = models.CharField(max_length=100)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre_cargo}'
   
class Sexo_trabajador(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMENINO = 'F', 'Femenino'
    OTRO = 'O', 'Otro'

class Trabajador(models.Model):
    rut_trabajador = models.CharField(max_length=12)
    nombre_trabajador = models.CharField(max_length=100)
    apellidos_trabajador = models.CharField(max_length=100)
    direccion_trabajador = models.CharField(max_length=225)
    fecha_ingreso_trabajador = models.DateTimeField(auto_now_add=True)
    sexo_trabajador = models.CharField(
        max_length=1,
        choices=Sexo_trabajador.choices,
        default=Sexo_trabajador.OTRO
    )

    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rut: {self.rut_trabajador}\nNombre: {self.nombre_trabajador}'

class Carga_familiar(models.Model):
    rut_carga_familiar = models.CharField(max_length=12)
    nombre_carga_familiar = models.CharField(max_length=100)
    parentesco_carga_familiar = models.CharField(max_length=100)
    sexo_carga_familiar = models.CharField(
        max_length=1,
        choices=Sexo_trabajador.choices,
        default=Sexo_trabajador.OTRO
    )

    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

class Contacto_emergencia(models.Model):
    nombre_contacto_emergencia = models.CharField(max_length=100)
    parentesco_contacto_emergencia = models.CharField(max_length=50)
    
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

class Tipo_marcado(models.TextChoices):
    ENTRADA = 'E', 'Entrada'
    SALIDA = 'S', 'Salida'
    PAUSA = 'P', 'Pausa'

class Origen_marcado(models.TextChoices):
    BIOMETRICO = 'B', 'Biometrico'
    MANUAL = 'M', 'Manual'
    APP = 'A', 'App'

class Marcado(models.Model):
    fecha_marcado = models.DateTimeField(auto_now_add=True)
    origen_marcado = models.CharField(max_length=100)
    tipo_marcado = models.CharField(
        max_length=1,
        choices=Tipo_marcado.choices,
    )
    origen_marcado = models.CharField(
        max_length=1,
        choices= Origen_marcado.choices
    )
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

# ENTIDADES CON DEPENDENCIA DOBLE
class Trabajador_telefono(models.Model):
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    id_telefono = models.ForeignKey(Telefono, on_delete=models.CASCADE)

class Contacto_emergencia_telefono(models.Model):
    id_contacto_emergencia = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    id_telefono = models.ForeignKey(Telefono, on_delete=models.CASCADE)