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
    bag_quantity = serializers.IntegerField( read_only=True)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseDetail
        fields = [
            "product",
            "warehouse",
            "lot_number",
            "purchased_bag_quantity",
            "purchased_weight",
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
    
    product_name = serializers.CharField(source="product.name", read_only=True)  
    # godown_name = serializers.CharField(source="godown_name.godown_name", read_only=True) 
    
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

        # Create ProductSellInfo records and adjust Purchase quantities
        for product in product_sell_data:
            product_sell_info = ProductSellInfo.objects.create(sell=sell, **product)

            lot_number = product_sell_info.lot_number
            try:
                purchaseDetail = PurchaseDetail.objects.get(lot_number=lot_number)
                purchaseDetail.bag_quantity -= product_sell_info.sale_bag_quantity
                purchaseDetail.weight -= product_sell_info.sale_weight
                if purchaseDetail.bag_quantity < 0 or purchaseDetail.weight < 0:
                    raise ValueError("Not enough inventory to complete the sale.")
                purchaseDetail.save()
            except Purchase.DoesNotExist:
                raise ValueError(f"No purchase record found for lot number {lot_number}")


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


    
    
class PaymentRecieveSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)

    class Meta:
        model = PaymentRecieve
        fields = '__all__'

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = '__all__'
        extra_kwargs = {
                    'payment_header': {'read_only': True}, 
                }


class PaymentSerializer(serializers.ModelSerializer):
    details = PaymentDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = '__all__'


    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        payment = Payment.objects.create(**validated_data)
        for detail_data in details_data:
            PaymentDetail.objects.create(payment_header=payment, **detail_data)
        return payment

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        instance.date = validated_data.get('date', instance.date)
        instance.voucher = validated_data.get('voucher', instance.voucher)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                PaymentDetail.objects.create(payment_header=instance, **detail_data)
        return instance
    
    
class InvoiceSerializer(serializers.ModelSerializer):
    bereft_name = serializers.CharField(source='bereft.name', read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'

class BankIncomeCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankIncomeCost
        fields = '__all__'
