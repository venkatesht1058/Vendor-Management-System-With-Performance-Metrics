from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework.decorators import action
from django.utils import timezone


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # Create Purchase Order
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        self.perform_create(serializer)

        serializer.instance.vendor.update_performance_metrics()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
        
        #serializer.save()
        #return Response(serializer.data, status=201)

    # List Purchase Orders
    def list(self, request, *args, **kwargs):
        queryset = PurchaseOrder.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Retrieve Purchase Order
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Update Purchase Order
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Delete Purchase Order
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    
    # Acknowledge Purchase Order
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        purchase_order.update_acknowledgment()
        return Response({'detail': 'Purchase Order acknowledged successfully.'}, status=status.HTTP_200_OK)
    

    # Issue Purchase Order
    @action(detail=True, methods=['post'])
    def issue(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.issue_date = timezone.now()
        purchase_order.save()
        purchase_order.save_issue()
        return Response({'detail': 'Purchase Order issued successfully.'})

    # Custom Action
    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk=None):
        purchase_order = self.get_object()
        custom_attribute_value = request.data.get('custom_attribute')
        purchase_order.custom_attribute = custom_attribute_value
        purchase_order.save()
    
        return Response({'detail': 'Custom action performed successfully.', 'custom_attribute': custom_attribute_value})