# Generated by Django 3.2.19 on 2023-05-19 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230519_1930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pacientescargaalta',
            options={'verbose_name': 'Paciente com Carga viral alta', 'verbose_name_plural': 'Pacientes com Carga viral alta'},
        ),
        migrations.AlterField(
            model_name='elegiveiscv',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='marcadoslevantamento',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pacientescargaalta',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
