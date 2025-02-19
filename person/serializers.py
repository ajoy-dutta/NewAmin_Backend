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
        

class PaymentSerializer(serializers.ModelSerializer):
    mohajon_name = serializers.CharField(source='mohajon.name')  # To get Mohajon's name

    class Meta:
        model = Payment
        fields = ['id', 'mohajon', 'voucher', 'amount', 'date', 'mohajon_name']

    def create(self, validated_data):
        """ Override create method to update the Mohajon total_payment """
        payment = super().create(validated_data)
        # The save method in the Payment model already updates the total_payment
        return payment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'