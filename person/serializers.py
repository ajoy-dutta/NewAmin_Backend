from rest_framework import serializers
from .models import Mohajon, BankInfo
from store.serializers import ShopBankInfoSerializer  # Assuming you have this serializer

# BankInfo serializer to handle multiple bank accounts
class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = ['bank_name', 'account_holder_name', 'account_number', 'branch_name', 'mobile_number']

# Mohajon serializer
class MohajonSerializer(serializers.ModelSerializer):
    # Nested BankInfo serializer to allow multiple bank details
    banking_details = BankInfoSerializer(many=True, required=False)

    class Meta:
        model = Mohajon
        fields = '__all__'

    # Override the create method to handle nested BankInfo objects
    def create(self, validated_data):
        banking_details_data = validated_data.pop('banking_details', None)  # Get nested banking details
        mohajon_instance = Mohajon.objects.create(**validated_data)  # Create Mohajon instance

        if banking_details_data:
            bank_info_instances = [
                BankInfo(user=mohajon_instance, **bank_data)
                for bank_data in banking_details_data
            ]
            BankInfo.objects.bulk_create(bank_info_instances)  # Bulk create bank records for better performance

        return mohajon_instance

    # Override update method to handle nested BankInfo objects (if updating Mohajon and bank details)
    def update(self, instance, validated_data):
        banking_details_data = validated_data.pop('banking_details', None)
        
        # Update Mohajon instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        if banking_details_data is not None:
            # Clear existing banking details and add new ones
            instance.banking_details.all().delete()
            bank_info_instances = [
                BankInfo(user=instance, **bank_data)
                for bank_data in banking_details_data
            ]
            BankInfo.objects.bulk_create(bank_info_instances)  # Bulk create bank records for better performance

        return instance
