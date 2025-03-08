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
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


# Login View
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


# Division Views
class DivisionListCreateAPIView(ListCreateAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [IsAuthenticated]


class DivisionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [IsAuthenticated]


# District Views
class DistrictListCreateAPIView(ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]


class DistrictRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]


# Thana Views
class ThanaListCreateAPIView(ListCreateAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
    permission_classes = [IsAuthenticated]


class ThanaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
    permission_classes = [IsAuthenticated]


# Area Views
class AreaListCreateAPIView(ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]


class AreaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]


# Route Views
class RouteListCreateAPIView(ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


class RouteRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]


# Godown Views
class GodownListCreateAPIView(ListCreateAPIView):
    queryset = GodownList.objects.all()
    serializer_class = GodownListSerializer
    permission_classes = [IsAuthenticated]


class GodownListRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GodownList.objects.all()
    serializer_class = GodownListSerializer
    permission_classes = [IsAuthenticated]


# Shop Bank Info Views
class ShopBankInfoListCreateView(generics.ListCreateAPIView):
    queryset = ShopBankInfo.objects.all()
    serializer_class = ShopBankInfoSerializer
    permission_classes = [IsAuthenticated]


class ShopBankInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopBankInfo.objects.all()
    serializer_class = ShopBankInfoSerializer
    permission_classes = [IsAuthenticated]


# Bank Method Views
class BankMethodListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BankMethod.objects.all()
    serializer_class = BankMethodSerializer
   


class BankMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BankMethod.objects.all()
    serializer_class = BankMethodSerializer
    


# Cost Method Views
class CostMethodListCreateView(generics.ListCreateAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostMethodSerializer
    permission_classes = [IsAuthenticated]


class CostMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cost.objects.all()
    serializer_class = CostMethodSerializer
    permission_classes = [IsAuthenticated]


# Employee Views
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all().prefetch_related('education', 'experiences', 'banking_details')
    serializer_class = EmployeeSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
