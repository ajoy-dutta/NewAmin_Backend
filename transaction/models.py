from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from .models import*
from person.models import Mohajon
from store.models import Product


# Create your models here.

class Purchase(models.Model):
    date = models.DateField(default=now)
    receipt_number = models.CharField(max_length=10, unique=True, blank=True)
    business_type = models.CharField(max_length=255, choices=[('মহাজন', 'মহাজন'), ('বেপারী/চাষী', 'বেপারী/চাষী')]) 
    buyer_name = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="purchases")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Receipt {self.receipt_number} ({self.date})"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last_code = Purchase.objects.order_by('receipt_number').last()
            if last_code:
                last_number = int(last_code.receipt_number[2:])
                self.receipt_number = f"PP{last_number + 1:05}"
            else:
                self.receipt_number = "PP00001"

        super().save(*args, **kwargs)

    def update_total_amount(self):
        self.total_amount = self.purchase_details.aggregate(total=Sum('total_amount'))['total'] or 0
        self.save()

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="purchase_details")  # Add this line
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_details")  # ForeignKey to Product
    product_category = models.CharField(max_length=255, blank=True, null=True)
    warehouse = models.CharField(max_length=255, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)

    bag_quantity = models.IntegerField()
    sheet_quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.purchase_price * self.weight 
        super().save(*args, **kwargs)

        self.purchase.update_total_amount()

    def __str__(self):
        return f"{self.product.name} ({self.weight} kg)"


class TransactionDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="transaction_details")  # Add this line
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    
    driver_name = models.CharField(max_length=255, blank=True, null=True)
    driver_mobile = models.CharField(max_length=15, blank=True, null=True)
    truck_number = models.CharField(max_length=50, blank=True, null=True)

    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    banking_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    banking_transaction_id = models.CharField(max_length=100, blank=True, null=True)

    additional_cost_description = models.TextField(blank=True, null=True)
    additional_cost_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_type} - {self.additional_cost_amount} ({'Paid' if self.is_paid else 'Unpaid'})"  # Fixed issue

