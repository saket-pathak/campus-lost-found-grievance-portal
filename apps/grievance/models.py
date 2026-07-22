from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class GrievanceCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.department})"
        
    class Meta:
        verbose_name_plural = "Grievance Categories"

class Grievance(TimeStampedModel):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    )
    
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_grievances'
    )
    category = models.ForeignKey(
        GrievanceCategory,
        on_delete=models.PROTECT,
        related_name='grievances'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(upload_to='grievance_attachments/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_grievances'
    )
    
    def __str__(self):
        return f"Grievance #{self.id}: {self.title} ({self.get_status_display()})"

class StatusLog(models.Model):
    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='status_logs'
    )
    old_status = models.CharField(max_length=15)
    new_status = models.CharField(max_length=15)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Log #{self.id}: Grievance #{self.grievance.id} transitioned from {self.old_status} to {self.new_status}"
