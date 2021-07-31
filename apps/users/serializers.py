


from rest_framework import serializers
from .models import Users


class UpdateUsersSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20, min_length=10)
    first_name = serializers.CharField(max_length=200, min_length=2)
    last_name = serializers.CharField(max_length=200, min_length=2)
    email = serializers.EmailField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['email','phone','first_name', 'last_name']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
        return super().validate(attrs)
