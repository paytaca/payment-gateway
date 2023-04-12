# from django.conf.urls import url
from django.urls import path, include
from .views import (
    TestApiView,
    TestTotalSalesByMonthApiView,
)

urlpatterns = [
    path('api', TestApiView.as_view()),
    path('api/total/', TestTotalSalesByMonthApiView.as_view()),
]