from django.db.models import Count, Avg, F
from django.utils import timezone
from datetime import timedelta, date
from grievance.models import Grievance
from lostfound.models import FoundItem

def get_grievance_stats():
    """
    Aggregates statistics for the Grievance module:
    - active grievances by category
    - counts by status
    - average turnaround time for resolved grievances
    """
    by_category = Grievance.objects.exclude(status='resolved').values(
        'category__name'
    ).annotate(count=Count('id')).order_by('-count')
    
    by_status = Grievance.objects.values('status').annotate(count=Count('id'))
    
    resolved = Grievance.objects.filter(status='resolved')
    if resolved.exists():
        avg_time = resolved.annotate(
            duration=F('updated_at') - F('created_at')
        ).aggregate(average_duration=Avg('duration'))['average_duration']
        
        if avg_time:
            avg_days = avg_time.days
            avg_hours = int(avg_time.seconds / 3600)
            avg_str = f"{avg_days}d {avg_hours}h"
        else:
            avg_str = "N/A"
    else:
        avg_str = "N/A"
        
    status_dict = {item['status']: item['count'] for item in by_status}
    for stat in ('open', 'in_review', 'resolved', 'escalated'):
        if stat not in status_dict:
            status_dict[stat] = 0
            
    return {
        'by_category': list(by_category),
        'by_status': status_dict,
        'average_turnaround': avg_str
    }

def get_lostfound_stats():
    """
    Aggregates statistics for the Lost & Found module:
    - age breakdown of unclaimed items (last 7 days, last 30 days, older)
    """
    today = date.today()
    unclaimed = FoundItem.objects.filter(status='unclaimed')
    
    last_7_days = unclaimed.filter(date_found__gte=today - timedelta(days=7)).count()
    last_30_days = unclaimed.filter(date_found__gte=today - timedelta(days=30)).count()
    older = unclaimed.filter(date_found__lt=today - timedelta(days=30)).count()
    
    return {
        'unclaimed_total': unclaimed.count(),
        'last_7_days': last_7_days,
        'last_30_days': last_30_days,
        'older': older,
    }
