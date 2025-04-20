import os
from celery import Celery

# تنظیم محیط پیش‌فرض جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digikala.settings')

# ساخت اپ celery
app = Celery("digikala")

# ست کردن Redis به‌عنوان message broker
app.conf.broker_url = 'redis://localhost:6379/0'

# ذخیره نتایج تسک‌ها در Redis
app.conf.result_backend = 'redis://localhost:6379/1'

# اختیاری: ذخیره‌ی نتایج در RPC
# app.conf.result_backend = 'rpc://'

# لود کردن تسک‌ها از اپ‌های جنگو 
app.config_from_object('django.conf:settings', namespace='CELERY')

# خودکار کشف تسک‌ها
app.autodiscover_tasks()
