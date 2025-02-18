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
        # ✅ Extract related fields
        related_fields = {
            "Product_sell_info": (ProductSellInfo, validated_data.pop("Product_sell_info", [])),
            "Cost_info": (CostInfo, validated_data.pop("Cost_info", [])),
            "Income_info": (IncomeInfo, validated_data.pop("Income_info", [])),
        }

        # ✅ Update the main Sell instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # ✅ Process related fields efficiently
        for field, (model, new_records) in related_fields.items():
            existing_records = {obj.id: obj for obj in getattr(instance, field).all()}  # Fetch existing records

            new_objects = []
            updated_objects = []
            seen_ids = set()

            for item in new_records:
                item_id = item.pop("id", None)  # Extract ID (if exists) and remove from dict
                item.pop("sell", None)  # ✅ Prevent error by removing 'sell' from data

                if item_id and item_id in existing_records:
                    # ✅ Update existing records
                    obj = existing_records[item_id]
                    for key, val in item.items():
                        setattr(obj, key, val)
                    updated_objects.append(obj)
                    seen_ids.add(item_id)
                else:
                    # ✅ Create new records
                    new_objects.append(model(sell=instance, **item))

            # ✅ Perform bulk update & create
            if updated_objects:
                model.objects.bulk_update(updated_objects, list(new_records[0].keys()) if new_records else [])

            if new_objects:
                model.objects.bulk_create(new_objects)

            # ✅ Delete removed records
            model.objects.filter(sell=instance).exclude(id__in=seen_ids).delete()

        return instance
