import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_upload.settings')

app = Celery('file_upload')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
