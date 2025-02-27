from django.contrib import admin
from .models import*

# Register your models here.

admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
admin.site.register(TransactionDetail)
admin.site.register(Sell)
admin.site.register(ProductSellInfo)
admin.site.register(CostInfo)
admin.site.register(IncomeInfo)
admin.site.register(Payment)
admin.site.register(PaymentDetail)
admin.site.register(Invoice)




