from django.urls import path
from .views import*

urlpatterns = [
    path('purchases/', PurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('purchases/<pk>/', PurchaseRetrieveUpdateDestroyView.as_view(), name='purchase-detail'),
    
    path('sell/', SellListCreateView.as_view(), name='sell-list-create'),
    path('sell/<pk>/', SellRetrieveUpdateDestroyView.as_view(), name='sell-list-create'),

    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('employee-payments/', EmployeePaymentListCreateView.as_view(), name='employee-payment-list-create'),
    path('other-payments/', OtherPaymentListCreateView.as_view(), name='other-payment-list-create'),


]