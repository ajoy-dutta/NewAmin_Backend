from rest_framework import serializers
from .models import Division, District, Thana, Route, Area

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class RouteSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'areas']


class ThanaSerializer(serializers.ModelSerializer):
    routes = RouteSerializer(many=True)

    class Meta:
        model = Thana
        fields = ['id', 'name', 'routes']


class DistrictSerializer(serializers.ModelSerializer):
    thanas = ThanaSerializer(many=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'thanas']


class DivisionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)

    class Meta:
        model = Division
        fields = ['id', 'name', 'districts']
