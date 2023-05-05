from django.urls import path
from .views import ProcessOrderAPIView, GetOrderAPIView, TotalBCHAPIView, UserApiView, SignUpAPIView, LoginAPIView, WalletAPIView

urlpatterns = [
    path('process-order/', ProcessOrderAPIView.as_view(), name='process_order'),
    path('get-order/', GetOrderAPIView.as_view(), name='get-order'),
    path('total-bch/', TotalBCHAPIView.as_view(), name='total-bch'),
    
    path('users', UserApiView.as_view(), name='users'),
    path('user/signup/', SignUpAPIView.as_view(), name='signup'),
    path('user/login/', LoginAPIView.as_view(), name='login'),
    path('user/wallet-update/', WalletAPIView.as_view(), name='wallet-update'),
    # path('generate-bch-address/', GenerateBchAddressAPIView.as_view(), name='generate-bch-address')
]