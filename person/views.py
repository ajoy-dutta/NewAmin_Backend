from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import*
from .serializers import*
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth import get_user_model

User=get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class UserRegistrationView(ListCreateAPIView):
    queryset = User.objects.all()  # Replace `User` with your model name
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Log received data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )



class StaffListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffApproveSerializer

class StaffApproveView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffApproveSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # Get the specific User instance
        user.is_approved = request.data.get('is_approved', user.is_approved)  # Update is_approved field
        user.save()  # Save the updated user instance
        return Response({"message": f"User {user.username} approval status updated successfully."}, status=status.HTTP_200_OK)
    def delete(self,request,*args,**kwargs):
        try:
            user=self.get_object()
            user.delete()
            return Response({"message": f"User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error":"User doesn't exist"},status=status.HTTP_404_NOT_FOUND )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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

        for field, model in [("banking_details", BankInfo)]:
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
           model.objects.filter(mohajon=instance).delete()
           related_data = data.get(field, [])
           for item in related_data:
              model.objects.create(mohajon=instance, **item)



class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer




   
