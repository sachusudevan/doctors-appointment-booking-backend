from core.messages import Messages
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from core.response import ResponseInfo
from django.test import TestCase
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail, EmailMessage

import random
import string
import threading
from core.hashing import Hash
# Create your tests here.

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



class TestAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(TestAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Testing"])
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            subject = Messages.messages(1)
            message = f'Hi {username}, thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            email = EmailMessage(
                subject=subject, body=message, to=[email])
            EmailThread(email).start()

            # send_mail( subject, message, email_from, recipient_list )
            self.response_format['data'] = request.data
            self.response_format['status'] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            self.response_format['data'] = request.data
            return Response(self.response_format, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Testing"])
    def get(self, request):
        self.response_format['status'] = False
        # self.response_format['message2'] = random.randint(100000, 999999)
        self.response_format['message1'] = Hash.bcrypt({"key": 12345678})
        # self.response_format['message'] = ''.join(
        #     (random.choice(string.ascii_uppercase) for x in range(6)))
        
        self.response_format['data'] = request.data
        return Response(self.response_format, status=status.HTTP_200_OK)


class DecryptAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DecryptAPIView, self).__init__(**kwargs)


    @swagger_auto_schema(tags=["Testing"])
    def get(self, request):
        key = request.data.get('key')
        otp = request.data.get('otp')
        self.response_format['status'] = False
        self.response_format['message1'] = Hash.verify(key,otp)
        self.response_format['data'] = request.data
        return Response(self.response_format, status=status.HTTP_200_OK)
