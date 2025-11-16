from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ContactInquiry
from .forms import ContactForm, ProductInquiryForm
from apps.shop.models import Product, CompanyInfo


class ContactView(CreateView):
    """Contact form view for general inquiries."""
    model = ContactInquiry
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.get_company_info()
        return context
    
    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        
        # Send email notification to shop owners
        self.send_notification_email(self.object)
        
        # Add success message
        messages.success(
            self.request,
            '感謝您的詢問！我們會盡快回覆您。Thank you for your inquiry! We will respond as soon as possible.'
        )
        
        # For AJAX requests, return JSON response
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': '詢問已送出！我們會盡快回覆您。Inquiry submitted! We will respond soon.',
                'redirect_url': str(self.success_url)
            })
        
        return response
    
    def form_invalid(self, form):
        """Handle form validation errors."""
        response = super().form_invalid(form)
        
        # For AJAX requests, return JSON response with errors
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors,
                'message': '表單填寫有誤，請檢查並重新提交。Form validation failed, please check and resubmit.'
            })
        
        return response
    
    def send_notification_email(self, inquiry):
        """Send email notification to shop owners."""
        try:
            company_info = CompanyInfo.get_company_info()
            
            subject = f'新的客戶詢問 New Customer Inquiry - {inquiry.subject or "一般詢問 General Inquiry"}'
            
            message = f"""
新的客戶詢問 New Customer Inquiry
===============================

客戶資訊 Customer Information:
姓名 Name: {inquiry.name}
電話 Phone: {inquiry.phone}
信箱 Email: {inquiry.email}
語言偏好 Language: {inquiry.get_language_preference_display()}

主旨 Subject: {inquiry.subject or "一般詢問 General Inquiry"}

詢問產品 Product: {inquiry.product_name or "無指定 Not specified"}

詢問內容 Message:
{inquiry.message}

提交時間 Submitted: {inquiry.created_at.strftime("%Y-%m-%d %H:%M")}

請透過客戶提供的聯絡方式回覆此詢問。
Please respond to this inquiry using the customer's provided contact information.
            """
            
            recipient_email = company_info.email if company_info else 'info@mingchang.com.tw'
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=True  # Don't break the form submission if email fails
            )
            
        except Exception as e:
            # Log the error but don't break the form submission
            print(f"Email notification failed: {e}")


class ProductInquiryView(CreateView):
    """Product-specific inquiry view."""
    model = ContactInquiry
    form_class = ProductInquiryForm
    template_name = 'contact/product_inquiry.html'
    success_url = reverse_lazy('contact:success')
    
    def get_form_kwargs(self):
        """Pass product to form."""
        kwargs = super().get_form_kwargs()
        product_slug = self.kwargs.get('slug')
        if product_slug:
            kwargs['product'] = get_object_or_404(Product, slug=product_slug)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product_slug = self.kwargs.get('slug')
        if product_slug:
            context['product'] = get_object_or_404(Product, slug=product_slug)
        
        context['company_info'] = CompanyInfo.get_company_info()
        return context
    
    def form_valid(self, form):
        """Handle successful form submission."""
        response = super().form_valid(form)
        
        # Send email notification
        self.send_notification_email(self.object)
        
        # Add success message
        messages.success(
            self.request,
            '感謝您的產品詢問！我們會盡快回覆您。Thank you for your product inquiry! We will respond as soon as possible.'
        )
        
        return response
    
    def send_notification_email(self, inquiry):
        """Send email notification for product inquiry."""
        # Similar to ContactView but with product-specific subject
        try:
            company_info = CompanyInfo.get_company_info()
            
            subject = f'產品詢問 Product Inquiry - {inquiry.product_name or inquiry.subject}'
            
            message = f"""
產品詢問 Product Inquiry
=======================

客戶資訊 Customer Information:
姓名 Name: {inquiry.name}
電話 Phone: {inquiry.phone}
信箱 Email: {inquiry.email}

詢問產品 Product: {inquiry.product_name}
主旨 Subject: {inquiry.subject or "產品詢問 Product Inquiry"}

詢問內容 Message:
{inquiry.message}

提交時間 Submitted: {inquiry.created_at.strftime("%Y-%m-%d %H:%M")}

請盡快回覆此產品詢問。
Please respond to this product inquiry as soon as possible.
            """
            
            recipient_email = company_info.email if company_info else 'info@mingchang.com.tw'
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=True
            )
            
        except Exception as e:
            print(f"Email notification failed: {e}")


class ContactSuccessView(TemplateView):
    """Contact form success page."""
    template_name = 'contact/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.get_company_info()
        return context
