import random
from datetime import timedelta


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation.trans_null import gettext_lazy as _
from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255,verbose_name=_("email address"),null=True)
    full_name = models.CharField(max_length=255,verbose_name=_("full name"),null=True)
    phone_number = models.CharField(max_length=11,unique=True,verbose_name=_("phone number"))
    is_active = models.BooleanField(default=True,verbose_name=_("is active"))
    is_staff = models.BooleanField(default=False,verbose_name=_("is staff"))
    password = models.CharField(_("password"), max_length=128,null=True)
    # is_superuser = models.BooleanField(default=False,verbose_name=_("is superuser"))
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email'] # for manage.py  createsuperuser

    objects = UserManager()


    def __str__(self):
        return f'{self.email}'






class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11,unique=True,verbose_name=_("phone number"))
    code = models.CharField(max_length=6,verbose_name=_("code"))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_("created at"))

    @staticmethod
    def generate_otp():
        otp = random.randint(100000, 999999)
        return otp

    def is_expired(self):
        return timezone.now()-self.created_at<timedelta(minutes=2)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created_at}'


