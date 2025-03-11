from datetime import timedelta
from django.utils import timezone

from django.core.management.base  import BaseCommand

from accounts.models import OtpCode


class Command(BaseCommand):
    help = 'remove all expired otp codes'


    def handle(self, *args, **options ):
        expired_time = expired_time = timezone.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created_at__lt=expired_time).delete()
        self.stdout.write("Expired OTP codes removed successfully.")
