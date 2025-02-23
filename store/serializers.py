from rest_framework import serializers
from .models import *
import json

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'parent']


class RouteSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'areas', 'parent']


class ThanaSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Thana
        fields = ['id', 'name', 'routes', 'parent']


class DistrictSerializer(serializers.ModelSerializer):
    thanas = ThanaSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'thanas','parent']


class DivisionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Division
        fields = ['id', 'name', 'districts']


class GodownListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GodownList
        fields = '__all__' 
        
        
class ShopBankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopBankInfo
        fields = ['id', 'shop_name', 'bank_name', 'bank_address']
        
        
class BankMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankMethod
        fields = ['id', 'payment_method']
     
        
class CostMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['id', 'name']
        
        
#Employee Info
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['exam_name', 'institute_name', 'passing_year', 'gpa_grade', 'board_or_university', 'group_or_department']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['company_name', 'position', 'address', 'working_time']


class BankingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingDetails
        fields = ['payment_method', 'account_holder_name', 'account_number', 'bank_name', 'branch_name', 'routing_number']


class EmployeeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    banking_details = BankingDetailsSerializer(many=True, required=False)
    

    class Meta:
        model = Employee
        fields = '__all__'
        
        
    def create(self, validated_data):
        
        print(validated_data)

        employee = Employee.objects.create(**validated_data)
        return employee

    def update(self, instance, validated_data):
       
        # Update Employee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)  # Allow optional image

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'code']
        

