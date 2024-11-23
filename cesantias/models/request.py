from django.db import models
from .official import Official
from .entities import Entities 
from django.core.validators import RegexValidator

# Modelo Request
class Request(models.Model):
    # Identificador de la solicitud
    request_ID = models.AutoField(primary_key=True)  
	# Identificador del funcionario
    official_ID = models.ForeignKey(Official, on_delete=models.CASCADE, null=True, blank=True)  
    # Fecha de radicación
    request_date = models.DateField()  
    # Fecha de corte
    cutoff_date = models.DateField()  
	# Estado de la solicitud
    STATE_CHOICES = [(1, 'RADICADA'), (2, 'LIQUIDADA'), (3, 'CDP SOLICITADO'), (4, 'EMISION RESOLUCION'), (5, 'NOTIFICADO'), (6, 'RPC SOLICITADO'), (7, 'RPC EMITIDO'), (8, 'PASO A FACTURACION'), (9, 'PROCESO DE PAGO'), ('10', 'RECHAZADO')]
    request_state = models.IntegerField(choices=STATE_CHOICES, default=1, null=True, blank=True)  
	# Número del Radicado
    filling_number = models.BigIntegerField()  
	# Valor del Radicado
    filling_value = models.DecimalField(max_digits=15, decimal_places=2)  
	# Tipo de Cesantía
    SEVERANCE_CHOICES = [('D', 'DEFINITIVA'), ('P', 'PARCIAL')]#, ('R', 'RELIQUIDACION')('M', 'MONTO'), 
    severance_type = models.CharField(max_length=1, choices=SEVERANCE_CHOICES)  
	# Modo de retiro
    MODE_CHOICES = [('D', 'DEFINITIVA'), ('E', 'EDUCACION'), ('H', 'HIPOTECARIO'), ('R', 'REPARACIONES LOCATIVAS'), ('V', 'COMPRA VIVIENDA')]#, ('O', 'OTROS'),
    withdrawal_mode = models.CharField(max_length=1, choices=MODE_CHOICES)  
	# Días totales
    total_days = models.IntegerField(null=True, blank=True)  
	# Días no trabajados
    no_work_days = models.IntegerField(null=True, blank=True, default=0)  
	# Días trabajados
    working_days = models.IntegerField(null=True, blank=True)  
	# Salario promedio
    average_salary = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  
	# Valor Cesantías Totales
    total_severance_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  
	# Valor cesantías anterior
    previous_severance_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  
	# Saldo de cesantías
    balance_severance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  
	# Valor desembolsado
    severance_disbursed_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  
	# Fecha liquidación
    settlement_date = models.DateField(null=True, blank=True)  
	# Fecha solicitud CDP
    cdp_request_date = models.DateField(null=True, blank=True)  
	# Fecha emisión CDP
    cdp_issue_date = models.DateField(null=True, blank=True)  
	# Número CDP
    cdp_number = models.BigIntegerField(null=True, blank=True)  
	# Cargo Titular
    holder_position = models.CharField(max_length=255, null=True, blank=True)  
	# Cargo titular por encargo
    incharge_position = models.CharField(max_length=255, null=True, blank=True)  
	# Fecha Notificación
    notify_date = models.DateField(null=True, blank=True)  
	# Fecha resolución
    resolution_date = models.DateField(null=True, blank=True)  
	# Número resolución
    resolution_number = models.CharField(max_length=255, null=True, blank=True)  
	# Fecha solicitud RPC
    rpc_request_date = models.DateField(null=True, blank=True)  
	# Número RPC
    rpc_number = models.BigIntegerField(null=True, blank=True)  
	# Fecha paso a facturación
    billing_date = models.DateField(null=True, blank=True)  
	# Fecha paso a tesorería
    treasury_date = models.DateField(null=True, blank=True)  
	# Número de la factura
    billing_number = models.BigIntegerField(null=True, blank=True)  
	# Motivo de rechazo
    rejection_reason = models.TextField(null=True, blank=True)  
	# Fecha de creación
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
	# Usuario que crea
    creation_user = models.CharField(max_length=255, null=True, blank=True)  
	# Fecha modificación
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)  
	# Usuario que modifica
    update_user = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return f'Request {self.request_ID}'


class RequestDetail(models.Model):
    # Identificador de la solicitud
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='details',null=True, blank=True) 
	# Tipo de solicitud
    sell_seller = models.CharField(max_length=255,null=True, blank=True)  
	# Tipo de documento del vendedor
    sell_doc_type = models.CharField(max_length=255,null=True, blank=True)  
	# Número de documento del vendedor
    sell_doc_num = models.CharField(max_length=255,null=True, blank=True)  
	# Número de resolución
    def_resolution = models.CharField(max_length=255,null=True, blank=True)  
	# Fecha de la resolución
    def_date = models.DateField(null=True, blank=True)  
	# Cargo
    def_position = models.CharField(max_length=255,null=True, blank=True)  
	# NIT de la institución educativa
    est_nit = models.CharField(max_length=255,null=True, blank=True)  
	# Nombre de la institución educativa
    est_institution = models.CharField(max_length=255,null=True, blank=True)  
	# Número del crédito hipotecario
    hip_loan_number = models.CharField(max_length=255,null=True, blank=True)  
	# NIT del banco
    hip_nit = models.CharField(max_length=255,null=True, blank=True)  
	# Nombre del banco
    hip_bank = models.CharField(max_length=255,null=True, blank=True)  

    def __str__(self):
        return f'RequestDetail for {self.request}'


class Certifications(models.Model):
    # Identificador de la solicitud
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='certifications',null=True, blank=True) 
	# Número de la certificación
    cert = models.IntegerField()  
	# Fecha de la certificación
    cert_date = models.DateField(null=True, blank=True)  
	# Número de la certificación
    cert_number = models.CharField(max_length=255, null=True, blank=True)  
	# Nombre de quien certifica
    cert_name = models.CharField(max_length=255,null=True, blank=True)  
	# Cargo de quien certifica
    cert_position = models.CharField(max_length=255,null=True, blank=True)  
	# Entidad que certifica
    cert_entity_name = models.CharField(max_length=255,null=True, blank=True)  

    def __str__(self):
        return f'Certification {self.cert_number} for {self.request}'

    def save(self, *args, **kwargs):
        if not self.cert:  # Si no tiene un número de certificación asignado
            last_cert = Certifications.objects.filter(request=self.request).count()
            self.cert = last_cert + 1  # Incrementa el número dentro de la solicitud

        super().save(*args, **kwargs)
        
class WageFactors(models.Model):
    # Identificador de la solicitud
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='wage_factors')  
	# Sueldo
    wage = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 
	# Sobresueldo
    overwage = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima anual de servicio
    annual_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima de Vacaciones
    holiday_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima de Navidad
    christmas_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Bonificación
    bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Subsidio de transporte
    transport_subsidy = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Auxilio de Alimentación
    food_subsidy = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima Técnica
    technical_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima de Antigüedad
    seniority_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Prima de Alojamiento
    accommodation_bonus = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Horas Extras
    overtime = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Dev. Por Sorteo
    dev_by_draw = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  
	# Viáticos
    travel_expenses = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)  

    def __str__(self):
        return f'WageFactors for {self.request}'