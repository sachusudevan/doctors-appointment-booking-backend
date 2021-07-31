
from rest_framework import serializers
from ..users.models import Users


class RegisterPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone','password']


class RegisterSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'username',
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']


class LoginPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone','password']

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



class VerifyOTPPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['otp']
