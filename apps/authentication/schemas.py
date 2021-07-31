
from rest_framework import serializers
from ..users.models import Users


class RegisterSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'username',
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']


class LoginSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'username',
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']


class UsersSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'username',
                  'first_name', 'last_name', 'date_joined', 'is_admin', 'is_active', 'is_verified', 'is_superuser']



# class VerifyOTPSchema(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['otp']
