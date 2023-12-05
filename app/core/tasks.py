from __future__ import absolute_import, unicode_literals

from celery import shared_task

# from core.models import (DatabaseConfig, MissedAppointment,
#                          PatientEligibleVLCollection, ViralLoadTestResult,
#                          Visit)
from django.conf import settings
from core.services.post_data import PostData
from core.services import fetch_data
from datetime import datetime
from core.models import Visit
import csv
import os


@shared_task
def Envio_pacientes_marcados_levantamento():
    PostData.post_sms_reminder()


@shared_task
def Envio_faltosos_ao_levantamento_ou_consulta():
    PostData.post_missed_appointment()


@shared_task
def envio_eligiveis_carga_viral():
    PostData().post_eligible_for_vl()


@shared_task
def envio_pacientes_carga_viral_alta():
    PostData().post_vl_test_result()


@shared_task
def save_to_csv():
   # today = datetime.now().date()
   # queryset = Visit.objects.filter(created_at=today)
    queryset = Visit.objects.exclude(phone_number=None)
    # Set filename with absolute path to the root of the Django project
    filename = os.path.join(
        settings.BASE_DIR, f'visits_{datetime.now().strftime("%Y%m%d")}.csv')
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the headers to the CSV file
        field_names = [
            field.name for field in Visit._meta.fields if field.name != 'patient_name']
        writer.writerow(field_names)

        # Write the data rows to the CSV file
        for visit in queryset:
            row = [getattr(visit, field.name)
                   for field in Visit._meta.fields if field.name != 'patient_name']
            writer.writerow(row)
        if queryset.exists():
            print(f'Data saved to {filename} locally.')
        else:
            print('No visits found for today.')
