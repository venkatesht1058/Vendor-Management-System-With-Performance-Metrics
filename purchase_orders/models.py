from django.db import models
from django.utils import timezone
from django.db.models import F
import json


class QualityIssue(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    description = models.TextField()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.update_performance_metrics()

    def delete(self, *args, **kwargs):
        vendor = self.vendor
        super().delete(*args, **kwargs)
        vendor.update_performance_metrics()

    def update_acknowledgment(self):
        if self.acknowledgment_date is not None:
            response_time = (self.acknowledgment_date - self.issue_date).total_seconds()
            self.vendor.average_response_time = ((self.vendor.average_response_time * self.vendor.purchaseorder_set.count()) +
                                                 response_time) / (self.vendor.purchaseorder_set.count() + 1)
            self.vendor.save()

    

    def save_issue(self):
        self.vendor.fulfillment_rate = (self.vendor.purchaseorder_set.filter(status='completed', qualityissue__isnull=True).count() /
                                       self.vendor.purchaseorder_set.filter(status='completed').count()) * 100
        self.vendor.save()

    def update_performance_metrics(self):
        completed_orders = self.vendor.purchaseorder_set.filter(status='completed')

        # On-Time Delivery Rate
        on_time_deliveries = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
        self.vendor.on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

        # Quality Rating Average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        self.vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

        # Average Response Time
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=F('acknowledgment_date') - F('issue_date')
        ).values_list('response_time', flat=True)

        # Convert timedelta to seconds
        response_times_seconds = [response.total_seconds() for response in response_times]

        self.vendor.average_response_time = sum(response_times_seconds) / len(response_times_seconds) if len(response_times_seconds) > 0 else 0
        self.vendor.save()

        # Fulfillment Rate
        successful_deliveries = completed_orders.exclude(qualityissue__isnull=False)
        self.vendor.fulfillment_rate = (successful_deliveries.count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0
        self.vendor.save()
    


    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

