from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class LostItem(TimeStampedModel):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('books', 'Books & Notebooks'),
        ('documents', 'Documents & IDs'),
        ('clothing', 'Clothing & Accessories'),
        ('keys', 'Keys'),
        ('bags', 'Bags & Backpacks'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('matched', 'Matched'),
        ('closed', 'Closed'),
    )
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lost_items'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    location_lost = models.CharField(max_length=200)
    date_lost = models.DateField()
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    
    def __str__(self):
        return f"Lost: {self.title} ({self.get_status_display()})"

class FoundItem(TimeStampedModel):
    CATEGORY_CHOICES = LostItem.CATEGORY_CHOICES
    
    STATUS_CHOICES = (
        ('unclaimed', 'Unclaimed'),
        ('claimed', 'Claimed'),
    )
    
    finder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='found_items'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    location_found = models.CharField(max_length=200)
    date_found = models.DateField()
    image = models.ImageField(upload_to='found_items/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='unclaimed')
    
    def __str__(self):
        return f"Found: {self.title} ({self.get_status_display()})"

class ClaimRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    found_item = models.ForeignKey(
        FoundItem,
        on_delete=models.CASCADE,
        related_name='claim_requests'
    )
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claim_requests'
    )
    proof_description = models.TextField(
        help_text="Provide details describing how you lost the item or other proof that it belongs to you."
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Claim by {self.claimant.username} for {self.found_item.title} ({self.get_status_display()})"
