from rest_framework import serializers
from .models import *

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = [
            "transaction_type",
            "payment_method",
            "invoice_number",
            "driver_name",
            "driver_mobile",
            "truck_number",
            "bank_name",
            "account_number",
            "cheque_number",
            "banking_mobile_number",
            "banking_transaction_id",
            "additional_cost_description",
            "additional_cost_amount",
            "is_paid",
        ]

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = [
            "product",
            "product_category",
            "warehouse",
            "lot_number",
            "bag_quantity",
            "sheet_quantity",
            "weight",
            "purchase_price",
            "sale_price",
            "commission",
            "total_amount",
        ]

class PurchaseSerializer(serializers.ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True, required=False) 
    purchase_details = PurchaseDetailSerializer(many=True, required=False)  

    class Meta:
        model = Purchase
        fields = '__all__'
    
    def create(self, validated_data):
        transaction_details_data = validated_data.pop('transaction_details')
        purchase_details_data = validated_data.pop('purchase_details')
        
        purchase = Purchase.objects.create(**validated_data)
        
        for transaction_data in transaction_details_data:
            TransactionDetail.objects.create(purchase=purchase, **transaction_data)
        
        for purchase_data in purchase_details_data:
            PurchaseDetail.objects.create(purchase=purchase, **purchase_data)
        
        return purchase
