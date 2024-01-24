from dataclasses import dataclass
from datetime import datetime
import requests
import json
import os
from django.conf import settings
import logging
from core.utils.date_conversion import DateConversion
from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)

filename = os.path.join(settings.BASE_DIR, 'bulk_sending.log')
logging.basicConfig(filename=filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class DataService:
    database_conf = DatabaseConfig.objects.get(pk=1)

    @classmethod
    def create_payload(
        cls, queryset, group_id, date_attribute=None, gender_attribute=None
    ):
        payload = None
        payload_list = []
        for item in queryset:
            # Validate phone number
            valid_phone = DateConversion.validate_phone_number(
                item.phone_number.strip()
            )

            # Skip adding to payload if phone number is invalid
            if valid_phone is None:
                continue

            # Construct payload dictionary
            property_dict = {
                "patient_identifier": item.patient_identifier,
            }

            # Add date_attribute (e.g., next_appointment_date) if provided
            if date_attribute and hasattr(item, date_attribute):
                date_value = getattr(item, date_attribute)
                property_dict[date_attribute] = date_value.strftime('%Y-%m-%d') if date_value else None

            # Add gender_attribute if provided
            if gender_attribute and hasattr(item, gender_attribute):
                property_dict[gender_attribute] = getattr(item, gender_attribute)

            # Add remaining properties
            property_dict.update({
                "pregnant": item.pregnant,
                "age": item.age,
                "district": item.district,
                "province": item.province,
                "health_facility": item.health_facility
            })

            payload = {
                "phone": valid_phone,
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": group_id,
                "active": "1",
                "property": property_dict
            }

            payload_list.append(payload)
           # payload = json.dumps(payload_list, indent=4)

        return payload_list
          
    @classmethod
    def post_bulk_data(cls, payload):
       
        try:
            response = requests.post(
                f'{cls.database_conf.viamo_api_url}?api_key={cls.database_conf.viamo_api_public_key}', json=payload)
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
    def post_bulk_sms_reminder(cls):
        queryset = Visit.objects.exclude(
            phone_number=None)
        payload = cls.create_payload(
            queryset, "463089", "appointment_date", "gender")
        # Split payload into chunks of 500
        chunks = [payload[i:i + 500] for i in range(0, len(payload), 500)]

        for chunk in chunks:
            response = requests.post(
                f'{cls.database_conf.viamo_api_url}?api_key={cls.database_conf.viamo_api_public_key}', json=chunk)
            print(f'SMS REMINDERS: {response.json()}')
            print(len(chunk), 'records sent')
     

    @classmethod
    def post_bulk_vl_eligibility(cls):
        queryset = PatientEligibleVLCollection.objects.exclude(
            phone_number=None)
        payload = cls.create_payload(queryset, "696884",  "gender")
        # Split payload into chunks of 500
        chunks = [payload[i:i + 500] for i in range(0, len(payload), 500)]
    
        for chunk in chunks:
            response = requests.post(
                f'{cls.database_conf.viamo_api_url}?api_key={cls.database_conf.viamo_api_public_key}', json=chunk)
            print(f'VL ELEGIBILITY: {response.json()}')
            print(len(chunk), 'records sent')

    @classmethod
    def post_bulk_vl_test_result(cls):
        queryset = ViralLoadTestResult.objects.exclude(
            phone_number=None)
        payload = cls.create_payload(queryset, "696885",  "gender")
        # Split payload into chunks of 500
        chunks = [payload[i:i + 500] for i in range(0, len(payload), 500)]
    
        for chunk in chunks:
            response = requests.post(
                f'{cls.database_conf.viamo_api_url}?api_key={cls.database_conf.viamo_api_public_key}', json=chunk)
            print(f'VL TEST RESULT: {response.json()}')
            print(len(chunk), 'records sent')
      
   