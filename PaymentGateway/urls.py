from django.urls import path
from .views import ProcessOrderAPIView

urlpatterns = [
    path('process-order/', ProcessOrderAPIView.as_view(), name='process_order'),
]