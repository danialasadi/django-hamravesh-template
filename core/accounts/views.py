import pyotp
from django.core.cache import cache

# Create your views here.

from rest_framework.generics import CreateAPIView

from django.contrib.auth import get_user_model
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import serializers
from accounts.serializers import OtpSerializer, ObtainTokenSerializer
from accounts.tasks import celery_send_otp_sms


# Create your views here.
class SendNumberOtpView(CreateAPIView):


    serializer_class = OtpSerializer

    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'otp'

    def perform_create(self, serializer):

        try:
            phone_number = serializer.validated_data['phone_number']
        except KeyError:
            return Response({'error': 'No phone number provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            totp = pyotp.TOTP('base32secret3232',digits=6)
            code = totp.now()  # => '492039'
            cache.set(f'{phone_number}',  code , timeout=60 * 2)
            phone_number='98'+phone_number[1:]
            celery_send_otp_sms.delay(phone_number=phone_number, code=code)
            # send_faraz_otp_code(phone_number=989917411543,code=code)








class SigningOtpView(APIView):

    serializer_class = ObtainTokenSerializer
    queryset = None
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'otp'

    def post(self, request):
        ser_data = serializers.OtpSerializer(data=request.data)
        if ser_data.is_valid():
            try:
                phone_number = ser_data.validated_data['phone_number']
            except KeyError:
                return Response({'error': 'No phone number provided'}, status=status.HTTP_400_BAD_REQUEST)
            else:

                if cache.__contains__(phone_number):

                    try:
                        code = ser_data.validated_data['code']
                    except KeyError:
                        return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        redis_code = cache.get(f'{phone_number}')
                        if code == redis_code :
                            user, created = get_user_model().objects.get_or_create(phone_number=phone_number)
                            if created:
                                user.set_unusable_password()
                                user.save()
                            refresh = RefreshToken.for_user(user)
                            token =  serializers.ObtainTokenSerializer({
                                'refresh':str(refresh),
                                'token':str(refresh.access_token),
                                'created':created
                             }).data

                            return Response(token,status=status.HTTP_200_OK)
                        else:
                            return Response({'error': 'Invalid code'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    return Response({'error': 'No phone number provided'}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)




