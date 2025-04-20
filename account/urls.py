from django.urls import path
from .views import SendOTPView



urlpatterns = [
    path("create-account/", SendOTPView.as_view()),

]
