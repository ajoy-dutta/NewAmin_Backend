from rest_framework import serializers
from .models import*

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