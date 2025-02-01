from django.db import models
from .models import*
from store.models import ShopBankInfo  # Import ShopBankInfo from the store app

class Mohajon(models.Model):
    name = models.CharField(max_length=255)
    code = models.AutoField(primary_key=True)
    business_type = models.CharField(max_length=255, choices=[('মহাজন', 'মহাজন'),('চাষী','চাষী')])  # Updated field
    father_name = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
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



        
    def __str__(self):
        return self.name


class BankInfo(models.Model):
    user = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="banking_details")
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
