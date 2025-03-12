from django.urls import path
from .views import*

urlpatterns = [
    path('purchases/', PurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('purchases/<pk>/', PurchaseRetrieveUpdateDestroyView.as_view(), name='purchase-detail'),
    
    path('sell/', SellListCreateView.as_view(), name='sell-list-create'),
    path('sell/<pk>/', SellRetrieveUpdateDestroyView.as_view(), name='sell-list-create'),

    
    path('payments-recieve/', PaymentRecieveListCreateView.as_view(), name='paymentRecieve-list-create'),
    path('payments-recieve/<int:pk>/', PaymentRecieveRetrieveUpdateDestroyView.as_view(), name='paymentRecieve-detail'),
    
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    
    
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-detail'),
    
    
    path('product-transfer/', GodownTransferView.as_view(), name = 'GodownTransferView'),

    path("bank-income/", BankIncomeCostListCreateView.as_view(), name="bank-income-list"),
    path("bank-income/<int:pk>/", BankIncomeCostUpdateView.as_view(), name="bank-income-detail"),  
]