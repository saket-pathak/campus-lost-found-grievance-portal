from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model

from lostfound.models import ClaimRequest
from grievance.models import Grievance, StatusLog
from .models import Notification
from .services import send_email_notification

User = get_user_model()

@receiver(post_save, sender=ClaimRequest)
def claim_request_notifications(sender, instance, created, **kwargs):
    found_item = instance.found_item
    claimant = instance.claimant
    finder = found_item.finder
    
    if created:
        msg = f"New claim request submitted for your found item '{found_item.title}' by {claimant.username}."
        link = reverse('lostfound:found_detail', kwargs={'pk': found_item.pk})
        Notification.objects.create(
            recipient=finder,
            message=msg,
            link=link
        )
        send_email_notification(
            finder,
            subject="New Claim Request Submitted",
            message=f"Hello {finder.username},\n\n{msg}\n\nView details: {request_url(link)}"
        )
    else:
        msg = f"Your claim request for '{found_item.title}' has been {instance.get_status_display().lower()}."
        link = reverse('lostfound:found_detail', kwargs={'pk': found_item.pk})
        Notification.objects.create(
            recipient=claimant,
            message=msg,
            link=link
        )
        send_email_notification(
            claimant,
            subject=f"Claim Request {instance.get_status_display()}",
            message=f"Hello {claimant.username},\n\n{msg}\n\nView details: {request_url(link)}"
        )

@receiver(post_save, sender=Grievance)
def grievance_notifications(sender, instance, created, **kwargs):
    link = reverse('grievance:grievance_detail', kwargs={'pk': instance.pk})
    
    if created:
        category = instance.category
        staff_users = User.objects.filter(role__in=['staff', 'admin'], department=category.department)
        msg = f"A new grievance has been submitted in your department ({category.department}): '{instance.title}'."
        
        for staff in staff_users:
            Notification.objects.create(
                recipient=staff,
                message=msg,
                link=link
            )
            send_email_notification(
                staff,
                subject="New Grievance Submitted",
                message=f"Hello {staff.username},\n\n{msg}\n\nView details: {request_url(link)}"
            )
            
    # Notify assignee if assigned
    if instance.assigned_to:
        msg = f"You have been assigned to handle grievance #{instance.pk}: '{instance.title}'."
        if not Notification.objects.filter(recipient=instance.assigned_to, message=msg).exists():
            Notification.objects.create(
                recipient=instance.assigned_to,
                message=msg,
                link=link
            )
            send_email_notification(
                instance.assigned_to,
                subject="Grievance Assigned to You",
                message=f"Hello {instance.assigned_to.username},\n\n{msg}\n\nView details: {request_url(link)}"
            )

@receiver(post_save, sender=StatusLog)
def grievance_status_changed_notification(sender, instance, created, **kwargs):
    if created:
        grievance = instance.grievance
        submitter = grievance.submitter
        msg = f"Your grievance '{grievance.title}' status was updated to '{grievance.get_status_display()}'. Note: {instance.note or 'None'}"
        link = reverse('grievance:grievance_detail', kwargs={'pk': grievance.pk})
        
        Notification.objects.create(
            recipient=submitter,
            message=msg,
            link=link
        )
        send_email_notification(
            submitter,
            subject="Grievance Status Updated",
            message=f"Hello {submitter.username},\n\n{msg}\n\nView details: {request_url(link)}"
        )

def request_url(path):
    # Helper to construct absolute/relative URL strings
    return f"http://localhost:8000{path}"
