# Generated by Django 5.1.5 on 2025-03-08 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=255, verbose_name='পেমেন্ট মেথড')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('user_code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('user_type', models.CharField(choices=[('Shop Admin', 'Shop Admin'), ('Manager', 'Manager'), ('Account Officer', 'Account Officer'), ('Collection Representative (CR)', 'Collection Representative (CR)'), ('Sales Representative (SR)', 'Sales Representative (SR)')], max_length=50)),
                ('mobile_1', models.CharField(max_length=15)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10, null=True)),
                ('religion', models.CharField(blank=True, choices=[('Islam', 'Islam'), ('Christianity', 'Christianity'), ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Other', 'Other')], max_length=100, null=True)),
                ('national_id', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_2', models.CharField(blank=True, max_length=15, null=True)),
                ('father_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('mother_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image', models.ImageField(blank=True, default='Employee_image', null=True, upload_to='image/')),
                ('nid_image', models.ImageField(blank=True, default='NID_image', null=True, upload_to='image/')),
                ('password', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.IntegerField(blank=True, default=0)),
                ('current_village', models.CharField(blank=True, max_length=255, null=True)),
                ('current_union', models.CharField(blank=True, max_length=255, null=True)),
                ('current_post_office', models.CharField(blank=True, max_length=255, null=True)),
                ('current_post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('current_division', models.CharField(blank=True, max_length=255, null=True)),
                ('current_district', models.CharField(blank=True, max_length=255, null=True)),
                ('current_thana', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_village', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_union', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_post_office', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('permanent_district', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_division', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_thana', models.CharField(blank=True, max_length=255, null=True)),
                ('reference_person', models.CharField(blank=True, max_length=255, null=True)),
                ('reference_person_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GodownList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=255, null=True)),
                ('godown_name', models.CharField(blank=True, max_length=255, null=True)),
                ('godown_address', models.TextField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/Products/')),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ShopBankInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='store.division')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(blank=True, max_length=255, null=True)),
                ('institute_name', models.CharField(blank=True, max_length=255, null=True)),
                ('passing_year', models.CharField(blank=True, max_length=4, null=True)),
                ('gpa_grade', models.CharField(blank=True, max_length=10, null=True)),
                ('board_or_university', models.CharField(blank=True, max_length=255, null=True)),
                ('group_or_department', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='store.employee')),
            ],
        ),
        migrations.CreateModel(
            name='BankingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(blank=True, max_length=255, null=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=255, null=True)),
                ('routing_number', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banking_details', to='store.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('working_time', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='store.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='store.route')),
            ],
        ),
        migrations.CreateModel(
            name='Thana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thanas', to='store.district')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='store.thana'),
        ),
    ]
