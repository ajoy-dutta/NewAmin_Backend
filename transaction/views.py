from django.shortcuts import render
from rest_framework import generics
from .models import*
from .serializers import*
import json
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy() 
        
        for field in ["transaction_details", "purchase_details"]:
            if isinstance(data.get(field), str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response({f"error": f"Invalid JSON format for {field}"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, data) 

        return Response(serializer.data, status=201)

    def clean_decimal_fields(self,data, fields):
        """Convert empty strings to None for decimal fields."""
        for field in fields:
            if field in data and data[field] == "":
                data[field] = None
        return data

    def perform_create(self, serializer, data):
        purchase = serializer.save()

        for field, model in [
            ("transaction_details", TransactionDetail),
            ("purchase_details", PurchaseDetail),
        ]:
            related_data = data.get(field, [])
            for item in related_data:
                decimal_fields = ["purchase_price", "sale_price", "commission", "total_amount", "additional_cost_amount"]
                item = self.clean_decimal_fields(item, decimal_fields)

                if field == "purchase_details":
                    product_id = item.pop("product", None)
                    if product_id is not None:
                        item["product"] = get_object_or_404(Product, pk=product_id)

                model.objects.create(purchase=purchase, **item)


class PurchaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()  # Copy request data to modify safely

        # Convert JSON strings to Python objects if needed
        for field in ["transaction_details", "purchase_details"]:
            if isinstance(data.get(field), str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response({f"error": f"Invalid JSON format for {field}"}, status=400)

        # Clean top-level decimal fields
        decimal_fields = ["purchase_price", "sale_price", "commission", "total_amount", "additional_cost_amount"]
        for field in decimal_fields:
            if field in data and data[field] == "":
                data[field] = None

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, data)  # pass the cleaned data to perform_update

        return Response(serializer.data)

    def clean_decimal_fields(self, data, fields):
        """Convert empty strings to None for decimal fields."""
        for field in fields:
            if field in data and data[field] == "":
                data[field] = None
        return data

    def perform_update(self, serializer, data):
        # Update the main purchase instance
        purchase = serializer.save()

        # Process nested details if provided in the update payload
        for field, model in [
            ("transaction_details", TransactionDetail),
            ("purchase_details", PurchaseDetail),
        ]:
            if field in data:
                # Delete existing related objects for a fresh update
                model.objects.filter(purchase=purchase).delete()

                related_data = data.get(field, [])
                for item in related_data:
                    # Clean any empty string values in the decimal fields
                    decimal_fields = ["purchase_price", "sale_price", "commission", "total_amount", "additional_cost_amount"]
                    item = self.clean_decimal_fields(item, decimal_fields)

                    # For purchase_details, handle the foreign key for Product
                    if field == "purchase_details":
                        product_id = item.pop("product", None)
                        if product_id is not None:
                            item["product"] = get_object_or_404(Product, pk=product_id)

                    model.objects.create(purchase=purchase, **item)

    
    
    
class SellListCreateView(generics.ListCreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
   

class SellRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    

    
    
class PaymentRecieveListCreateView(generics.ListCreateAPIView):
    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class PaymentRecieveRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
