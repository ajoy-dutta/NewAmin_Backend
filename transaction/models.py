from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from .models import*
from person.models import Mohajon,Customer
from store.models import Product, GodownList, ShopBankInfo, BankMethod,Employee
from decimal import Decimal 
from datetime import datetime

# Create your models here

class Purchase(models.Model):
    date = models.DateField(default=now)
    receipt_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    business_type = models.CharField(max_length=255, choices=[('মহাজন', 'মহাজন'), ('বেপারী/চাষী', 'বেপারী/চাষী')]) 
    buyer_name = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="purchases")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    advance_payment = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null = True)
    total_transaction_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def update_total_amount(self):
        """ Updates total_amount by summing all related PurchaseDetails """
        total = self.purchase_details.aggregate(total=Sum('total_amount'))['total'] or Decimal(0)
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def update_total_transaction_amount(self):
        """ Updates total_transaction_amount by summing all related TransactionDetails """
        total_transactions = self.transaction_details.aggregate(total=Sum('additional_cost_amount'))['total'] or Decimal(0)
        self.total_transaction_amount = total_transactions
        self.save(update_fields=['total_transaction_amount'])

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last_purchase = Purchase.objects.order_by('id').last()
            new_user_id = last_purchase.id + 1 if last_purchase else 1
            self.receipt_number = f"PP{new_user_id:07}"

        super(Purchase, self).save(*args, **kwargs)
        self.buyer_name.update_total_purchases()
        self.buyer_name.update_total_payment() 
        self.buyer_name.update_total_transaction_amount()


    def delete(self, *args, **kwargs):
        """ Ensure total_purchases updates when a Purchase is deleted """
        buyer = self.buyer_name
        print(f"Deleting PaymentDetail for Mohajon: {buyer}")  # Debugging Line

        super().delete(*args, **kwargs)
        buyer.update_total_purchases()
        buyer.update_total_payment() 
        buyer.update_total_transaction_amount()

    def __str__(self):
        return f"Receipt {self.receipt_number} ({self.date})"

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_details")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    warehouse = models.CharField(max_length=255, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
    
    purchased_bag_quantity = models.IntegerField(blank=True, null = True)
    purchased_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null = True)

    bag_quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    total_sell_bag = models.IntegerField(default=0, blank=True, null = True)
    total_sell_weight = models.DecimalField(default=Decimal('0.00'),max_digits=10, decimal_places=2, blank=True, null = True)

    
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    exist = models.BooleanField(default=True, blank= True, null = True)

    def save(self, *args, **kwargs):
        
        if not self.pk:
            if self.purchased_bag_quantity is not None and self.purchased_weight is not None:
                self.bag_quantity = self.purchased_bag_quantity
                self.weight = self.purchased_weight

        if not self.lot_number:
            if self.purchase and self.purchase.date:
                date_obj = self.purchase.date.date() if hasattr(self.purchase.date, 'date') else self.purchase.date
                date_str = date_obj.strftime('%d%m%y')
            else:
                date_str = datetime.today().strftime('%d%m%y')
            
            # Count existing details for this product on the same purchase date
            existing_count = PurchaseDetail.objects.filter(
                purchase__date=self.purchase.date,
                # product=self.product
            ).count()
            
            # The new sequence number starts at 1 for a new date
            new_sequence = existing_count + 1
            
            # Build the lot number as: date_str - bag_quantity - new_sequence
            self.lot_number = f"{date_str}-{self.bag_quantity}-{new_sequence}"

        super().save(*args, **kwargs)

        self.purchase.update_total_amount()

        def delete(self, *args, **kwargs):
            """ Update total_amount in Purchase when a PurchaseDetail is deleted """
            purchase = self.purchase
            super().delete(*args, **kwargs)
            purchase.update_total_amount()

    def __str__(self):
        return f"{self.product.name} ({self.weight} kg)"


class TransactionDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="transaction_details")  # Add this line
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    additional_cost_description = models.TextField(blank=True, null=True)
    additional_cost_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(TransactionDetail, self).save(*args, **kwargs)
        self.purchase.update_total_transaction_amount()  # ✅ Update purchase transaction amount

    def delete(self, *args, **kwargs):
        purchase = self.purchase
        super(TransactionDetail, self).delete(*args, **kwargs)
        purchase.update_total_transaction_amount()  # ✅ Update purchase transaction amount after deletion

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
        return f"Sell {self.receipt_no} - {self.buyer}"



class ProductSellInfo(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="Product_sell_info")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null= True, related_name="Product" )
    bereft_name = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="bereft_name")
    godown_name = models.ForeignKey(GodownList, on_delete=models.CASCADE, related_name="warehouse_name",blank=True, null= True)
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
        return f"{self.product} ({self.sell.receipt_no})"



class CostInfo(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="Cost_info")
    cost_type = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    costDescription = models.TextField(max_length=500, null= True)
    
    def __str__(self):
        return f"Cost {self.sell.receipt_no} - {self.cost_type}"



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
    


   
class PaymentRecieve(models.Model):
    date = models.DateField(auto_now_add=True)  # Auto-generate the date
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)  # Auto-generate
    voucher_number = models.CharField(max_length=50, blank=True, null=True)
    deposit_type= models.CharField(max_length=255, blank=True, null=True)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="buyer", null=True, blank=True)
    paymentDescription = models.TextField(max_length=255,blank=True, null=True )
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_bank = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
   
    def save(self, *args, **kwargs):
        # Auto-generate receipt_number if not provided
        if not self.receipt_number:
            last_transaction = PaymentRecieve.objects.filter(receipt_number__startswith="TR").order_by('-receipt_number').first()
            if last_transaction:
                try:
                    last_number = int(last_transaction.receipt_number[2:])
                    self.receipt_number = f"TR{last_number + 1:07}"
                except ValueError:
                    raise ValueError(f"Invalid receipt format: {last_transaction.receipt_number}")
            else:
                self.receipt_number = "TR0000001"

        super().save(*args, **kwargs)

    def __str__(self):
        buyer_name = self.buyer.name if self.buyer else "No Buyer"
        return f"Transaction {self.receipt_number} - {buyer_name}"
    
    

class Payment(models.Model):
    date = models.DateField()
    voucher = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_payment = Payment.objects.order_by('id').last()  # ✅ Use Payment instead of PaymentHeader
            new_id = last_payment.id + 1 if last_payment else 1
            self.code = f"P{new_id:07}"
        super().save(*args, **kwargs)



class PaymentDetail(models.Model):
    payment_header = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="details")
    
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    
    payment_description = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    cheque_number = models.CharField(max_length=100, blank=True, null=True)
    mobile_banking_number = models.CharField(max_length=15, blank=True, null=True)

    mohajon = models.ForeignKey(Mohajon, on_delete=models.CASCADE, blank=True, null=True, related_name="payment_details")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, related_name="employee_payment_details")
    
    def save(self, *args, **kwargs):
        """ Ensure total_payment updates when a payment is saved """
        super().save(*args, **kwargs)
        if self.mohajon:
            self.mohajon.update_total_payment()

    def delete(self, *args, **kwargs):
        """ Ensure total_payment updates when a payment is deleted """
        mohajon = self.mohajon  # ✅ Store reference before deleting
        print(f"Deleting PaymentDetail for Mohajon: {mohajon}")  # Debugging Line
        super().delete(*args, **kwargs)  # Delete the PaymentDetail object
        if mohajon:
            print("Updating total_payment after deletion...")  # Debugging Line
            mohajon.update_total_payment()


    def __str__(self):
        return f"{self.payment_header.code} - {self.payment_type} - {self.amount}"
    

 
class Invoice(models.Model):
    date = models.DateField()
    product_name = models.CharField(max_length=255)
    bereft = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    godown_name = models.CharField(max_length=255)
    lot_number = models.CharField(max_length=255)
    purchased_bag_quantity = models.IntegerField(default=0, blank= True, null =True)
    purchased_weight = models.DecimalField(max_digits=10, decimal_places=2, blank= True, null =True)
    advance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    van_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vehicle_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    station_expense = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_cost_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_cost_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_no = models.CharField(max_length=255,blank= True, null =True)
    
    
    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last_invoice = Invoice.objects.filter(invoice_no__startswith="SC").order_by('-invoice_no').first()
            if last_invoice:
                try:
                    last_number = int(last_invoice.invoice_no[2:])
                    self.invoice_no = f"SC{last_number + 1:07}"
                except ValueError:
                    raise ValueError(f"Invalid receipt format: {last_invoice.invoice_no}")
            else:
                self.invoice_no = "SC0000001"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for {self.product_name} ({self.date})"


        from django.db import models

class BankIncomeCost(models.Model):
    TRANSACTION_CHOICES = [
        ("জমা", "জমা"),  # Deposit
        ("খরচ", "খরচ")   # Expense
    ]

    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_CHOICES)
    bank_name = models.CharField(max_length=255) 
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=now)
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.bank_name})"

