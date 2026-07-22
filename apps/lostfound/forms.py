from django import forms
from .models import LostItem, FoundItem, ClaimRequest

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'category', 'location_lost', 'date_lost', 'contact_email', 'contact_number', 'image']
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date'}),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['title', 'description', 'category', 'location_found', 'date_found', 'contact_email', 'contact_number', 'image']
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'}),
        }

class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['proof_description']
