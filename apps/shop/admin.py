from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, CompanyInfo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    
    list_display = [
        'name_zh', 'name_en', 'slug', 
        'display_order', 'is_active', 'product_count'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_zh', 'name_en', 'slug']
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ['display_order', 'name_en']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_zh', 'name_en', 'slug')
        }),
        ('Description', {
            'fields': ('description_zh', 'description_en'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def product_count(self, obj):
        """Display number of products in this category."""
        count = obj.products.count()
        return f"{count} product{'s' if count != 1 else ''}"
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    """Inline admin for ProductImage."""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text_zh', 'alt_text_en', 'display_order', 'is_primary']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Display thumbnail preview of image."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.thumbnail.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = [
        'name_zh', 'name_en', 'category', 'formatted_price',
        'stock_status', 'is_featured', 'is_available', 'image_count'
    ]
    list_filter = [
        'category', 'is_featured', 'is_available', 
        'stock_status', 'created_at'
    ]
    search_fields = ['name_zh', 'name_en', 'description_zh', 'description_en']
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ['-is_featured', 'name_en']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'category', 'name_zh', 'name_en', 'slug'
            )
        }),
        ('Description', {
            'fields': ('description_zh', 'description_en')
        }),
        ('Pricing & Measurements', {
            'fields': ('price', 'unit', 'weight_grams')
        }),
        ('Origin & Nutrition', {
            'fields': (
                'origin_zh', 'origin_en',
                'nutritional_info_zh', 'nutritional_info_en'
            ),
            'classes': ('collapse',)
        }),
        ('Status & Availability', {
            'fields': ('is_featured', 'is_available', 'stock_status')
        }),
    )
    
    def image_count(self, obj):
        """Display number of images for this product."""
        count = obj.images.count()
        primary_count = obj.images.filter(is_primary=True).count()
        primary_text = " (✓ primary)" if primary_count > 0 else " (no primary)"
        return f"{count} image{'s' if count != 1 else ''}{primary_text}"
    image_count.short_description = 'Images'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for ProductImage model."""
    
    list_display = [
        'product', 'display_order', 'is_primary', 'image_preview', 
        'alt_text_zh', 'alt_text_en'
    ]
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name_zh', 'product__name_en', 'alt_text_zh', 'alt_text_en']
    ordering = ['product', 'display_order']
    
    fields = [
        'product', 'image', 'image_preview', 
        'alt_text_zh', 'alt_text_en', 
        'display_order', 'is_primary'
    ]
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """Display thumbnail preview of image."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.medium.url if obj.medium else obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """Admin interface for CompanyInfo model."""
    
    def has_add_permission(self, request):
        """Only allow one company info object."""
        return not CompanyInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of company info."""
        return False
    
    fieldsets = (
        ('Company Details', {
            'fields': ('name_zh', 'name_en')
        }),
        ('About Section', {
            'fields': ('about_zh', 'about_en')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address_zh', 'address_en')
        }),
        ('Location (Google Maps)', {
            'fields': ('latitude', 'longitude'),
            'description': 'Enter coordinates for Google Maps integration'
        }),
        ('Business Hours', {
            'fields': ('business_hours_zh', 'business_hours_en')
        }),
        ('Social Media & Messaging', {
            'fields': ('line_id', 'whatsapp', 'facebook_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('hero_image',),
            'classes': ('collapse',)
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to edit view if company info exists, otherwise show add view."""
        if CompanyInfo.objects.exists():
            company_info = CompanyInfo.objects.first()
            return self.change_view(request, str(company_info.pk), extra_context)
        return super().changelist_view(request, extra_context)
