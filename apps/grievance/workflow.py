from django.core.exceptions import ValidationError
from django.db import transaction
from .models import StatusLog

ALLOWED_STATUSES = {'open', 'in_review', 'resolved', 'escalated'}

def transition_status(grievance, new_status, actor, note=""):
    """
    Safely transitions the status of a grievance, logs the change,
    and validates authorization and logical constraints.
    """
    if new_status not in ALLOWED_STATUSES:
        raise ValidationError(f"Invalid status: {new_status}")
        
    old_status = grievance.status
    if old_status == new_status:
        raise ValidationError(f"Grievance is already in status: {new_status}")
        
    # Check authorization
    is_staff_or_admin = actor.role in ('staff', 'admin') or actor.is_superuser
    is_submitter = actor == grievance.submitter
    
    if not (is_staff_or_admin or is_submitter):
        raise ValidationError("You are not authorized to change the status of this grievance.")
        
    # If the student (submitter) transitions status, they can only transition it to 'resolved' (cancel/close it)
    if not is_staff_or_admin and is_submitter:
        if new_status != 'resolved':
            raise ValidationError("Students can only transition their grievances to 'resolved'.")
            
    with transaction.atomic():
        grievance.status = new_status
        grievance.save()
        
        log = StatusLog.objects.create(
            grievance=grievance,
            old_status=old_status,
            new_status=new_status,
            changed_by=actor,
            note=note
        )
        
    return log
