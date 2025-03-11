from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError





class UserSerializer(serializers.ModelSerializer):




    class Meta:
        model = get_user_model()
        fields = ('email','full_name','phone_number','articles')

        ##### SerializerMethodField
        # def get_articles(self, obj):
        #     result = obj.articles.all()
        #     from blog.serializers import ArticleSerializer
        #     ser_data = ArticleSerializer(instance=result, many=True)
        #
        #     return ser_data.data





#//////////////////////////////////////

#### inline kwarg validator
def func_name(value):
    if 'admin' in value:
        raise ValidationError('dmin cant be in email')


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)


    class Meta:
        model = get_user_model()
        fields = ('email','full_name','phone_number','password','password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (func_name,)},
        }







    def validate_email(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('email is too short')



    def validate_full_name(self, value):
        if value == "admin":

            raise serializers.ValidationError('full name cant be admin')

        return value


    def validate(self, value):
        if value['password'] != value['password2']:
            raise serializers.ValidationError('password must be match')
        return value




class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('phone_number','password')

#----------------------------------------------------------------------



class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=False,max_length=6,min_length=6)
    phone_number = serializers.CharField(write_only=True,required=True , max_length=11)


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True, max_length=128,allow_null=False)
    refresh = serializers.CharField(read_only=True, max_length=128,allow_null=False)
    created=serializers.BooleanField(read_only=True,allow_null=False )




