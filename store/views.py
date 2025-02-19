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
    
    
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all().prefetch_related('education', 'experiences', 'banking_details')
    serializer_class = EmployeeSerializer
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy() 
        
        for field in ["banking_details", "education", "experiences"]:
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
        
        employee = serializer.save() 
        
        for field, model in [
            ("banking_details", BankingDetails),
            ("education", Education),
            ("experiences", Experience),
        ]:
            related_data = data.get(field, [])
            for item in related_data:
                model.objects.create(user=employee, **item)



class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        for field in ["banking_details", "education", "experiences"]:
            if isinstance(data.get(field), str):
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response({f"error": f"Invalid JSON format for {field}"}, status=400)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, data)

        return Response(serializer.data)

    def perform_update(self, serializer, data):
        employee = serializer.save()

        for field, model in [
            ("banking_details", BankingDetails),
            ("education", Education),
            ("experiences", Experience),
        ]:
            model.objects.filter(user=employee).delete()
            related_data = data.get(field, [])
            for item in related_data:
                model.objects.create(user=employee, **item)
    
    
# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    
    
