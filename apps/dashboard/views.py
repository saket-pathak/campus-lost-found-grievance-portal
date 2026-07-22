from django.views.generic import TemplateView
from core.mixins import StaffOrAdminRequiredMixin
from grievance.models import Grievance
from lostfound.models import ClaimRequest, FoundItem, LostItem
from .stats import get_grievance_stats, get_lostfound_stats

class DashboardIndexView(StaffOrAdminRequiredMixin, TemplateView):
    """
    Consolidated control panel for staff and administrators.
    Provides analytics counters and feeds of active cases.
    """
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grievance_stats'] = get_grievance_stats()
        context['lostfound_stats'] = get_lostfound_stats()
        
        context['recent_grievances'] = Grievance.objects.all().order_by('-created_at')[:10]
        context['pending_claims'] = ClaimRequest.objects.filter(status='pending').order_by('-created_at')[:10]
        context['recent_lost'] = LostItem.objects.all().order_by('-created_at')[:5]
        context['recent_found'] = FoundItem.objects.all().order_by('-created_at')[:5]
        
        return context
