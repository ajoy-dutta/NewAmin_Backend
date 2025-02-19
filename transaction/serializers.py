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
    
    
    def update(self, instance, validated_data):
        related_fields = {
            "Product_sell_info": ProductSellInfo,
            "Cost_info": CostInfo,
            "Income_info": IncomeInfo,
        }

        related_data = {field: validated_data.pop(field, None) for field in related_fields}

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for field, model in related_fields.items():
            if related_data[field] is not None:  # Only update if data is provided
                getattr(instance, field).all().delete()  # Delete existing records

                new_objects = [model(sell=instance, **{k: v for k, v in item.items() if k != "sell"}) for item in related_data[field]]

                model.objects.bulk_create(new_objects)  # Bulk create new records

        return instance

class PaymentSerializer(serializers.ModelSerializer):
    mohajon_name = serializers.CharField(source='mohajon.name')  # To get Mohajon's name

    class Meta:
        model = Payment
        fields = ['id', 'mohajon','code', 'voucher', 'amount', 'date', 'mohajon_name','payment_description']

    def create(self, validated_data):
        """ Override create method to update the Mohajon total_payment """
        payment = super().create(validated_data)
        # The save method in the Payment model already updates the total_payment
        return payment
    
    
    
class PaymentRecieveSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)

    class Meta:
        model = PaymentRecieve
        fields = '__all__'

class EmployeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePayment
        fields = '__all__'

class OtherPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPayment
        fields = '__all__'

