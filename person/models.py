from django.db import models
from .models import*
from store.models import ShopBankInfo  # Import ShopBankInfo from the store app

class Mohajon(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True,blank=True)  # Ensure this is a CharField, not AutoField
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



    def save(self, *args, **kwargs):
            if not self.code:  # If no code is set
                # Get the last code in the database, or default to 'NAS0' if none exist
                last_code = Mohajon.objects.order_by('code').last()
                if last_code:
                    # Increment the last code number
                    last_number = int(last_code.code[1:])  # Extract the number part after 'NAS'
                    self.code = f"N{last_number + 1:05}"  # Set new code as NAS{incremented_number}
                else:
                    self.code = "N00001"  # First code if no entries in the table

            super().save(*args, **kwargs)


class BankInfo(models.Model):
    user = models.ForeignKey(Mohajon, on_delete=models.CASCADE, related_name="banking_details")
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
            if not self.code:  # If no code is set
                # Get the last code in the database, or default to 'NAS0' if none exist
                last_code = Customer.objects.order_by('code').last()
                if last_code:
                    # Increment the last code number
                    last_number = int(last_code.code[1:])  # Extract the number part after 'NAS'
                    self.code = f"N{last_number + 1:05}"  # Set new code as NAS{incremented_number}
                else:
                    self.code = "N00001"  # First code if no entries in the table

            super().save(*args, **kwargs)


