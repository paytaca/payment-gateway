# from django.conf.urls import url
from django.urls import path, include
from .views import (
    UserApiView,
    StorefrontApiView,
    OrdersApiView,
    OrdersTotalSalesByMonthApiView,
    TestView,
    CreateTestView
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('bch_api/', include(bch_urls)),
    
    # path('users', UserApiView.as_view()),
    
    path('storefront', StorefrontApiView.as_view()),
    
    path('orders', OrdersApiView.as_view()),
    path('orders/total/', OrdersTotalSalesByMonthApiView.as_view()),
    
    path('test/list/', TestView.as_view()),
    path('test/create/', CreateTestView.as_view()),
]