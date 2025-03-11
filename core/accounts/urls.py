from django.urls import path

from accounts.views import SigningOtpView , SendNumberOtpView

urlpatterns = [

    path('otp/send', SendNumberOtpView.as_view()),
    path('otp/verify', SigningOtpView.as_view()),


]