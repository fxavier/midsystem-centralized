from __future__ import absolute_import, unicode_literals

from celery import shared_task

# from core.models import (DatabaseConfig, MissedAppointment,
#                          PatientEligibleVLCollection, ViralLoadTestResult,
#                          Visit)
from core.services.post_data import PostData


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
