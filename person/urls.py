from django.urls import path
from .views import*

urlpatterns = [
    path('mohajons/', MohajonListCreateAPIView.as_view(), name='mohajon-list-create'),
    path('mohajons/<pk>/', MohajonDestroyUpdateAPIView.as_view(), name='mohajon-destroy-update'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<pk>/', CustomerDestroyUpdateAPIView.as_view(), name='customer-destroy-update'),


    
]
