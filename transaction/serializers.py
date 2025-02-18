from rest_framework import serializers
from .models import *

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = [
            "transaction_type",
            "additional_cost_description",
            "additional_cost_amount",
        ]

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = [
            "product",
            "warehouse",
            "lot_number",
            "bag_quantity",
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
        extra_kwargs = {'sell': {'required': False}}
        
        
class CostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostInfo
        fields = '__all__'
        extra_kwargs = {'sell': {'required': False}}
        
        
class IncomeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeInfo
        fields = '__all__'
        extra_kwargs = {'sell': {'required': False}}
        
        
class SellSerializer(serializers.ModelSerializer):
    Product_sell_info = ProductSellInfoSerializer(many = True, required = False)
    Cost_info = CostInfoSerializer(many = True, required = False)
    Income_info = IncomeInfoSerializer(many = True, required = False)
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)
    
    
    class Meta:
        model = Sell
        fields = ['id', 'date', 'receipt_no','buyer','buyer_name','Product_sell_info', 'Cost_info', 'Income_info'] 
        
    def create(self, validated_data):
        product_sell_data = validated_data.pop('Product_sell_info', [])
        cost_info_data = validated_data.pop('Cost_info', [])
        income_info_data = validated_data.pop('Income_info', [])

        sell = Sell.objects.create(**validated_data)

        for product in product_sell_data:
            ProductSellInfo.objects.create(sell=sell, **product)

        for cost in cost_info_data:
            CostInfo.objects.create(sell=sell, **cost)

        for income in income_info_data:
            IncomeInfo.objects.create(sell=sell, **income)

        return sell
    
    def update(self, instance, validate_data):
        
        # Update Employee fields
        for attr, value in validate_data.items():
            setattr(instance, attr, value)
        instance.save()
            
        return instance