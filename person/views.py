from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import*
from .serializers import*
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class MohajonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer


class MohajonDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer




   
