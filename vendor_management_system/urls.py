
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from vendors.views import VendorViewSet
from purchase_orders.views import PurchaseOrderViewSet
from historical_performance.views import HistoricalPerformanceViewSet

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)
router.register(r'historical_performance', HistoricalPerformanceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    #path('api/historical_performance/', HistoricalPerformanceView.as_view(), name='historical_performance'),
]
