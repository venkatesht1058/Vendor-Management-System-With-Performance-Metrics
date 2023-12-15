
from django.contrib import admin
from django.urls import path, include
from historical_performance.urls import urlpatterns as historical_urls

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include(historical_urls)),
]
