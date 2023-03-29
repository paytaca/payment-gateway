from celery import shared_task
from django.core.management import call_command

@shared_task
def get_order():
    call_command('get_order')