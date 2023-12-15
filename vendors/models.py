from django.db import models
from django.utils import timezone
from datetime import timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        # On-Time Delivery Rate
        on_time_deliveries = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date'))
        self.on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

        # Quality Rating Average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

        # Average Response Time
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).values_list('response_time', flat=True)
        self.average_response_time = sum(response_times, timedelta()) / len(response_times) if len(response_times) > 0 else 0

        # Convert timedelta to seconds
        response_times_seconds = [response.total_seconds() for response in response_times]
        self.average_response_time = sum(response_times_seconds) / len(response_times_seconds) if len(response_times_seconds) > 0 else 0
        self.save()

        # Fulfillment Rate
        successful_deliveries = completed_orders.exclude(qualityissue__isnull=False)
        self.fulfillment_rate = (successful_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

        self.save()

    def __str__(self):
        return self.name
