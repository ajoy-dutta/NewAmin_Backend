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
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.permissions import IsAdminUser
from django.db import transaction

# Create your views here.
class PurchaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAuthenticated]

    queryset = Sell.objects.all()
    serializer_class = SellSerializer
   

class SellRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    

    
    
class PaymentRecieveListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class PaymentRecieveRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    

class InvoiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Invoice.objects.all() 
    serializer_class = InvoiceSerializer
    
    
class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all() 
    serializer_class = InvoiceSerializer
    
    
    
class GodownTransferView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            # Extract data from request
            source_godown_id = request.data.get("fromGodown")
            target_godown_id = request.data.get("toGodown")
            product_id = request.data.get("product")
            transfer_bag_quantity = request.data.get("movedBagQuantity")
            transfer_kg_quantity = request.data.get("movedKgQuantity")
            lot_number = request.data.get("lotNumber")

            source_record = PurchaseDetail.objects.get(warehouse=source_godown_id, product_id=product_id, lot_number=lot_number)

            with transaction.atomic():  # Ensures atomicity of transfer
                
                transfer_bag_quantity = Decimal(str(transfer_bag_quantity))
                transfer_kg_quantity = Decimal(str(transfer_kg_quantity))
                
                purchase_obj = source_record.purchase  

                source_record.bag_quantity -= transfer_bag_quantity
                source_record.weight -= transfer_kg_quantity
                source_record.save()

                # Add stock to target godown (create if not exists)
                target_record, created = PurchaseDetail.objects.get_or_create(
                    warehouse=target_godown_id,
                    product_id=product_id,
                    lot_number=lot_number,
                    purchase=purchase_obj, 
                    defaults={
                        "bag_quantity": 0,
                        "weight": 0,
                        "purchase_price": source_record.purchase_price
                    }
                )

                # Increase stock in target godown
                target_record.bag_quantity += transfer_bag_quantity
                target_record.weight += transfer_kg_quantity
                target_record.save()

                return Response({"message": "Product transferred successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankIncomeCostListCreateView(generics.ListCreateAPIView):
    queryset = BankIncomeCost.objects.all().order_by("-date")  # Show newest first
    serializer_class = BankIncomeCostSerializer
# ///new add 
class BankIncomeCostUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankIncomeCost.objects.all()
    serializer_class = BankIncomeCostSerializer
  

