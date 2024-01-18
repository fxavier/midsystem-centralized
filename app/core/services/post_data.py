from dataclasses import dataclass
from datetime import datetime
import csv
import json
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

patient_list = [{"phone": "258840162088", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2015/00403", "next_appointment_date": "2023-12-28", "gender": "F", "pregnant": "NAO", "age": 27, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258847069125", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2013/00134", "next_appointment_date": "2023-12-23", "gender": "F", "pregnant": "NAO", "age": 35, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258852043528", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2014/00096", "next_appointment_date": "2023-12-18", "gender": "F", "pregnant": "NAO", "age": 29, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258845652753", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2015/00389", "next_appointment_date": "2023-12-27", "gender": "F", "pregnant": "NAO", "age": 47, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258845009211", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2015/00406", "next_appointment_date": "2023-12-21", "gender": "F", "pregnant": "NAO", "age": 60, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258862309771", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107023601/2010/00711", "next_appointment_date": "2023-12-20", "gender": "F", "pregnant": "NAO", "age": 14, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258826220238", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2014/00350", "next_appointment_date": "2023-12-20", "gender": "F", "pregnant": "NAO", "age": 35, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258848094209", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2014/00348", "next_appointment_date": "2023-12-27", "gender": "F", "pregnant": "NAO", "age": 28, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258823728569", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2013/00125", "next_appointment_date": "2023-12-27", "gender": "F", "pregnant": "SIM", "age": 25, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258846876972", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00329", "next_appointment_date": "2023-12-17", "gender": "F", "pregnant": "NAO", "age": 19, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258829297091", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107010701/2013/01315", "next_appointment_date": "2023-12-20", "gender": "F", "pregnant": "NAO", "age": 40, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258845832905", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00395", "next_appointment_date": "2023-12-26", "gender": "F", "pregnant": "NAO", "age": 17, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258846756582", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2015/00034", "next_appointment_date": "2023-12-18", "gender": "F", "pregnant": "NAO", "age": 38, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258842815990", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2014/00050", "next_appointment_date": "2023-12-18", "gender": "F", "pregnant": "NAO", "age": 29, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258846172282", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00394", "next_appointment_date": "2023-12-28", "gender": "F", "pregnant": "NAO", "age": 42, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258840563471", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00061", "next_appointment_date": "2023-12-29", "gender": "F", "pregnant": "NAO", "age": 46, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258866303315", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00370", "next_appointment_date": "2023-12-19", "gender": "F", "pregnant": "NAO", "age": 64, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258845648832", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00009", "next_appointment_date": "2023-12-27", "gender": "M", "pregnant": "NAO", "age": 41, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258846544148", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2016/00322", "next_appointment_date": "2023-12-19", "gender": "M", "pregnant": "NAO", "age": 59, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}, {"phone": "258848039597", "receive_voice": "1", "receive_sms": "1", "preferred_channel": "1", "groups": "463089", "active": "1", "property": {"patient_identifier": "0107011101/2010/00015", "next_appointment_date": "2023-12-18", "gender": "F", "pregnant": "NAO", "age": 32, "district": "Beira", "province": "Sofala", "health_facility": "CS Chamba"}}]

@dataclass
class PostData:
    database_conf = DatabaseConfig.objects.get(pk=1)

    @classmethod
    def create_payload(
        cls, queryset, group_id, date_attribute=None, gender_attribute=None
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

            # Append the constructed payload to the list
            payload_list.append(payload)

            # Mark item as sent (if applicable)
            item.sent = True  # Ensure this is appropriate for your application logic
            item.save()

        return payload_list



    @classmethod
    def post_data(cls, payload_list):
        records = 0
       # records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records + 1} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                   # records_not_sent.append(data.copy())
                    records += 1
            #print(f'Records not sent: {records_not_sent}')
        except requests.exceptions.RequestException as err:
            print(err)

   
            
    @classmethod
    def post_bulk_data(cls, payload_list):
       
        try:
            payload = json.dumps(payload_list, indent=4)
            print(payload[:10])
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
    def post_sms_reminder(cls):
        queryset = Visit.objects.exclude(
            phone_number=None)[:100]
        payload_list = cls.create_payload(
            queryset, "463089", "appointment_date", "gender")
        cls.post_bulk_data(payload_list)
    


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
