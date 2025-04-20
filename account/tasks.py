from celery import shared_task
from kavenegar import KavenegarAPI, APIException
import random
from django.core.cache import cache
from django.conf import settings

my_apikey = settings.KAVENEGAR_API_KEY




@shared_task
def send_otp_task(phone_number):
    try:
        code  = str(random.randint(100000, 999999))
        cache.set(f"otp_{phone_number}", code, timeout=300)

        api = KavenegarAPI(my_apikey)
        params = {
            'receptor':phone_number,
            'sender':2000660110,
            'message':f"Your Validated code is {code}",
        }
        api.sms_send(params)
        return f"OTP sent to {phone_number}"
    except APIException as e:
        return f"Kavenegar Error:{str(e)}"
  
    





