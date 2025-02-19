from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from .models import*
from person.models import Mohajon,Customer
from store.models import Product, GodownList, ShopBankInfo, BankMethod
from decimal import Decimal 


# Create your models here.

class Purchase(models.Model):
    date = models.DateField(default=now)
    receipt_number = models.CharField(max_length=100, unique=True, blank=True,null = True)
    business_type = models.CharField(max_length=255, choices=[('মহাজন', 'মহাজন'), ('বেপারী/চাষী', 'বেপারী/চাষী')]) 
    buyer_name = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="purchases")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Receipt {self.receipt_number} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last_purchase = Purchase.objects.order_by('id').last()

            if last_purchase:
                new_user_id = last_purchase.id + 1
            else:
                new_user_id = 1

            self.receipt_number = f"PP{new_user_id:07}"

        super(Purchase, self).save(*args, **kwargs)

    def update_total_amount(self):
        self.total_amount = self.purchase_details.aggregate(total=Sum('total_amount'))['total'] or 0
        self.save()

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_details")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    warehouse = models.CharField(max_length=255, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)

    bag_quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure both purchase_price and weight are not None
        if self.purchase_price is None or self.weight is None:
            raise ValueError("purchase_price and weight must be provided")

        # Convert to Decimal if they are strings
        if isinstance(self.purchase_price, str):
            self.purchase_price = Decimal(self.purchase_price)
        if isinstance(self.weight, str):
            self.weight = Decimal(self.weight)

        # Perform multiplication
        self.total_amount = self.purchase_price * self.weight

        super().save(*args, **kwargs)
        self.purchase.update_total_amount()


    def __str__(self):
        return f"{self.product.name} ({self.weight} kg)"


class TransactionDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="transaction_details")  # Add this line
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    additional_cost_description = models.TextField(blank=True, null=True)
    additional_cost_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_type} - {self.additional_cost_amount}"  # Fixed issue



## sell method
class Sell(models.Model):
    date = models.DateField()
    receipt_no = models.CharField(max_length=50, unique=True, blank = True)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sell")
    
    
    def save(self, *args, **kwargs):
        if not self.receipt_no:
            last_code = Sell.objects.filter(receipt_no__startswith="PS").order_by('-receipt_no').first()
            if last_code:
                try:
                    last_number = int(last_code.receipt_no[2:]) 
                    self.receipt_no = f"PS{last_number + 1:07}" 
                except ValueError:
                    raise ValueError(f"Invalid code format found: {last_code.receipt_no}")
            else:
                self.receipt_no = "PS0000001"  

        super().save(*args, **kwargs)
            
        
    def __str__(self):
        return f"Sell {self.receipt_no} - {self.buyer_name}"



class ProductSellInfo(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="Product_sell_info")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null= True, related_name="Product" )
    bereft_name = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="bereft_name")
    godown_name = models.ForeignKey(GodownList, on_delete=models.CASCADE, related_name="GodownList")
    lot_number = models.CharField(max_length=50)
    bag_quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_bag_quantity = models.IntegerField(default=0)
    sale_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sale_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    
    def __str__(self):
        return f"{self.product_name} ({self.sell.receipt_no})"



class CostInfo(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="Cost_info")
    cost_type = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    costDescription = models.TextField(max_length=500, null= True)
    
    def __str__(self):
        return f"Cost {self.sell.receipt_no} - {self.transaction_category}"


class IncomeInfo(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="Income_info")
    payment_method = models.CharField(max_length=255, blank=True, null=True)  
    bank_name = models.CharField(max_length=255, blank=True, null=True)  
    account_number = models.CharField(max_length=50, blank=True, null=True)
    check_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Income {self.sell.receipt_no} - {self.amount}"

class Payment(models.Model):
    mohajon = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name='payments')
    voucher = models.CharField(max_length=50, blank=True,null=True)  # Voucher number
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)  # Timestamp
    code = models.CharField(max_length=50, unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        """ Update total_payment in Mohajon when a new payment is added """
        super(Payment, self).save(*args, **kwargs)
        self.mohajon.total_payment += self.amount
        self.mohajon.save(update_fields=['total_payment'])  # Update only total_payment
        if not self.code:
            last_payment = Payment.objects.order_by('id').last()

            if last_payment:
                new_user_id = last_payment.id + 1
            else:
                new_user_id = 1

            self.code = f"P{new_user_id:07}"

        super(Payment, self).save(*args, **kwargs)


class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    name = models.CharField(max_length=255, blank=True,null=True) 
    voucher = models.CharField(max_length=50, blank=True,null=True)  # Voucher number
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)  # Timestamp
    code = models.CharField(max_length=50, unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_payment = CustomerPayment.objects.order_by('id').last()

            if last_payment:
                new_user_id = last_payment.id + 1
            else:
                new_user_id = 1

            self.code = f"P{new_user_id:07}"

        super(CustomerPayment, self).save(*args, **kwargs)