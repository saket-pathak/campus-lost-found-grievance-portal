from django.urls import path
from .views import (
    LostItemListView, LostItemDetailView, LostItemCreateView, LostItemUpdateView,
    FoundItemListView, FoundItemDetailView, FoundItemCreateView,
    ClaimRequestCreateView, ClaimRequestActionView
)

app_name = 'lostfound'

urlpatterns = [
    # Lost Items
    path('lost/', LostItemListView.as_view(), name='lost_list'),
    path('lost/new/', LostItemCreateView.as_view(), name='lost_create'),
    path('lost/<int:pk>/', LostItemDetailView.as_view(), name='lost_detail'),
    path('lost/<int:pk>/edit/', LostItemUpdateView.as_view(), name='lost_update'),
    
    # Found Items
    path('found/', FoundItemListView.as_view(), name='found_list'),
    path('found/new/', FoundItemCreateView.as_view(), name='found_create'),
    path('found/<int:pk>/', FoundItemDetailView.as_view(), name='found_detail'),
    
    # Claims
    path('found/<int:found_item_pk>/claim/', ClaimRequestCreateView.as_view(), name='claim_create'),
    path('claim/<int:pk>/action/', ClaimRequestActionView.as_view(), name='claim_action'),
]
