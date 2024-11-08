# Generated by Django 5.1.1 on 2024-10-06 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cesantias', '0006_rename_extensions_official_extensions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestdetail',
            name='request_type',
        ),
        migrations.AlterField(
            model_name='certifications',
            name='cert_entity_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certifications',
            name='cert_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certifications',
            name='cert_number',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='certifications',
            name='cert_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='noworkdays',
            name='request_ID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='noworkdays',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='official',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='official',
            name='celphone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='official',
            name='extensions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='official',
            name='gender',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')], max_length=1),
        ),
        migrations.AlterField(
            model_name='official',
            name='official_ID',
            field=models.IntegerField(blank=True, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='official',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='average_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='balance_severance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='billing_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='billing_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='cdp_issue_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='cdp_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='cdp_request_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='creation_user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='filling_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='holder_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='incharge_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='no_work_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='notify_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='previous_severance_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='resolution_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='resolution_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='rpc_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='rpc_request_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='settlement_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='severance_disbursed_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='total_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='total_severance_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='treasury_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='update_user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='working_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='def_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='def_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='def_resolution',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='est_institution',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='est_nit',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='hip_bank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='hip_loan_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='hip_nit',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='cesantias.request'),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='sell_doc_num',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='sell_doc_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='requestdetail',
            name='sell_seller',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='accommodation_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='annual_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='christmas_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='dev_by_draw',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='food_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='holiday_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='overtime',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='overwage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='seniority_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='technical_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='transport_subsidy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='travel_expenses',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='wagefactors',
            name='wage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]