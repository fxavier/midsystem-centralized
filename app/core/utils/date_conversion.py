from datetime import datetime


class DateConversion:

    @staticmethod
    def convert_str_date(strDate):
        if strDate is None:
            date_str_format = '1900-01-01 00:00:00'
            return datetime.strptime(date_str_format, '%Y-%m-%d %H:%M:%S')
        date_format = str(strDate[0:10]) + ' ' + '00:00:00'
        return datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def validate_phone_number(phone_number):
        """
        Validates and formats a phone number based on specific rules.

        Args:
        phone_number (str): The phone number to validate and format.

        Returns:
        str: Formatted phone number if valid, otherwise returns None.

        """
        # Check if phone_number is None or empty
        if phone_number is None:
            return None

        if phone_number.startswith("258") and len(phone_number) >= 12:

            return phone_number[:12]

        elif phone_number.startswith("8") and len(phone_number) >= 9:

            return "258" + phone_number[:9]
        else:
            # If the number doesn't meet the criteria, it's considered invalid
            return None
