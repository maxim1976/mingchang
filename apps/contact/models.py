from django.db import models
from django.utils import timezone


class ContactInquiry(models.Model):
    """Customer contact inquiry model."""
    
    # Customer information
    name = models.CharField(
        max_length=100,
        verbose_name='Name',
        help_text='Customer full name'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone',
        help_text='Customer phone number'
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Customer email address'
    )
    
    # Inquiry details
    subject = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Subject',
        help_text='Inquiry subject (optional)'
    )
    message = models.TextField(
        verbose_name='Message',
        help_text='Customer inquiry message'
    )
    
    # Optional product reference
    product_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Product of Interest',
        help_text='Product the customer is asking about (optional)'
    )
    
    # Language preference
    LANGUAGE_CHOICES = [
        ('zh', 'Traditional Chinese'),
        ('en', 'English'),
        ('both', 'Both Languages'),
    ]
    language_preference = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='zh',
        verbose_name='Language Preference'
    )
    
    # Status tracking
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Status'
    )
    
    # Admin notes
    admin_notes = models.TextField(
        blank=True,
        verbose_name='Admin Notes',
        help_text='Internal notes for staff'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replied_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Replied At',
        help_text='When the inquiry was replied to'
    )
    
    class Meta:
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'General Inquiry'} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def mark_as_replied(self):
        """Mark inquiry as replied."""
        self.status = 'replied'
        self.replied_at = timezone.now()
        self.save()
    
    @property
    def is_new(self):
        """Check if inquiry is new (less than 24 hours old)."""
        return (timezone.now() - self.created_at).days == 0
    
    @property
    def response_time(self):
        """Calculate response time if replied."""
        if self.replied_at:
            return self.replied_at - self.created_at
        return None
