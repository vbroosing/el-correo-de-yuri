# from django import forms
# from .models import Trabajador

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Trabajador
#         fields = ['rut_trabajador', 'nombre_trabajador', 'apellidos_trabajador', 
#                   'direccion_trabajador', 'fecha_ingreso_trabajador', 'sexo_trabajador', 'id_cargo']
#         widgets = {
#             'rut_trabajador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
#             'nombre_trabajador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
#             'apellidos_trabajador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
#             'direccion_trabajador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
#             'fecha_ingreso_trabajador': forms.DateField(attrs={'class': 'form-control'}),
#             'sexo_trabajador': forms.ChoiceField(attrs={'class': 'form-control', 'placeholder': 'Otro'}),
#             'id_cargo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
            
#         }