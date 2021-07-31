from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from ..users.models import Users



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    phone = serializers.CharField(max_length=255, min_length=4)
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['password', 'phone', 'otp']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)








class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['username', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['otp']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
