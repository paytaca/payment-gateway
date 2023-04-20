from django.urls import path
from .views import ProcessOrderAPIView, GetOrderAPIView, TotalBCHAPIView

urlpatterns = [
    path('process-order/', ProcessOrderAPIView.as_view(), name='process_order'),
    path('get-order/', GetOrderAPIView.as_view(), name='get-order'),
    path('total-bch/', TotalBCHAPIView.as_view(), name='total-bch')
]