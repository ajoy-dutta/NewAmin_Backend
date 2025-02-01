from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Mohajon, BankInfo
from .serializers import MohajonSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView


# ListCreate API view for Mohajon model (GET and POST)
class MohajonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer


# DestroyUpdate API view for Mohajon model (DELETE and PUT)
class MohajonDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mohajon.objects.all()
    serializer_class = MohajonSerializer



   
