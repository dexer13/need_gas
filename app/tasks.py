from celery import shared_task
from app.core import Delivery

@shared_task
def task_start_delivery(service):
    Delivery(service).start_delivery()
