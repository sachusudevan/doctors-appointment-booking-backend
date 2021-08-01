from django.urls import include, path
from .views import UpdateUserAPIView

app_name = 'users'

urlpatterns = [
    path('update', UpdateUserAPIView.as_view()),

]
