from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from vendors.views import VendorViewSet

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
