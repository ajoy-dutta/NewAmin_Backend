from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('divisions/', DivisionListCreateAPIView.as_view(), name='division-list-create'),
    path('divisions/<int:pk>/', DivisionRetrieveUpdateDestroyAPIView.as_view(), name='division-detail'),
    path('districts/', DistrictListCreateAPIView.as_view(), name='district-list-create'),
    path('districts/<int:pk>/', DistrictRetrieveUpdateDestroyAPIView.as_view(), name='district-detail'),
    path('thana/', ThanaListCreateAPIView.as_view(), name='thana-list-create'),
    path('thana/<int:pk>/', ThanaRetrieveUpdateDestroyAPIView.as_view(), name='thana-detail'),
    path('area/', AreaListCreateAPIView.as_view(), name='area-list-create'),
    path('area/<int:pk>/', AreaRetrieveUpdateDestroyAPIView.as_view(), name='area-detail'),  
    path('route/', RouteListCreateAPIView.as_view(), name='route-list-create'),
    path('route/<int:pk>/', RouteRetrieveUpdateDestroyAPIView.as_view(), name='route-detail'),
    path('godown/', GodownListCreateAPIView.as_view(), name='godown'),
    path('godown/<int:pk>/', GodownListRetrieveUpdateDestroyAPIView.as_view(), name='godown-detail') ,
    path('bank_info/', ShopBankInfoListCreateView.as_view(), name='bank_info_list_create'),
    path('bank_info/<int:pk>/', ShopBankInfoDetailView.as_view(), name='bank_info_detail'),  
    path('payment_method/', BankMethodListCreateView.as_view(), name='bank_method_list_create'),
    path('payment_method/<int:pk>/', BankMethodDetailView.as_view(), name='bank_method_detail'),
    path('cost_method/', CostMethodListCreateView.as_view(), name='cost_method_list_create'),
    path('cost_method/<int:pk>/', CostMethodDetailView.as_view(), name='cost_method_detail'),
    
]