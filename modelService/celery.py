import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modelService.settings')

# app = Celery('proj',
#              broker='amqp://guest@localhost:5672//',
#              include=['model_prediction.tasks'])


app = Celery('modelService',broker='amqp://guest@rabbitmq//')
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#guest:guest@rabbitmq:5672

# Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

if __name__ == '__main__':
    app.start()