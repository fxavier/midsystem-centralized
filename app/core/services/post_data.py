from dataclasses import dataclass
from datetime import datetime
import csv
import requests
from django.conf import settings
import os
import logging
from core.utils.date_conversion import DateConversion
from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)

# Obtain a logger instance
# logger = logging.getLogger('app')

# Configure logging
filename = os.path.join(settings.BASE_DIR, 'bulk_sending.log')
logging.basicConfig(filename=filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class PostData:
    database_conf = DatabaseConfig.objects.get(pk=1)

    @classmethod
    def create_payload(
        cls, queryset,
        group_id,
        date_attribute=None,
        gender_attribute=None
    ):
        payload_list = []
        for item in queryset:
            # Validate phone number
            valid_phone = DateConversion.validate_phone_number(
                item.phone_number.strip()
            )

            # Skip adding to payload if phone number is invalid
            if valid_phone is None:
                continue

            payload = {
                "phone": valid_phone,
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": group_id,
                "active": "1",
            }

            data_values = {
                "patient_identifier": item.patient_identifier,
                "pregnant": item.pregnant,
                "age": item.age,
                "district": item.district,
                "province": item.province,
                "health_facility": item.health_facility
            }

            if date_attribute:
                data_values[date_attribute] = '{:%Y-%m-%d}'.format(
                    getattr(item, date_attribute))

            if gender_attribute:
                data_values[gender_attribute] = getattr(item, gender_attribute)

            payload["property"] = data_values
            payload_list.append(payload)

            item.sent = True
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
                    records += 1
            print(f'Records not sent: {records_not_sent}')
        except requests.exceptions.RequestException as err:
            print(err)

    # @classmethod
    # def post_bulk_data(cls, payload_list):
    #     try:
    #         headers = {
    #             "Authorization": f"Bearer {cls.database_conf.viamo_api_public_key}"}
    #         response = requests.post(
    #             cls.database_conf.viamo_api_url,
    #             json={"subscribers": payload_list},
    #             headers=headers
    #         )

    #         if response.status_code == 200:
    #             response_data = response.json()
    #             if 'message' in response_data and response_data['message'] == "Subscriber(s) created successfully!":
    #                 print(f"Success! Group ID: {response_data['data']}")
    #             else:
    #                 print(
    #                     f"Failed to create subscribers. Bad Input. Problematic numbers: {response_data['data']}")
    #         else:
    #             print(
    #                 f"Request failed with status code: {response.status_code}")
    #             print(response.text)
    #     except requests.exceptions.RequestException as err:
    #         print(err)

    @classmethod
    def post_bulk_data(cls, payload_list):
        try:
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "subscribers": payload_list
            }
            response = requests.post(
                cls.database_conf.viamo_api_url, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                if 'message' in response_data and response_data['message'] == "Subscriber(s) created successfully!":
                    logging.info(f"Success! Group ID: {response_data['data']}")
                else:
                    logging.warning(
                        f"Failed to create subscribers. Bad Input. Problematic numbers: {response_data['data']}")
            else:
                logging.error(
                    f"Request failed with status code: {response.status_code}")
                logging.error(response.text)  # To help diagnose the issue
        except requests.exceptions.RequestException as err:
            logging.exception(f"RequestException: {err}")

    @classmethod
    def post_sms_reminder(cls):
        queryset = Visit.objects.exclude(
            phone_number=None)
        payload_list = cls.create_payload(
            queryset, "463089", "next_appointment_date", "gender")
        print(payload_list[:20])
        cls.post_bulk_data(payload_list[:20])

    @classmethod
    def post_missed_appointment(cls):
        queryset = MissedAppointment.objects.exclude(phone_number=None)
        payload_list = cls.create_payload(
            queryset, "485273", "last_appointment_date", "gender")
        cls.post_data(payload_list)

    @classmethod
    def post_eligible_for_vl(cls):
        queryset = PatientEligibleVLCollection.objects.exclude(
            phone_number=None)  # .filter(sent=False)
        payload_list = cls.create_payload(queryset, "696884")
        cls.post_data(payload_list)

    @classmethod
    def post_vl_test_result(cls):
        queryset = ViralLoadTestResult.objects.exclude(
            phone_number=None)  # .filter(sent=False)
        payload_list = cls.create_payload(queryset, "696885")
        cls.post_data(payload_list)

    def fetch_data_created_today(cls):
        today = datetime.now().date()
        visits_today = Visit.objects.filter(created_at=today)
        return visits_today

    def save_appointments_to_csv(queryset, filename, filepath):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the headers to the CSV file
            writer.writerow([field.name for field in Visit._meta.fields])

            # Write the data rows to the CSV file
            for visit in queryset:
                row = [getattr(visit, field.name)
                       for field in Visit._meta.fields]
                writer.writerow(row)
