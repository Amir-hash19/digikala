from rest_framework.generics import ListAPIView, CreateAPIView
from .models import CustomUser
from .permission import IsAdminUser, IsSupportUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import SendOTPRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import send_otp_task
from rest_framework import status
from django.core.cache import cache



class SendOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SendOTPRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = str(serializer.validated_data['phone'])
            
            key = f"otp_request_count_{phone_number}"

            # تعداد دفعات فعلی را از Redis بگیر
            request_count = cache.get(key, 0)

            if request_count >= 7:
                return Response(
                    {"message":" You tried more than 7 time"},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            # افزایش شمارنده و تعیین انقضا
            cache.set(key, request_count + 1, timeout=300)  

            send_otp_task.delay(phone_number)
            return Response({"message": "Your code has been sent"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

