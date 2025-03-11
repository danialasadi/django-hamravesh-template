from celery import shared_task
import logging

from celery.exceptions import MaxRetriesExceededError

logger = logging.getLogger(__name__)
from lib.utils import send_faraz_otp_code


@shared_task(  bind=True,
    max_retries=2,
               )
def celery_send_otp_sms(self,phone_number, code):
    try:
        send_faraz_otp_code(phone_number, code)
    except Exception as exc:
        logger.error(f"Failed to send OTP to {phone_number}: {exc}")
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.critical(f"Max retries exceeded for {phone_number}")