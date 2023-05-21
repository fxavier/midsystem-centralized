from dataclasses import dataclass
from datetime import date, timedelta

import requests
from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)


@dataclass
class PostData:
    database_conf = DatabaseConfig.objects.get(pk=1)

    @classmethod
    def create_payload(cls, queryset, group_id, date_attribute=None):
        payload_list = []
        for item in queryset:
            phone = item.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": group_id,
                "active": "1",
            }

            data_values = {
                "patient_identifier": item.patient_identifier,
                "gender": item.gender,
                "pregnant": item.pregnant,
                "age": item.age,
                "district": item.district,
                "province": item.province,
                "health_facility": item.health_facility
            }
            if date_attribute:
                data_values[date_attribute] = '{:%Y-%m-%d}'.format(
                    getattr(item, date_attribute))

            payload['property'] = data_values
            payload_list.append(payload)

            item.synced = True
            item.save()

        return payload_list

    @classmethod
    def post_data(cls, payload_list):
        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records + 1} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())
            print(f'Records not sent: {records_not_sent}')
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def post_sms_reminder(cls):
        queryset = Visit.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(
            queryset, "463089", "next_appointment_date")
        cls.post_data(payload_list)

    @classmethod
    def post_missed_appointment(cls):
        queryset = MissedAppointment.objects.exclude(phone_number=None)
        payload_list = cls.create_payload(
            queryset, "485273", "last_appointment_date")
        cls.post_data(payload_list)

    @classmethod
    def post_eligible_for_vl(cls):
        queryset = PatientEligibleVLCollection.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(queryset, "696884")
        cls.post_data(payload_list)

    @classmethod
    def post_vl_test_result(cls):
        queryset = ViralLoadTestResult.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(queryset, "696885")
        cls.post_data(payload_list)
