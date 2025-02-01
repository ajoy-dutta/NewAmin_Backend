from django.db import models


class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Division, related_name='districts', on_delete=models.CASCADE)  # District has a parent Division

    def __str__(self):
        return self.name


class Thana(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(District, related_name='thanas', on_delete=models.CASCADE)  # Thana has a parent District

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Thana, related_name='routes', on_delete=models.CASCADE)  # Route has a parent Thana

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Route, related_name='areas', on_delete=models.CASCADE)  # Area has a parent Route

    def __str__(self):
        return self.name

class GodownList(models.Model):
    shop_name = models.CharField(max_length=255, null= True, blank=True)
    godown_name = models.CharField(max_length=255, null= True, blank=True)
    godown_address = models.TextField(max_length=255,null= True, blank=True)

    def __str__(self):
        return f"{self.shop_name} - {self.godown_name}"



class ShopBankInfo(models.Model):
    shop_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    bank_address = models.TextField()

    def __str__(self):
        return self.shop_name


class BankMethod(models.Model):
    payment_method = models.CharField(max_length=255, verbose_name="পেমেন্ট মেথড")

    def __str__(self):
        return self.payment_method
    
    
class Cost(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    



class Employee(models.Model):
    full_name = models.CharField(max_length=255)  # Required
    user_code = models.CharField(max_length=50, unique=True)  # Required
    user_type = models.CharField(max_length=50)  # Required
    mobile_1 = models.CharField(max_length=15)  # Required

    # Optional fields
    gender = models.CharField(max_length=20, blank=True, null = True)  # Required
    dob = models.DateField(blank=True, null = True)  # Required
    joining_date = models.DateField(blank=True, null = True)  # Required
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=50, default='Bangladeshi', blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    mobile_2 = models.CharField(max_length=15, blank=True, null=True)
    father_mobile = models.CharField(max_length=15, blank=True, null=True)
    mother_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Current Address
    current_village = models.CharField(max_length=255, blank=True, null=True)
    current_union = models.CharField(max_length=255, blank=True, null=True)
    current_post_office = models.CharField(max_length=255, blank=True, null=True)
    current_post_code = models.CharField(max_length=10, blank=True, null=True)
    current_district = models.CharField(max_length=255, blank=True, null=True)
    current_thana = models.CharField(max_length=255, blank=True, null=True)

    # Permanent Address
    permanent_village = models.CharField(max_length=255, blank=True, null=True)
    permanent_union = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_office = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_code = models.CharField(max_length=10, blank=True, null=True)
    permanent_district = models.CharField(max_length=255, blank=True, null=True)
    permanent_thana = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Education(models.Model):
    # ForeignKey to link education to a user
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="education")

    # Education Details (required fields)
    exam_name = models.CharField(max_length=255)  # Required
    institute_name = models.CharField(max_length=255)  # Required
    passing_year = models.CharField(max_length=4)  # Required
    gpa_grade = models.CharField(max_length=10)  # Required

    # Optional fields
    board_or_university = models.CharField(max_length=255, blank=True, null=True)
    group_or_department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.exam_name} - {self.institute_name}"
    

class Experience(models.Model):
    # Job experience details
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=255)  # Required
    position = models.CharField(max_length=255)  # Required
    address = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class BankingDetails(models.Model):
    # Banking or mobile banking details
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="banking_details")
    payment_method = models.CharField(max_length=255)  # Required (e.g., Bank, Mobile Banking)
    account_holder_name = models.CharField(max_length=255)  # Required
    account_number = models.CharField(max_length=50)  # Required
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    routing_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.payment_method} - {self.account_holder_name}"
