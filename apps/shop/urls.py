"""Shop app URL configuration."""

from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # About & Company Info
    path('about/', views.AboutView.as_view(), name='about'),
    path('location/', views.LocationView.as_view(), name='location'),
]