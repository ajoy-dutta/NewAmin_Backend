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
    
    USER_TYPE_CHOICES = [
        ('Shop Admin', 'Shop Admin'),
        ('Manager', 'Manager'),
        ('Account Officer', 'Account Officer'),
        ('Collection Representative (CR)', 'Collection Representative (CR)'),
        ('Sales Representative (SR)', 'Sales Representative (SR)'),
    ]
    
    # Gender Choices
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    # Define choices for blood group
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # Define choices for religion
    RELIGION_CHOICES = [
        ('Islam', 'Islam'),
        ('Christianity', 'Christianity'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Other', 'Other'),
    ]
    
    full_name = models.CharField(max_length=255)  # Required
    user_code = models.CharField(max_length=50, unique=True,blank=True, null= True)  # Required
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)   # Required
    mobile_1 = models.CharField(max_length=15)  # Required

    # Optional fields
    joining_date = models.DateField(blank=True, null = True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null = True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True) 
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, blank=True, null=True) 
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES, blank=True, null=True) 
    national_id = models.CharField(max_length=50, blank=True, null=True)
    mobile_2 = models.CharField(max_length=15, blank=True, null=True)
    father_mobile = models.CharField(max_length=15, blank=True, null=True)
    mother_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(default = "Employee_image",upload_to='image/', blank=True, null=True)
    nid_image = models.ImageField(default = "NID_image",upload_to='image/', blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null= True)
    is_active = models.BooleanField(default= False, blank=True, null = True)
    
    # Current Address
    current_village = models.CharField(max_length=255, blank=True, null=True)
    current_union = models.CharField(max_length=255, blank=True, null=True)
    current_post_office = models.CharField(max_length=255, blank=True, null=True)
    current_post_code = models.CharField(max_length=10, blank=True, null=True)
    current_division = models.CharField(max_length=255, blank=True, null=True)
    current_district = models.CharField(max_length=255, blank=True, null=True)
    current_thana = models.CharField(max_length=255, blank=True, null=True)

    # Permanent Address
    permanent_village = models.CharField(max_length=255, blank=True, null=True)
    permanent_union = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_office = models.CharField(max_length=255, blank=True, null=True)
    permanent_post_code = models.CharField(max_length=10, blank=True, null=True)
    permanent_district = models.CharField(max_length=255, blank=True, null=True)
    permanent_division = models.CharField(max_length=255, blank=True, null=True)
    permanent_thana = models.CharField(max_length=255, blank=True, null=True)
    
    # Reference 
    reference_person = models.CharField(max_length=255, blank= True, null = True)
    reference_person_number = models.CharField(max_length=255, blank= True, null = True)
    
    
    def save(self, *args, **kwargs):
        if not self.user_code:
            last_employee = Employee.objects.order_by('id').last()

            if last_employee:
                new_user_id = last_employee.id + 1
            else:
                new_user_id = 1

            self.user_code = f"N{new_user_id:05}"

        super(Employee, self).save(*args, **kwargs) 

    def __str__(self):
        return self.full_name


class Education(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="education")
    exam_name = models.CharField(max_length=255, blank=True, null=True) 
    institute_name = models.CharField(max_length=255, blank=True, null=True) 
    passing_year = models.CharField(max_length=4, blank=True, null=True)  
    gpa_grade = models.CharField(max_length=10, blank=True, null=True)  
    board_or_university = models.CharField(max_length=255, blank=True, null=True)
    group_or_department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.exam_name} - {self.institute_name}"
    

class Experience(models.Model):
    # Job experience details
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    working_time = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class BankingDetails(models.Model):
    # Banking or mobile banking details
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="banking_details")
    payment_method = models.CharField(max_length=255,blank=True, null=True)  # Required (e.g., Bank, Mobile Banking)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)  # Required
    account_number = models.CharField(max_length=50, blank=True, null=True)  # Required
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    routing_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.payment_method} - {self.account_holder_name}"
    

class Product(models.Model):
    name = models.CharField(max_length=255,unique=True,blank=True, null = True)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="types")
    image = models.ImageField(upload_to='image/Products/', blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_code = ProductType.objects.all().order_by('id').last()
            new_code = f"{last_code.id + 1:04d}" if last_code else "0001"
            self.code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.product.name}"

