from django.db import models
import uuid
from django.core.validators import RegexValidator

# Modelo Entities
class Entities(models.Model):
    # Código de la entidad (UUID)
    entity_ID = models.IntegerField(primary_key=True, editable=False)
    # Sigla de la entidad
    nick_name = models.CharField(max_length=255)
    # Nombre de la entidad
    entity_name = models.CharField(max_length=255)
    # Fondo al cual pertenece la entidad
    fund = models.CharField(max_length=255)
    # Código PosPre
    posPre = models.CharField(max_length=255)
    # Cuenta mayor
    ledger_account = models.BigIntegerField()
    # Rubro
    heading = models.CharField(max_length=255)

    def __str__(self):
        return self.entity_name
