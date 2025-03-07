from django.db import models
from .models import*
from store.models import ShopBankInfo  # Import ShopBankInfo from the store app
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=40, default='General', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='image/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
            self.is_approved = True
        elif not self.role:  # If the role is not provided, assign the default 'Assistant Accountant'
            self.role = 'General'
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.username



class Mohajon(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True,blank=True,null=True)  # Ensure this is a CharField, not AutoField
    business_type = models.CharField(max_length=255, choices=[('মহাজন', 'মহাজন'),('বেপারী/চাষী','বেপারী/চাষী')]) 
    father_name = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=[('পুরুষ', 'পুরুষ'), ('নারী', 'নারী'), ('অন্যান্য', 'অন্যান্য')], blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    nid_number = models.CharField(max_length=50, blank=True, null=True)
    market_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    mobile_number_1 = models.CharField(max_length=15, blank=True, null=True)
    mobile_number_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Present Address Information
    present_division = models.CharField(max_length=255, blank=True, null=True)
    present_district = models.CharField(max_length=255, blank=True, null=True)
    present_thana = models.CharField(max_length=255, blank=True, null=True)
    present_route = models.CharField(max_length=255, blank=True, null=True)
    present_area = models.CharField(max_length=255, blank=True, null=True)
    present_village_street = models.CharField(max_length=255, blank=True, null=True)
    present_post_office = models.CharField(max_length=255, blank=True, null=True)
    present_post_code = models.CharField(max_length=100, blank=True, null=True)

    # Permanent Address Information
    permanent_division = models.CharField(max_length=255, blank=True, null=True)
    permanent_district = models.CharField(max_length=255, blank=True, null=True)
    permanent_thana = models.CharField(max_length=255, blank=True, null=True)
    permanent_route = models.CharField(max_length=255, blank=True, null=True)
    permanent_area = models.CharField(max_length=255, blank=True, null=True)
    permanent_village_street = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_office = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_code = models.CharField(max_length=100, blank=True, null=True)

    # Additional Information
    photo = models.ImageField(upload_to='image/', blank=True, null=True)
    shop_photo = models.ImageField(upload_to='image/', blank=True, null=True)
    nid_front_photo = models.ImageField(upload_to='image/', blank=True, null=True)
    nid_back_photo = models.ImageField(upload_to='image/', blank=True, null=True)

    # Previous Records
    previous_account = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    khatian_number = models.CharField(max_length=50, blank=True, null=True)
        
    # Financial Fields
    total_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total payments received
    total_purchases = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Total purchases
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # ✅ New Field

    def update_total_payment(self):
        """ Updates total_payment by summing all related PaymentDetails """
        total_payments = self.payment_details.aggregate(total=Sum('amount'))['total'] or Decimal(0)
        self.total_payment = total_payments
        self.save(update_fields=['total_payment'])
        self.update_due_amount()  # ✅ Update due_amount after updating payments

    def update_total_purchases(self):
        """ Updates total_purchases by summing all related Purchases total_amount """
        total = self.purchases.aggregate(total=Sum('total_amount'))['total'] or Decimal(0)
        self.total_purchases = total
        self.save(update_fields=['total_purchases'])
        self.update_due_amount()  # ✅ Update due_amount after updating purchases

    def update_due_amount(self):
        """ Calculates due_amount = previous_account + total_purchases - total_payment """
        self.due_amount = (self.previous_account or Decimal(0)) + self.total_purchases - self.total_payment
        self.save(update_fields=['due_amount'])
    
        
    def save(self, *args, **kwargs):
        if not self.code:
            last_mohajon = Mohajon.objects.order_by('id').last()

            new_user_id = (last_mohajon.id + 1) if last_mohajon else 1

            
            prefix = "M" if self.business_type == "মহাজন" else "B"
            self.code = f"{prefix}{new_user_id:05}"

        super(Mohajon, self).save(*args, **kwargs)


class BankInfo(models.Model):
    mohajon = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="banking_details")
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True,blank=True)  # Ensure this is a CharField, not AutoField
    business_type = models.CharField(max_length=255, choices=[('Retailer', 'Retailer'),('Whole Saler','Whole Saler')]) 
    father_name = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=[('পুরুষ', 'পুরুষ'), ('নারী', 'নারী'), ('অন্যান্য', 'অন্যান্য')], blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    nid_number = models.CharField(max_length=50, blank=True, null=True)
    market_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    mobile_number_1 = models.CharField(max_length=15, blank=True, null=True)
    mobile_number_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Present Address Information
    present_division = models.CharField(max_length=255, blank=True, null=True)
    present_district = models.CharField(max_length=255, blank=True, null=True)
    present_thana = models.CharField(max_length=255, blank=True, null=True)
    present_route = models.CharField(max_length=255, blank=True, null=True)
    present_area = models.CharField(max_length=255, blank=True, null=True)
    present_village_street = models.CharField(max_length=255, blank=True, null=True)
    present_post_office = models.CharField(max_length=255, blank=True, null=True)
    present_post_code = models.CharField(max_length=100, blank=True, null=True)

    # Permanent Address Information
    permanent_division = models.CharField(max_length=255, blank=True, null=True)
    permanent_district = models.CharField(max_length=255, blank=True, null=True)
    permanent_thana = models.CharField(max_length=255, blank=True, null=True)
    permanent_route = models.CharField(max_length=255, blank=True, null=True)
    permanent_area = models.CharField(max_length=255, blank=True, null=True)
    permanent_village_street = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_office = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_code = models.CharField(max_length=100, blank=True, null=True)

    # Additional Information
    photo = models.ImageField(upload_to='image/', blank=True, null=True)
    shop_photo = models.ImageField(upload_to='image/', blank=True, null=True)
    nid_front_photo = models.ImageField(upload_to='image/', blank=True, null=True)
    nid_back_photo = models.ImageField(upload_to='image/', blank=True, null=True)

    # Previous Records
    previous_account = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    khatian_number = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_customer = Customer.objects.order_by('id').last()

            if last_customer:
                new_user_id = last_customer.id + 1
            else:
                new_user_id = 1

            self.code = f"K{new_user_id:05}"

        super(Customer, self).save(*args, **kwargs)



