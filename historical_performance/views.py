from rest_framework import viewsets
from rest_framework.response import Response
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from purchase_orders.models import PurchaseOrder
from vendors.models import Vendor
from django.db.models import Count, Avg
from django.utils import timezone
from rest_framework.decorators import action
from django.db.models import F


class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

    def calculate_and_save_metrics(self, vendor, date):
        # Retrieve metrics for the given vendor and date
        completed_pos = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            delivery_date__lte=date
        ).count()

        total_pos = PurchaseOrder.objects.filter(
            vendor=vendor,
            delivery_date__lte=date
        ).count()

        quality_rating_avg = PurchaseOrder.objects.filter(
            vendor=vendor,
            quality_rating__isnull=False,
            acknowledgment_date__lte=date
        ).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0

        average_response_time = PurchaseOrder.objects.filter(
            vendor=vendor,
            acknowledgment_date__isnull=False,
            acknowledgment_date__lte=date
        ).aggregate(Avg('acknowledgment_date' - F('issue_date')))['acknowledgment_date__avg'] or 0.0

        fulfillment_rate = (completed_pos / total_pos) * 100 if total_pos > 0 else 0.0

        # Save the metrics to the HistoricalPerformance model
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=date,
            on_time_delivery_rate=fulfillment_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Custom Action to Calculate and Save Historical Metrics
    @action(detail=False, methods=['post'])
    def calculate_metrics(self, request):
        vendor_id = request.data.get('vendor_id')
        date = request.data.get('date')

        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'detail': 'Vendor not found.'}, status=404)

        self.calculate_and_save_metrics(vendor, date)

        return Response({'detail': 'Metrics calculated and saved successfully.'})