from django.urls import include, path
from .views import UpdateUserAPIView

app_name = 'users'

urlpatterns = [
    path('update', UpdateUserAPIView.as_view()),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
