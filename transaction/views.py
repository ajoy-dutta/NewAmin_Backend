from django.shortcuts import render
from rest_framework import generics
from .models import*
from .serializers import*
import json
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser



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

    def perform_create(self, serializer, data):
        
        purchase = serializer.save() 
        
        for field, model in [
            ("transaction_details", TransactionDetail),
            ("purchase_details", PurchaseDetail),
        ]:
            related_data = data.get(field, [])
            for item in related_data:
                model.objects.create(user=purchase, **item)


class PurchaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    
    
    
class SellListCreateView(generics.ListCreateAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer

class SellRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
