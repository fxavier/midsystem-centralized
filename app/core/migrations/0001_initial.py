# Generated by Django 3.2.19 on 2023-05-19 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElegiveisCv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_facility', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
                ('patient_id', models.IntegerField()),
                ('nid', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.DecimalField(decimal_places=0, max_digits=7)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]