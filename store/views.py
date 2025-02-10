from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser


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
    

class GodownListCreateAPIView(ListCreateAPIView):
    queryset = GodownList.objects.all()
    serializer_class = GodownListSerializer 
    
class GodownListRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GodownList.objects.all()
    serializer_class = GodownListSerializer
    
    
class ShopBankInfoListCreateView(generics.ListCreateAPIView):
    queryset = ShopBankInfo.objects.all()
    serializer_class = ShopBankInfoSerializer


class ShopBankInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopBankInfo.objects.all()
    serializer_class = ShopBankInfoSerializer
    
class BankMethodListCreateView(generics.ListCreateAPIView):
    queryset = BankMethod.objects.all()
    serializer_class = BankMethodSerializer


class BankMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankMethod.objects.all()
    serializer_class = BankMethodSerializer
    
class CostMethodListCreateView(generics.ListCreateAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostMethodSerializer


class CostMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostMethodSerializer
    
    
# Employee Personal Info     
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all().prefetch_related('education', 'experiences', 'banking_details')
    serializer_class = EmployeeSerializer
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy() 
        
        banking_details = data.get("banking_details")
        if isinstance(banking_details, str):
            try:
                data["banking_details"] = json.loads(banking_details)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format"}, status=400)
            
        education = data.get("education")
        if isinstance(education, str):
            try:
                data["education"] = json.loads(education)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format"}, status=400)
            
        experiences = data.get("experiences")
        if isinstance(experiences, str):
            try:
                data["experiences"] = json.loads(experiences)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON format"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, data) 

        return Response(serializer.data, status=201)

    def perform_create(self, serializer, data):
        
        employee = serializer.save() 

        banking_details_data = data.get('banking_details', [])
        for bank_data in banking_details_data:
            BankingDetails.objects.create(user=employee, **bank_data)
            
        education_data = data.get('education', [])
        for education in education_data:
            Education.objects.create(user=employee, **education)
            
        experiences_data = data.get('experiences', [])
        for experience in experiences_data:
            Experience.objects.create(user=employee, **experience)



class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    
# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Product Type Views
class ProductTypeListCreateView(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    
    
