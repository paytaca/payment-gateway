# from django.conf.urls import url
from django.urls import path, include
from .views import (
    TestApiView,
    TestTotalSalesByMonthApiView
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('bch_api/', include(bch_urls)),
    path('api', TestApiView.as_view()),
    path('api/total/', TestTotalSalesByMonthApiView.as_view()),
]