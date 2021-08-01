from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import include, path
from .views import RegisterAPIView, LoginAPIView, LogoutAllView, LogoutAPIView, VerifyOTP, RefreshTokenView
from .tests import TestAPIView, DecryptAPIView

app_name = 'authentication'

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('verify_otp', VerifyOTP.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('refresh/token', RefreshTokenView.as_view()),


    # path('logout/all/devices', LogoutAllView.as_view()),
    # path('test', TestAPIView.as_view()),
    # path('test2', DecryptAPIView.as_view()),
    
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
