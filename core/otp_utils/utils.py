import logging
import os

from core.settings import FARAZ_SMS_API_KEY, FARAZ_SMS_PATTERN_CODE, KAVENEGAR_API_KEY
from kavenegar import *
import requests
from requests.exceptions import RequestException

# تنظیمات لاگگیری
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import json

def send_otp_code( phone_number , code ):

    try:
        import json
    except ImportError:
        import simplejson as json
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'sender': '20006535',
            'receptor': str(phone_number),
            'message': 'Kaveh specialized Web service '
        }
        response = api.sms_send(params)
        print(str(response))

    except APIException as e:
        print (str(e))

    except HTTPException as e:
        print (str(e))





def send_faraz_otp_code(phone_number: str| int, code: str) -> bool:



    try:
        # اعتبارسنجی اولیه
        if not all([phone_number, code]):
            raise ValueError("شماره همراه و کد نمی‌توانند خالی باشند")

        phone_number = str(phone_number).strip()
        if not phone_number.startswith('98') or len(phone_number) != 12:
            raise ValueError("فرمت شماره همراه نامعتبر است. باید با 98 شروع شود و 12 رقمی باشد")

        # دریافت تنظیمات از محیطی امن
        api_key = FARAZ_SMS_API_KEY
        pattern_code = FARAZ_SMS_PATTERN_CODE

        url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

        payload = {
            "code": pattern_code,
            "sender": "3000505",
            "recipient": phone_number,
            "variable": {"code": code}
        }

        headers = {
            'apikey': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'OTP-Service/1.0'
        }

        # ارسال درخواست با timeout و SSL verification
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10,
            verify=True
        )

        # بررسی وضعیت پاسخ
        response.raise_for_status()

        # پردازش پاسخ JSON
        response_data = response.json()

        if response_data.get('status') == 'success':
            logger.info(f"پیامک با موفقیت به {phone_number} ارسال شد")
            return True

        logger.error(f"خطا در ارسال پیامک: {response_data.get('message')}")
        return False

    except ValueError as ve:
        logger.error(f"خطای اعتبارسنجی: {str(ve)}")
        return False

    except RequestException as re:
        logger.error(f"خطای ارتباطی: {str(re)}")
        raise  # برای Retry در Celery

    except Exception as e:
        logger.critical(f"خطای غیرمنتظره: {str(e)}", exc_info=True)
        return False