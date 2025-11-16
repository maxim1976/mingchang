from django.contrib import admin
from django.utils.html import format_html
from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    """Admin interface for ContactInquiry model."""
    
    list_display = [
        'name', 'email', 'phone', 'subject_display', 
        'product_name', 'status', 'language_preference', 
        'created_at', 'is_new_inquiry', 'response_time_display'
    ]
    
    list_filter = [
        'status', 'language_preference', 'created_at', 
        'replied_at', 'updated_at'
    ]
    
    search_fields = [
        'name', 'email', 'phone', 'subject', 
        'message', 'product_name'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at', 'is_new', 
        'response_time_display', 'message_preview'
    ]
    
    ordering = ['-created_at']
    
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_in_progress', 'mark_as_replied', 'mark_as_resolved']
    
    fieldsets = (
        ('Customer Information', {
            'fields': (
                'name', 'phone', 'email', 'language_preference'
            )
        }),
        ('Inquiry Details', {
            'fields': (
                'subject', 'product_name', 'message_preview', 'message'
            )
        }),
        ('Status & Management', {
            'fields': (
                'status', 'admin_notes', 'replied_at'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'response_time_display'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def subject_display(self, obj):
        """Display subject with fallback."""
        return obj.subject or "一般詢問 General Inquiry"
    subject_display.short_description = 'Subject'
    
    def is_new_inquiry(self, obj):
        """Display if inquiry is new."""
        if obj.is_new:
            return format_html(
                '<span style="color: #dc2626; font-weight: bold;">🔥 New</span>'
            )
        return ""
    is_new_inquiry.short_description = 'New?'
    
    def response_time_display(self, obj):
        """Display response time if available."""
        if obj.response_time:
            days = obj.response_time.days
            hours, remainder = divmod(obj.response_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        return "-"
    response_time_display.short_description = 'Response Time'
    
    def message_preview(self, obj):
        """Display truncated message for preview."""
        if obj.message:
            preview = obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
            return format_html(
                '<div style="max-width: 300px; white-space: pre-wrap;">{}</div>',
                preview
            )
        return ""
    message_preview.short_description = 'Message Preview'
    
    def mark_as_in_progress(self, request, queryset):
        """Mark selected inquiries as in progress."""
        updated = queryset.update(status='in_progress')
        self.message_user(
            request, 
            f"{updated} inquiry(ies) marked as in progress."
        )
    mark_as_in_progress.short_description = 'Mark as in progress'
    
    def mark_as_replied(self, request, queryset):
        """Mark selected inquiries as replied."""
        for inquiry in queryset:
            inquiry.mark_as_replied()
        self.message_user(
            request,
            f"{queryset.count()} inquiry(ies) marked as replied."
        )
    mark_as_replied.short_description = 'Mark as replied'
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected inquiries as resolved."""
        updated = queryset.update(status='resolved')
        self.message_user(
            request,
            f"{updated} inquiry(ies) marked as resolved."
        )
    mark_as_resolved.short_description = 'Mark as resolved'
    
    def get_queryset(self, request):
        """Optimize queryset to prevent N+1 queries."""
        return super().get_queryset(request).select_related()
