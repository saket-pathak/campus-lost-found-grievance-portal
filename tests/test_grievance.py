import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from grievance.models import Grievance, GrievanceCategory, StatusLog
from grievance.workflow import transition_status

User = get_user_model()

@pytest.mark.django_db
def test_grievance_transitions():
    student = User.objects.create_user(username='student', password='p', role='student')
    staff = User.objects.create_user(username='staff', password='p', role='staff')
    
    cat = GrievanceCategory.objects.create(name="Hostel Maintenance", department="Hostels")
    
    grv = Grievance.objects.create(
        submitter=student,
        category=cat,
        title="Broken fan in Room 302",
        description="The ceiling fan is not working."
    )
    
    assert grv.status == 'open'
    
    log1 = transition_status(grv, 'in_review', staff, "Inspecting the room fan today.")
    assert grv.status == 'in_review'
    assert log1.old_status == 'open'
    assert log1.new_status == 'in_review'
    
    with pytest.raises(ValidationError):
        transition_status(grv, 'in_review', staff, "Duplicate transition.")
        
    with pytest.raises(ValidationError):
        transition_status(grv, 'escalated', student, "I want to escalate.")
        
    transition_status(grv, 'resolved', student, "It got fixed on its own.")
    assert grv.status == 'resolved'
