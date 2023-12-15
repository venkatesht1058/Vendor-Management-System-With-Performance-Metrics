from django.db import models
from vendors.models import Vendor

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfilment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
