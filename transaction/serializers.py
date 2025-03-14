from rest_framework import serializers
from .models import *
from store.models import *

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
    total_sell_bag = serializers.IntegerField( read_only=True)
    total_sell_weight = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

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
            "total_sell_bag",
            "total_sell_weight",
            "purchase_price",
            "sale_price",
            "commission",
            "total_amount",
            'exist',
        ]

class PurchaseSerializer(serializers.ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True, required=False) 
    purchase_details = PurchaseDetailSerializer(many=True, required=False)  
    bereft_name = serializers.CharField(source='buyer_name.name', read_only=True)
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
    godown = serializers.CharField(source="godown_name.godown_name", read_only = True)  
    
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
        total_price = 0 
        total_income = 0
        

        sell = Sell.objects.create(**validated_data)

        # Create ProductSellInfo records and adjust Purchase quantities
        for product in product_sell_data:
            product_sell_info = ProductSellInfo.objects.create(sell=sell, **product)
            total_price += product_sell_info.amount

            lot_number = product_sell_info.lot_number
            godown = product_sell_info.godown_name
            try:
                purchaseDetail = PurchaseDetail.objects.get(lot_number=lot_number , warehouse=godown.godown_name)
                purchaseDetail.bag_quantity -= product_sell_info.sale_bag_quantity
                purchaseDetail.weight -= product_sell_info.sale_weight
                purchaseDetail.total_sell_bag += product_sell_info.sale_bag_quantity
                purchaseDetail.total_sell_weight += product_sell_info.sale_weight
                if purchaseDetail.bag_quantity < 0 or purchaseDetail.weight < 0:
                    raise ValueError("Not enough inventory to complete the sale.")
                purchaseDetail.save()
            except Purchase.DoesNotExist:
                raise ValueError(f"No purchase record found for lot number {lot_number}")
            
        # Update customer's previous_account field
        customer = sell.buyer
        if customer.previous_account is None:
            customer.previous_account = 0  # Ensure it's not None
        customer.previous_account += total_price
        customer.save()


        for cost in cost_info_data:
            CostInfo.objects.create(sell=sell, **cost)

        for income in income_info_data:
            income_info = IncomeInfo.objects.create(sell=sell, **income)
            total_income += income_info.amount
            
        customer.previous_account -= total_income
        customer.save()

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
    remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRecieve
        fields = '__all__'

    def get_remaining_balance(self, obj):
        customer = Customer.objects.filter(id=obj.buyer_id).first()
        previous_account = customer.previous_account if customer else 0
        return previous_account - obj.amount

    def create(self, validated_data):
        instance = super().create(validated_data)
        
        customer = Customer.objects.filter(id=instance.buyer_id).first()
        if customer:
            customer.previous_account -= instance.amount
            customer.save()

        return instance
    
    

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
        
    
    def validate_lot_number(self, value):
        lot_number = value
        print(lot_number)
        purchase_details = PurchaseDetail.objects.filter(lot_number=lot_number)

        purchase_details.update(exist=False)
        return value 
    
    def create(self, validated_data):
        lot_number = validated_data.get('lot_number')
        
        purchase_details = PurchaseDetail.objects.filter(lot_number=lot_number)
        purchase_details.update(exist=False)
        
        return super().create(validated_data)
    
    def update(self, instance, validate_data):
        lot_number = validate_data.get('lot_number')
        
        purchase_details = PurchaseDetail.objects.filter(lot_number = lot_number)
        purchase_details.update(exist = False)
        
        return super().update(instance, validate_data)
    

class BankIncomeCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankIncomeCost
        fields = '__all__'
