from ..users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from core.response import ResponseInfo
from .serializers import RefreshTokenSerializer, UserSerializer, LoginSerializer, LogoutSerializer, OTPSerializer
from .schemas import LoginPostSchema, RegisterPostSchema, RegisterSchema, LoginSchema, UsersSchema, VerifyOTPPostSchema
from core.utils import Util
from core.hashing import Hash

from .emails import RegistrationEmail

# Create your views here.

class RegisterAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterAPIView, self).__init__(**kwargs)

    serializer_class = RegisterPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            otp = Util.random_number()
            user_data.update({"otp": Hash.bcrypt({"key": otp})})
            user_data.update({"plain_otp": otp})
            # return Response(RegistrationEmail.send(user_data), status=status.HTTP_200_OK)
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                # RegistrationEmail.send(user_data)
                data = request.data
                phone = data.get('phone', '')
                password = data.get('password', '')
                user = auth.authenticate(username=phone, password=password)
                if user:
                    refresh = RefreshToken.for_user(user)
                    serializer = RegisterSchema(user)
                    data = {'user': serializer.data, 'errors': {}, 'token': str(
                        refresh.access_token), 'refresh': str(refresh), 'otp': otp}
                    self.response_format['status_code'] = 200
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = 106
                    data = {'user': serializer.data, 'errors': {}, 'token': '', 'refresh': '', 'otp': ''}
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_201_CREATED)
            else:
                self.response_format['status_code'] = 102
                data = {'user': {}, 'errors': serializer.errors,
                        'token': '', 'refresh': '', 'otp': ''}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)



class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    serializer_class = LoginPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            data = request.data
            phone = data.get('phone', '')
            password = data.get('password', '')
            user = auth.authenticate(username=phone, password=password)
            if user:
                serializer = LoginSchema(user)

                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = 107
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    self.response_format["message"] = 'Account Temparary suspended, contact admin'
                    return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    refresh = RefreshToken.for_user(user)
                    data = {'user': serializer.data, 'token': str(
                        refresh.access_token), 'refresh': str(refresh)}
                    self.response_format['status_code'] = 200
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)

            else:
                self.response_format['status_code'] = 106
                self.response_format["data"] = {'detail': 'Invalid credentials'}
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)





class VerifyOTP(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyOTPPostSchema
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(VerifyOTP, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            otp = request.data.get('otp', '')
            if(otp):
                user_data = Users.objects.get(id=request.user.id)
                if (user_data.is_verified  == 0):
                    if(Hash.verify(user_data.otp, int(otp))):
                        user_data.is_verified = 1
                        user_data.otp = ''
                        user_data.save()
                        serializer = UsersSchema(user_data)
                        data = {'user' : serializer.data, 'errors': {}}
                        self.response_format['data'] = data
                        self.response_format['status_code'] = 200
                        return Response(self.response_format, status=status.HTTP_200_OK)
                        
                    else:
                        data = {'user': {}, 'errors': {'message': 'Invalid OTP'}}
                        self.response_format['status_code'] = 104
                        self.response_format['data'] = data
                        return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    serializer = UsersSchema(user_data)
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format['message'] = 'Already Verified'
                    self.response_format['status_code'] = 105
                    self.response_format['data'] = data
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                data = {'user': {}, 'errors': {'message': 'Invalid OTP'}}
                self.response_format['status_code'] = 103
                self.response_format['data'] = data
                return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = 200
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = 101
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)







class LogoutAllView(GenericAPIView):
    pass
    # permission_classes = (IsAuthenticated,)
    # def __init__(self, **kwargs):
    #     self.response_format = ResponseInfo().response
    #     super(LogoutAllView, self).__init__(**kwargs)

    # @swagger_auto_schema(tags=["Authorization"])
    # def post(self, request):
    #     pass
        # tokens = OutstandingToken.objects.filter(user_id=request.user.id)
    #     for token in tokens:
    #         t, _ = BlacklistedToken.objects.get_or_create(token=token)

    #     return Response(status=status.HTTP_205_RESET_CONTENT)




class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)




