from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from purchase_orders.views import PurchaseOrderViewSet

router = routers.DefaultRouter()
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
