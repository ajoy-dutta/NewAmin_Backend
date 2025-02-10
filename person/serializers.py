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
        banking_details_data = validated_data.pop('banking_details', None)  
        mohajon_instance = Mohajon.objects.create(**validated_data) 

        if banking_details_data:
            bank_info_instances = [
                BankInfo(user=mohajon_instance, **bank_data)
                for bank_data in banking_details_data
            ]
            BankInfo.objects.bulk_create(bank_info_instances)  

        return mohajon_instance

    def update(self, instance, validated_data):
        banking_details_data = validated_data.pop('banking_details', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        if banking_details_data is not None:
            instance.banking_details.all().delete()
            bank_info_instances = [
                BankInfo(user=instance, **bank_data)
                for bank_data in banking_details_data
            ]
            BankInfo.objects.bulk_create(bank_info_instances) 
        return instance

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'