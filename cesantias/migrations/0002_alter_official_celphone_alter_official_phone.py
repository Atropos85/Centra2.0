# Generated by Django 5.1.1 on 2024-10-02 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cesantias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='official',
            name='celphone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='official',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
