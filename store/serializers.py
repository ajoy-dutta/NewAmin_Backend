from rest_framework import serializers
from .models import *

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class RouteSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'areas']


class ThanaSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Thana
        fields = ['id', 'name', 'routes']


class DistrictSerializer(serializers.ModelSerializer):
    thanas = ThanaSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'thanas']


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