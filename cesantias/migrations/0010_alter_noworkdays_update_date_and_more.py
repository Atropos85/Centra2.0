# Generated by Django 5.1.2 on 2024-10-18 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cesantias', '0009_alter_certifications_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noworkdays',
            name='update_date',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='official_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cesantias.official'),
        ),
        migrations.AlterField(
            model_name='request',
            name='request_state',
            field=models.IntegerField(blank=True, choices=[(1, 'RADICADA'), (2, 'LIQUIDADA'), (3, 'CDP SOLICITADO'), (4, 'EMISION RESOLUCION'), (5, 'NOTIFICADO'), (6, 'RPC SOLICITADO'), (7, 'RPC EMITIDO'), (8, 'PASO A FACTURACION'), (9, 'PROCESO DE PAGO'), ('10', 'RECHAZADO')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
