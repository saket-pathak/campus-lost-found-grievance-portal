from django import forms
from django.contrib.auth import get_user_model
from .models import Grievance, GrievanceCategory

User = get_user_model()

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['title', 'description', 'category', 'attachment']

class GrievanceAssignForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=True,
        empty_label="Select Handler"
    )
    
    class Meta:
        model = Grievance
        fields = ['assigned_to']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate queryset dynamically with staff/admins
        self.fields['assigned_to'].queryset = User.objects.filter(role__in=['staff', 'admin'])

class GrievanceStatusTransitionForm(forms.Form):
    status = forms.ChoiceField(choices=Grievance.STATUS_CHOICES, required=True)
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, help_text="Reason for change")
