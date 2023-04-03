# from django.conf.urls import url
from django.urls import path, include
from .views import (
    TestApiView,
    TestDetailApiView,
)

urlpatterns = [
    path('api', TestApiView.as_view()),
    path('api/<int:todo_id>/', TestDetailApiView.as_view()),
]