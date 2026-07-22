from django.contrib import admin
from .models import LostItem, FoundItem, ClaimRequest

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'category', 'status', 'date_lost', 'created_at')
    list_filter = ('category', 'status', 'date_lost')
    search_fields = ('title', 'description', 'location_lost', 'reporter__username')

@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'finder', 'category', 'status', 'date_found', 'created_at')
    list_filter = ('category', 'status', 'date_found')
    search_fields = ('title', 'description', 'location_found', 'finder__username')

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('found_item', 'claimant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('found_item__title', 'claimant__username', 'proof_description')
