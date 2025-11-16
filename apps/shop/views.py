from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Category, Product, CompanyInfo


class HomeView(TemplateView):
    """Homepage view displaying featured products and company intro."""
    template_name = 'shop/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured products (max 6 for homepage grid)
        featured_products = Product.objects.filter(
            is_featured=True, 
            is_available=True
        ).select_related('category').prefetch_related('images')[:6]
        
        # Get company information
        company_info = CompanyInfo.get_company_info()
        
        # Get all categories for navigation
        categories = Category.objects.filter(is_active=True).order_by('display_order')
        
        context.update({
            'featured_products': featured_products,
            'company_info': company_info,
            'categories': categories,
        })
        
        return context


class ProductListView(ListView):
    """Product listing view with category filtering and search."""
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Filter products by category, search, and availability."""
        queryset = Product.objects.filter(is_available=True).select_related(
            'category'
        ).prefetch_related('images')
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search filter
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name_zh__icontains=search_query) |
                Q(name_en__icontains=search_query) |
                Q(description_zh__icontains=search_query) |
                Q(description_en__icontains=search_query)
            )
        
        # Sort filter
        sort_by = self.request.GET.get('sort', 'featured')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'name':
            queryset = queryset.order_by('name_en')
        else:  # default: featured
            queryset = queryset.order_by('-is_featured', 'name_en')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories for filter sidebar
        categories = Category.objects.filter(is_active=True).order_by('display_order')
        
        # Get current filters for display
        current_category = None
        category_slug = self.request.GET.get('category')
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
        
        search_query = self.request.GET.get('q', '')
        sort_by = self.request.GET.get('sort', 'featured')
        
        context.update({
            'categories': categories,
            'current_category': current_category,
            'search_query': search_query,
            'sort_by': sort_by,
        })
        
        return context


class ProductDetailView(DetailView):
    """Product detail view with related products."""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        """Only show available products."""
        return Product.objects.filter(is_available=True).select_related(
            'category'
        ).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related products from same category (exclude current product)
        related_products = Product.objects.filter(
            category=self.object.category,
            is_available=True
        ).exclude(pk=self.object.pk).select_related(
            'category'
        ).prefetch_related('images')[:4]
        
        context['related_products'] = related_products
        
        return context


class AboutView(TemplateView):
    """About page with company information."""
    template_name = 'shop/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get company information
        company_info = CompanyInfo.get_company_info()
        
        context['company_info'] = company_info
        
        return context


class LocationView(TemplateView):
    """Location page with map and contact details."""
    template_name = 'shop/location.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get company information
        company_info = CompanyInfo.get_company_info()
        
        context['company_info'] = company_info
        
        return context
