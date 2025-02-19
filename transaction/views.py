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
    
    
    
class SellListCreateView(generics.ListCreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
   

class SellRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    
class PaymentListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        """ List all payments """
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Create a new payment """
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()  # This will automatically update the Mohajon total_payment
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PaymentRecieveListCreateView(generics.ListCreateAPIView):
    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class PaymentRecieveRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentRecieve.objects.all()
    serializer_class = PaymentRecieveSerializer

class EmployeePaymentListCreateView(generics.ListCreateAPIView):
    queryset = EmployeePayment.objects.all()
    serializer_class = EmployeePaymentSerializer

class OtherPaymentListCreateView(generics.ListCreateAPIView):
    queryset = OtherPayment.objects.all()
    serializer_class = OtherPaymentSerializer
