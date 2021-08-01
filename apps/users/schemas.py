

from rest_framework import serializers
from .models import Users

class UpdatePostUserSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'first_name', 'last_name', 'address','place']


class UpdateUserSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 'username',
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser','address','place']
