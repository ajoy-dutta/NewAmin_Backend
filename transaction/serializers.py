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

        purchase = Purchase.objects.create(**validated_data)
        return purchase

    def update(self, instance, validated_data):
       
        # Update Employee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class ProductSellInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSellInfo
        fields = '__all__'
        
        
class CostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostInfo
        fields = '__all__'
        
        
class IncomeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeInfo
        fields = '__all__'
        
        
class SellSerializer(serializers.ModelSerializer):
    Product_sell_info = ProductSellInfoSerializer(many = True, required = False)
    Cost_info = CostInfoSerializer(many = True, required = False)
    Income_info = IncomeInfoSerializer(many = True, required = False)
    
    
    class Meta:
        model = Sell
        fields = '__all__'
        
    def create(self, validate_data):
        print(validate_data)
        
        sell = Sell.objects.create( **validate_data )
        return sell
    
    def update(self, instance, validate_data):
        
        # Update Employee fields
        for attr, value in validate_data.items():
            setattr(instance, attr, value)
        instance.save()
            
        return instance