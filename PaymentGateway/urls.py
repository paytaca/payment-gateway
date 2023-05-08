from django.urls import path
from .views import ProcessOrderAPIView, GetOrderAPIView, TotalBCHAPIView, UserApiView, SignUpAPIView, LoginAPIView, WalletAPIView
from .views import TotalSalesAPIView, TotalSalesYesterdayAPIView, TotalSalesByMonthAPIView, TotalSalesByYearAPIView
from .views import user_info
# from . import views

urlpatterns = [
    path('process-order/', ProcessOrderAPIView.as_view(), name='process_order'),
    path('get-order/', GetOrderAPIView.as_view(), name='get_order'),
    path('total-bch/', TotalBCHAPIView.as_view(), name='total_bch'),
    
    path('users', UserApiView.as_view(), name='users'),
    path('user/signup/', SignUpAPIView.as_view(), name='signup'),
    path('user/login/', LoginAPIView.as_view(), name='login'),
    # path('user/info/', views.member_info, name='member_info'),
    path('user/info/', user_info, name='user_info'),
    path('user/wallet-update/', WalletAPIView.as_view(), name='wallet_update'),
    
    path('total-sales/', TotalSalesAPIView.as_view(), name='total_sales'),
    path('total-sales-yesterday/', TotalSalesYesterdayAPIView.as_view(), name='total_sales_yesterday'),
    path('total-sales-month/', TotalSalesByMonthAPIView.as_view(), name='total_sales_by_month'),
    path('total-sales-year/', TotalSalesByYearAPIView.as_view(), name='total_sales_by_year'),
]