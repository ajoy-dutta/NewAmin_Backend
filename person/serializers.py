from rest_framework import serializers
from .models import*
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import password_validation
import json

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'profile_picture', 'email', 'password', 'confirm_password', 'phone')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password doesn't match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        User = get_user_model()
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            phone=validated_data.get('phone')  # Assign phone field
        )
        if 'profile_picture' in validated_data:
            user.profile_picture = validated_data['profile_picture']
        user.is_approved = False
        user.save()
        return user


class StaffApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_approved", "phone", "profile_picture"]
        # read_only_fields = ["id", "username", "email", "role"]  # Prevent modification of certain fields

    def update(self, instance, validated_data):
        """Ensure 'is_approved' is updated properly"""
        is_approved = validated_data.get("is_approved", instance.is_approved)

        if isinstance(is_approved, str):  # Handle "true"/"false" as string input
            is_approved = is_approved.lower() == "true"

        instance.is_approved = is_approved
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Check if the user is approved
        if not user.is_approved:
            raise AuthenticationFailed("Your account has not been approved yet.")

        return data
        
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context['request'].user  # Get the logged-in user
        print(f"Stored password hash: {user.password}")  # Log the stored password hash

        print(f"User: {user.username}, Current Password: {data['current_password']}")
        if isinstance(data, str):
                data = json.loads(data)  
        # Ensure the user is authenticated before checking password
        if not user.is_authenticated:
            raise serializers.ValidationError({"detail": "Authentication is required to change the password."})

        # Check if current password is correct
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        # Ensure the new password is not the same as the current password
        if data['current_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the current password."})

        # Validate the new password using Django's built-in validators
        try:
            password_validation.validate_password(data['new_password'], user=user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return data

    def save(self):
        user = self.context['request'].user  # Get the logged-in user
        user.set_password(self.validated_data['new_password'])  # Set the new password
        user.save()  # Save the user with the new password

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_approved', 'profile_picture','phone']
        
class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = ['bank_name', 'account_holder_name', 'account_number', 'branch_name', 'mobile_number']

# Mohajon serializer
class MohajonSerializer(serializers.ModelSerializer):
    banking_details = BankInfoSerializer(many=True, required=False)

    class Meta:
        model = Mohajon
        fields = '__all__'

    def create(self, validated_data):
        mohajon = Mohajon.objects.create(**validated_data)
        return mohajon


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
        



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'