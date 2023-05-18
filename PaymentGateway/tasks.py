from celery import shared_task
from django.core.management import call_command

@shared_task
def get_order():
    call_command('get_order')

@shared_task
def total_sales_month():
    call_command('total_sales_month')

@shared_task
def total_sales_year():
    call_command('total_sales_year')

@shared_task
def total_sales():
    call_command('total_sales')

@shared_task
def total_sales_yesterday():
    call_command("total_sales_yesterday")

@shared_task
def total():
    call_command("total")