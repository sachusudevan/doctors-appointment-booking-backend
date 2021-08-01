from apps.authentication.serializers import UserSerializer
from apps.users.serializers import UpdateUsersSerializer
from apps.users.schemas import UpdatePostUserSchema, UpdateUserSchema
from drf_yasg.utils import swagger_auto_schema
from core.response import ResponseInfo
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import Users

# Create your views here.


class UpdateUserAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateUserAPIView, self).__init__(**kwargs)

    serializer_class = UpdatePostUserSchema

    @swagger_auto_schema(tags=["User"])
    def put(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            serializer = UpdatePostUserSchema(user)
            if serializer:
                email = request.data.get('email','')
                phone = request.data.get('phone','')
                first_name = request.data.get('first_name','')
                last_name = request.data.get('last_name','')
                address = request.data.get('address', '')
                place = request.data.get('place', '')
                if email:
                    user.email = email
                if phone:
                    user.phone = phone
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                if first_name and last_name:
                    user.username = first_name + ' ' + last_name
                user.save()

                userserializer = UpdateUserSchema(user)
                data = {'user': userserializer.data, 'errors': {}}
                self.response_format['status_code'] = 100
                self.response_format['data'] = data
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = 102
                data = {'user': {}, 'errors': serializer.errors}
                self.response_format["data"] = data
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_200_OK)


        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)
