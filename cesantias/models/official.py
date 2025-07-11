from django.db import models
from .entities import Entities 
import uuid
from django.core.validators import RegexValidator


################################################################

class Departament(models.Model):
    # Nombre del departamento
    departament = models.CharField(max_length=100, unique=True)  # Asegúrate de que sea único
    # Descripción del departamento
    depto_name = models.CharField(max_length=255)

    def __str__(self):
        return self.depto_name  # Muestra solo el nombre del departamento

class City(models.Model):
    # Relación de clave foránea usando el campo 'departament'
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, to_field='departament', related_name='cities')
    # Nombre del municipio
    city = models.CharField(max_length=100, unique=True)
    # Descripción del municipio
    city_name = models.CharField(max_length=255)

    def __str__(self):
        return self.city_name  # Muestra solo el nombre del municipio


# Modelo Official
class Official(models.Model):
    # Número de identificación del funcionario (solo números)
    official_ID = models.IntegerField(primary_key=True, editable=False, blank=True)
    # Número de identificación del funcionario (solo números)
    number_ID = models.BigIntegerField( validators=[
        RegexValidator(regex=r'^\d+$', message='El ID oficial solo puede contener números.')
    ])
     # Nombre del funcionario (solo letras)
    names = models.CharField(max_length=100, validators=[
        RegexValidator(regex=r'^[a-zA-Z\s]+$', message='El nombre solo puede contener letras.')
    ])
    # Apellidos del funcionario (solo letras)
    last_names = models.CharField(max_length=100, validators=[
        RegexValidator(regex=r'^[a-zA-Z\s]+$', message='Los apellidos solo pueden contener letras.')
    ])
    # Género del funcionario ('M' para Masculino, 'F' para Femenino)
    GENDER_CHOICES = [('M', 'MASCULINO'), ('F', 'FEMENINO')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # Relación con Entities (Entidad a la que pertenece el funcionario)
    entity_ID = models.ForeignKey(Entities, on_delete=models.CASCADE)
    # Ciudad a la que pertenece el funcionario (solo números)
    city = models.ForeignKey(City, on_delete=models.CASCADE, to_field='city', related_name='citdep')
    # Departamento al cual pertenece el funcionario (solo números)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, to_field='departament', related_name='depto')
    # Dirección del funcionario
    address = models.CharField(max_length=255, null=True, blank=True)
    # Teléfono fijo del funcionario (solo números)
    phone = models.BigIntegerField(null=True, blank=True)
    # Extension
    extensions = models.IntegerField(null=True, blank=True)
    # Celular del funcionario (solo números)
    celphone = models.BigIntegerField(null=True, blank=True)
    # Fecha de ingreso del funcionario
    start_date = models.DateField()

    def __str__(self):
        return f' {self.number_ID} {self.names} {self.last_names}'

# Modelo NoWorkDays
class NoWorkDays(models.Model):
    # Relación con Official (Identificador del funcionario)
    official_ID = models.ForeignKey(Official, on_delete=models.CASCADE)
    # Número de días no trabajados
    no_work_days = models.IntegerField()
    # Fecha de actualización
    update_date = models.DateField(auto_now=True, null=True, blank=True)
    # Identificador de la solicitud ()
    request_ID = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Funcionario: {self.official_ID}, Días no trabajados: {self.no_work_days}'
    
    
