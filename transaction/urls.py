from django.urls import path
from .views import*

urlpatterns = [
    path('purchases/', PurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('purchases/<pk>/', PurchaseRetrieveUpdateDestroyView.as_view(), name='purchase-detail'),
    
    path('sell/', SellListCreateView.as_view(), name='sell-list-create'),
]