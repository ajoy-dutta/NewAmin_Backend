from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import*
from .serializers import*
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from rest_framework.parsers import MultiPartParser, FormParser



class MohajonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if isinstance(data.get("banking_details"), str):
            try:
                data["banking_details"] = json.loads(data["banking_details"])
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format for banking_details"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, data)

        return Response(serializer.data, status=201)

    def perform_create(self, serializer, data): 
        instance = serializer.save()  

        for field, model in [
          ("banking_details", BankInfo),
           ]:
          related_data = data.get(field, [])
          for item in related_data:
            model.objects.create(mohajon=instance, **item)



class MohajonDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        if isinstance(data.get("banking_details"), str):
            try:
                data["banking_details"] = json.loads(data["banking_details"])
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format for banking_details"}, status=400)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, data)

        return Response(serializer.data)

    def perform_update(self, serializer, data):
        instance = serializer.save()

        for field, model in [
           ("banking_details", BankInfo),
        ]:
           model.objects.filter(user=instance).delete()
           related_data = data.get(field, [])
           for item in related_data:
              model.objects.create(user=instance, **item)


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer




   
