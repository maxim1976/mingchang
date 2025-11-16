from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose
import os


class Category(models.Model):
    """Product category with bilingual support."""
    
    # Slug validator for URL-friendly identifiers
    slug_validator = RegexValidator(
        regex=r'^[a-z0-9-]+$',
        message='Slug must contain only lowercase letters, numbers, and hyphens.'
    )
    
    # Core fields
    name_zh = models.CharField(
        max_length=100, 
        verbose_name='Name (Chinese)',
        help_text='Category name in Traditional Chinese'
    )
    name_en = models.CharField(
        max_length=100, 
        verbose_name='Name (English)',
        help_text='Category name in English'
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        validators=[slug_validator],
        help_text='URL-friendly identifier (lowercase, numbers, hyphens only)'
    )
    
    # Descriptions
    description_zh = models.TextField(
        blank=True, 
        verbose_name='Description (Chinese)',
        help_text='Category description in Traditional Chinese'
    )
    description_en = models.TextField(
        blank=True, 
        verbose_name='Description (English)',
        help_text='Category description in English'
    )
    
    # Display settings
    display_order = models.PositiveIntegerField(
        default=0,
        help_text='Sort order for display (0 = first)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether category is visible to customers'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name_en']
        indexes = [
            models.Index(fields=['name_zh']),
            models.Index(fields=['name_en']),
            models.Index(fields=['display_order']),
        ]
    
    def __str__(self):
        return f"{self.name_zh} ({self.name_en})"
    
    def clean(self):
        """Validate that at least one name field is provided."""
        from django.core.exceptions import ValidationError
        
        if not self.name_zh and not self.name_en:
            raise ValidationError('At least one of Chinese or English name must be provided.')
    
    def get_absolute_url(self):
        """Return URL for this category's product list."""
        return reverse('shop:product_list') + f'?category={self.slug}'


class Product(models.Model):
    """Meat product with bilingual support and detailed attributes."""
    
    # Stock status choices
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('seasonal', 'Seasonal'),
    ]
    
    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Category'
    )
    
    # Basic info
    name_zh = models.CharField(
        max_length=200, 
        verbose_name='Name (Chinese)',
        help_text='Product name in Traditional Chinese'
    )
    name_en = models.CharField(
        max_length=200, 
        verbose_name='Name (English)',
        help_text='Product name in English'
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True,
        help_text='URL-friendly identifier'
    )
    
    # Descriptions
    description_zh = models.TextField(
        verbose_name='Description (Chinese)',
        help_text='Product description in Traditional Chinese'
    )
    description_en = models.TextField(
        verbose_name='Description (English)',
        help_text='Product description in English'
    )
    
    # Pricing and measurements
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Price in TWD (New Taiwan Dollar)'
    )
    unit = models.CharField(
        max_length=50,
        default='kg',
        help_text='Unit of measurement (e.g., kg, piece, pack)'
    )
    weight_grams = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text='Weight per unit in grams (if applicable)'
    )
    
    # Origin and nutrition info
    origin_zh = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Origin (Chinese)',
        help_text='Product origin/source in Traditional Chinese'
    )
    origin_en = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Origin (English)',
        help_text='Product origin/source in English'
    )
    nutritional_info_zh = models.TextField(
        blank=True,
        verbose_name='Nutritional Info (Chinese)',
        help_text='Nutritional information in Traditional Chinese'
    )
    nutritional_info_en = models.TextField(
        blank=True,
        verbose_name='Nutritional Info (English)',
        help_text='Nutritional information in English'
    )
    
    # Status flags
    is_featured = models.BooleanField(
        default=False,
        help_text='Whether this product should be featured on homepage'
    )
    is_available = models.BooleanField(
        default=True,
        help_text='Whether this product is available for sale'
    )
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS_CHOICES,
        default='in_stock',
        help_text='Current stock status'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-is_featured', 'name_en']
        indexes = [
            models.Index(fields=['name_zh']),
            models.Index(fields=['name_en']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['stock_status']),
        ]
    
    def __str__(self):
        return f"{self.name_zh} ({self.name_en})"
    
    def get_absolute_url(self):
        """Return URL for this product's detail page."""
        return reverse('shop:product_detail', kwargs={'slug': self.slug})
    
    @property
    def primary_image(self):
        """Get the primary image for this product."""
        return self.images.filter(is_primary=True).first()
    
    @property
    def formatted_price(self):
        """Return formatted price with TWD currency."""
        return f"NT$ {self.price:,.2f}"
    
    def get_stock_status_badge_class(self):
        """Return CSS class for stock status badge."""
        status_classes = {
            'in_stock': 'bg-green-100 text-green-800',
            'low_stock': 'bg-yellow-100 text-yellow-800',
            'out_of_stock': 'bg-red-100 text-red-800',
            'seasonal': 'bg-orange-100 text-orange-800',
        }
        return status_classes.get(self.stock_status, 'bg-gray-100 text-gray-800')


class ProductImage(models.Model):
    """Product image with optimization and bilingual alt text."""
    
    def upload_to_product_images(instance, filename):
        """Generate upload path for product images."""
        # Clean filename and organize by product slug
        name, ext = os.path.splitext(filename)
        return f'products/{instance.product.slug}/{instance.product.slug}_{instance.display_order}{ext}'
    
    # Relationships
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Product'
    )
    
    # Image field with processing
    image = ProcessedImageField(
        upload_to=upload_to_product_images,
        processors=[Transpose()],  # Auto-rotate based on EXIF
        format='JPEG',
        options={'quality': 85},
        verbose_name='Image'
    )
    
    # Image specifications for different sizes
    thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(150, 150)],
        format='JPEG',
        options={'quality': 80}
    )
    
    medium = ImageSpecField(
        source='image',
        processors=[ResizeToFit(400, 400)],
        format='JPEG',
        options={'quality': 85}
    )
    
    large = ImageSpecField(
        source='image',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90}
    )
    
    # Alt text for accessibility
    alt_text_zh = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Alt Text (Chinese)',
        help_text='Alternative text in Traditional Chinese for accessibility'
    )
    alt_text_en = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Alt Text (English)',
        help_text='Alternative text in English for accessibility'
    )
    
    # Display settings
    display_order = models.PositiveIntegerField(
        default=0,
        help_text='Order for displaying images (0 = first)'
    )
    is_primary = models.BooleanField(
        default=False,
        help_text='Whether this is the primary image for the product'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['product', 'display_order']),
            models.Index(fields=['is_primary']),
        ]
    
    def __str__(self):
        primary_text = " (Primary)" if self.is_primary else ""
        return f"{self.product.name_en} - Image {self.display_order}{primary_text}"
    
    def save(self, *args, **kwargs):
        """Ensure only one primary image per product."""
        if self.is_primary:
            # Set other images of the same product to not primary
            ProductImage.objects.filter(
                product=self.product, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class CompanyInfo(models.Model):
    """Company information with bilingual support and location data."""
    
    def upload_to_company_images(instance, filename):
        """Generate upload path for company images."""
        name, ext = os.path.splitext(filename)
        return f'company/hero_{name}{ext}'
    
    # Basic company info
    name_zh = models.CharField(
        max_length=200,
        verbose_name='Company Name (Chinese)',
        help_text='Company name in Traditional Chinese'
    )
    name_en = models.CharField(
        max_length=200,
        verbose_name='Company Name (English)',
        help_text='Company name in English'
    )
    
    # About sections
    about_zh = models.TextField(
        verbose_name='About (Chinese)',
        help_text='Company story and description in Traditional Chinese'
    )
    about_en = models.TextField(
        verbose_name='About (English)',
        help_text='Company story and description in English'
    )
    
    # Contact information
    address_zh = models.TextField(
        verbose_name='Address (Chinese)',
        help_text='Physical address in Traditional Chinese'
    )
    address_en = models.TextField(
        verbose_name='Address (English)',
        help_text='Physical address in English'
    )
    phone = models.CharField(
        max_length=20,
        help_text='Primary phone number'
    )
    email = models.EmailField(
        help_text='Primary email address'
    )
    
    # Location coordinates for maps
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        null=True, 
        blank=True,
        help_text='Latitude coordinate for Google Maps'
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        null=True, 
        blank=True,
        help_text='Longitude coordinate for Google Maps'
    )
    
    # Business hours
    business_hours_zh = models.TextField(
        verbose_name='Business Hours (Chinese)',
        help_text='Operating hours in Traditional Chinese'
    )
    business_hours_en = models.TextField(
        verbose_name='Business Hours (English)',
        help_text='Operating hours in English'
    )
    
    # Social media and messaging
    line_id = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='LINE ID',
        help_text='LINE messenger ID'
    )
    whatsapp = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name='WhatsApp',
        help_text='WhatsApp phone number'
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name='Facebook URL',
        help_text='Facebook page URL'
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name='Instagram URL',
        help_text='Instagram profile URL'
    )
    
    # Hero image
    hero_image = ProcessedImageField(
        upload_to=upload_to_company_images,
        processors=[Transpose()],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True,
        verbose_name='Hero Image',
        help_text='Main hero image for homepage and about page'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company Information'
        verbose_name_plural = 'Company Information'
    
    def __str__(self):
        return f"{self.name_zh} ({self.name_en})"
    
    @classmethod
    def get_company_info(cls):
        """Get the singleton company info object."""
        return cls.objects.first()
    
    def save(self, *args, **kwargs):
        """Ensure only one company info object exists."""
        if not self.pk and CompanyInfo.objects.exists():
            raise ValueError("Only one company info object is allowed.")
        super().save(*args, **kwargs)
