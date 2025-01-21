from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                return Response({
                'access': access_token,
                'refresh': str(refresh),
                })
                
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            
        
        


# List and Create View for Divisions
class DivisionListCreateAPIView(ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


# Retrieve, Update, and Delete View for Division
class DivisionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


# List and Create View for Districts
class DistrictListCreateAPIView(ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
  


class DistrictRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
 
 
 
# Thana CRUD Views
class ThanaListCreateAPIView(ListCreateAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer

   


class ThanaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
   



class AreaListCreateAPIView(ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    
    
class AreaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    
    
class RouteListCreateAPIView(ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

  

class RouteRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    
