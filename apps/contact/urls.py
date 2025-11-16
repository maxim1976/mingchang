"""Contact app URL configuration."""

from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # General contact form
    path('', views.ContactView.as_view(), name='contact'),
    
    # Product-specific inquiry
    path('product/<slug:slug>/', views.ProductInquiryView.as_view(), name='product_inquiry'),
    
    # Success page
    path('success/', views.ContactSuccessView.as_view(), name='success'),
]