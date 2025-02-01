from django.urls import path
from .views import MohajonListCreateAPIView, MohajonDestroyUpdateAPIView

urlpatterns = [
    path('mohajons/', MohajonListCreateAPIView.as_view(), name='mohajon-list-create'),
    path('mohajons/<pk>/', MohajonDestroyUpdateAPIView.as_view(), name='mohajon-destroy-update'),
]
