from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.shop.models import Category, Product, ProductImage, CompanyInfo


class CategoryModelTest(TestCase):
    """Test Category model functionality."""
    
    def test_category_creation(self):
        """Test basic category creation."""
        category = Category.objects.create(
            name_zh="牛肉",
            name_en="Beef",
            slug="beef",
            description_zh="新鮮牛肉",
            description_en="Fresh beef",
            display_order=1
        )
        
        self.assertEqual(category.name_zh, "牛肉")
        self.assertEqual(category.name_en, "Beef")
        self.assertEqual(category.slug, "beef")
        self.assertTrue(category.is_active)
        self.assertEqual(category.display_order, 1)
    
    def test_category_str_method(self):
        """Test string representation."""
        category = Category.objects.create(
            name_zh="豬肉",
            name_en="Pork",
            slug="pork"
        )
        self.assertEqual(str(category), "豬肉 (Pork)")
    
    def test_slug_validation(self):
        """Test slug format validation."""
        # Valid slug
        category = Category.objects.create(
            name_zh="雞肉",
            name_en="Chicken",
            slug="chicken-breast"
        )
        category.full_clean()  # Should not raise
        
        # Invalid slug with uppercase
        with self.assertRaises(ValidationError):
            category = Category(
                name_zh="雞肉",
                name_en="Chicken",
                slug="Chicken"
            )
            category.full_clean()
    
    def test_name_validation(self):
        """Test that at least one name is required."""
        # Both names empty should fail
        category = Category(slug="test")
        with self.assertRaises(ValidationError):
            category.clean()
        
        # One name is sufficient
        category = Category(name_zh="測試", slug="test")
        category.clean()  # Should not raise
        
        category = Category(name_en="Test", slug="test")
        category.clean()  # Should not raise
    
    def test_unique_slug(self):
        """Test slug uniqueness constraint."""
        Category.objects.create(
            name_zh="牛肉",
            name_en="Beef", 
            slug="beef"
        )
        
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name_zh="另一種牛肉",
                name_en="Another Beef",
                slug="beef"  # Duplicate slug
            )
    
    def test_ordering(self):
        """Test default ordering by display_order then name_en."""
        Category.objects.create(name_zh="豬肉", name_en="Pork", slug="pork", display_order=2)
        Category.objects.create(name_zh="牛肉", name_en="Beef", slug="beef", display_order=1)
        Category.objects.create(name_zh="雞肉", name_en="Chicken", slug="chicken", display_order=1)
        
        categories = list(Category.objects.all())
        self.assertEqual(categories[0].slug, "beef")
        self.assertEqual(categories[1].slug, "chicken")  # Same display_order, ordered by name_en
        self.assertEqual(categories[2].slug, "pork")
    
    def test_get_absolute_url(self):
        """Test URL generation."""
        category = Category.objects.create(
            name_zh="牛肉",
            name_en="Beef",
            slug="beef"
        )
        expected_url = "/products/?category=beef"  # Assuming this URL pattern
        # Note: This test assumes URL pattern exists - may need adjustment
        # when actual URL patterns are implemented


class ProductModelTest(TestCase):
    """Test Product model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name_zh="牛肉",
            name_en="Beef",
            slug="beef"
        )
    
    def test_product_creation(self):
        """Test basic product creation."""
        product = Product.objects.create(
            category=self.category,
            name_zh="牛排",
            name_en="Beef Steak",
            slug="beef-steak",
            description_zh="優質牛排",
            description_en="Premium beef steak",
            price=Decimal('299.50'),
            unit="kg",
            weight_grams=1000
        )
        
        self.assertEqual(product.name_zh, "牛排")
        self.assertEqual(product.name_en, "Beef Steak")
        self.assertEqual(product.price, Decimal('299.50'))
        self.assertEqual(product.stock_status, 'in_stock')
        self.assertFalse(product.is_featured)
        self.assertTrue(product.is_available)
    
    def test_product_str_method(self):
        """Test string representation."""
        product = Product.objects.create(
            category=self.category,
            name_zh="牛排",
            name_en="Beef Steak",
            slug="beef-steak",
            description_zh="優質牛排",
            description_en="Premium beef steak",
            price=Decimal('299.50')
        )
        self.assertEqual(str(product), "牛排 (Beef Steak)")
    
    def test_formatted_price(self):
        """Test price formatting."""
        product = Product.objects.create(
            category=self.category,
            name_zh="牛排",
            name_en="Beef Steak",
            slug="beef-steak",
            description_zh="優質牛排",
            description_en="Premium beef steak",
            price=Decimal('1234.56')
        )
        self.assertEqual(product.formatted_price, "NT$ 1,234.56")
    
    def test_stock_status_badge_class(self):
        """Test stock status badge CSS classes."""
        product = Product.objects.create(
            category=self.category,
            name_zh="牛排",
            name_en="Beef Steak",
            slug="beef-steak",
            description_zh="優質牛排",
            description_en="Premium beef steak",
            price=Decimal('299.50'),
            stock_status='in_stock'
        )
        
        self.assertEqual(
            product.get_stock_status_badge_class(), 
            'bg-green-100 text-green-800'
        )
        
        product.stock_status = 'out_of_stock'
        self.assertEqual(
            product.get_stock_status_badge_class(),
            'bg-red-100 text-red-800'
        )
    
    def test_product_ordering(self):
        """Test default ordering by is_featured then name_en."""
        Product.objects.create(
            category=self.category,
            name_zh="普通牛排",
            name_en="Regular Steak",
            slug="regular-steak",
            description_zh="普通牛排",
            description_en="Regular steak",
            price=Decimal('199.50'),
            is_featured=False
        )
        
        Product.objects.create(
            category=self.category,
            name_zh="特級牛排",
            name_en="Premium Steak",
            slug="premium-steak",
            description_zh="特級牛排",
            description_en="Premium steak",
            price=Decimal('399.50'),
            is_featured=True
        )
        
        products = list(Product.objects.all())
        self.assertEqual(products[0].slug, "premium-steak")  # Featured first
        self.assertEqual(products[1].slug, "regular-steak")


class ProductImageModelTest(TestCase):
    """Test ProductImage model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name_zh="牛肉",
            name_en="Beef",
            slug="beef"
        )
        self.product = Product.objects.create(
            category=self.category,
            name_zh="牛排",
            name_en="Beef Steak",
            slug="beef-steak",
            description_zh="優質牛排",
            description_en="Premium beef steak",
            price=Decimal('299.50')
        )
    
    def test_product_image_str(self):
        """Test string representation."""
        image = ProductImage.objects.create(
            product=self.product,
            display_order=1,
            alt_text_zh="牛排圖片",
            alt_text_en="Beef steak image"
        )
        expected = "Beef Steak - Image 1"
        self.assertEqual(str(image), expected)
        
        # Test primary image
        image.is_primary = True
        image.save()
        expected = "Beef Steak - Image 1 (Primary)"
        self.assertEqual(str(image), expected)
    
    def test_primary_image_uniqueness(self):
        """Test that only one image can be primary per product."""
        # Create first image as primary
        image1 = ProductImage.objects.create(
            product=self.product,
            display_order=1,
            is_primary=True
        )
        
        # Create second image as primary
        image2 = ProductImage.objects.create(
            product=self.product,
            display_order=2,
            is_primary=True
        )
        
        # Refresh from database
        image1.refresh_from_db()
        
        # First image should no longer be primary
        self.assertFalse(image1.is_primary)
        self.assertTrue(image2.is_primary)
    
    def test_primary_image_property(self):
        """Test product's primary_image property."""
        # No images yet
        self.assertIsNone(self.product.primary_image)
        
        # Add non-primary image
        image1 = ProductImage.objects.create(
            product=self.product,
            display_order=1,
            is_primary=False
        )
        self.assertIsNone(self.product.primary_image)
        
        # Add primary image
        image2 = ProductImage.objects.create(
            product=self.product,
            display_order=2,
            is_primary=True
        )
        self.assertEqual(self.product.primary_image, image2)


class CompanyInfoModelTest(TestCase):
    """Test CompanyInfo model functionality."""
    
    def test_company_info_creation(self):
        """Test basic company info creation."""
        company = CompanyInfo.objects.create(
            name_zh="明昌肉舖",
            name_en="Ming Chang Meat Shop",
            about_zh="花蓮優質肉舖",
            about_en="Premium meat shop in Hualien",
            address_zh="花蓮市中正路123號",
            address_en="123 Zhongzheng Rd, Hualien City",
            phone="03-1234567",
            email="info@mingchang.com.tw",
            business_hours_zh="週一至週六 8:00-18:00",
            business_hours_en="Mon-Sat 8:00-18:00"
        )
        
        self.assertEqual(company.name_zh, "明昌肉舖")
        self.assertEqual(company.name_en, "Ming Chang Meat Shop")
        self.assertEqual(company.phone, "03-1234567")
    
    def test_company_info_str_method(self):
        """Test string representation."""
        company = CompanyInfo.objects.create(
            name_zh="明昌肉舖",
            name_en="Ming Chang Meat Shop",
            about_zh="花蓮優質肉舖",
            about_en="Premium meat shop in Hualien",
            address_zh="花蓮市中正路123號",
            address_en="123 Zhongzheng Rd, Hualien City",
            phone="03-1234567",
            email="info@mingchang.com.tw",
            business_hours_zh="週一至週六 8:00-18:00",
            business_hours_en="Mon-Sat 8:00-18:00"
        )
        self.assertEqual(str(company), "明昌肉舖 (Ming Chang Meat Shop)")
    
    def test_singleton_constraint(self):
        """Test that only one company info object can exist."""
        # Create first company info
        CompanyInfo.objects.create(
            name_zh="明昌肉舖",
            name_en="Ming Chang Meat Shop",
            about_zh="花蓮優質肉舖",
            about_en="Premium meat shop in Hualien",
            address_zh="花蓮市中正路123號",
            address_en="123 Zhongzheng Rd, Hualien City",
            phone="03-1234567",
            email="info@mingchang.com.tw",
            business_hours_zh="週一至週六 8:00-18:00",
            business_hours_en="Mon-Sat 8:00-18:00"
        )
        
        # Attempting to create second should fail
        with self.assertRaises(ValueError):
            CompanyInfo.objects.create(
                name_zh="另一家店",
                name_en="Another Shop",
                about_zh="另一家店",
                about_en="Another shop",
                address_zh="另一個地址",
                address_en="Another address",
                phone="03-7654321",
                email="info@another.com.tw",
                business_hours_zh="週一至週六 9:00-17:00",
                business_hours_en="Mon-Sat 9:00-17:00"
            )
    
    def test_get_company_info_classmethod(self):
        """Test get_company_info class method."""
        # No company info yet
        self.assertIsNone(CompanyInfo.get_company_info())
        
        # Create company info
        company = CompanyInfo.objects.create(
            name_zh="明昌肉舖",
            name_en="Ming Chang Meat Shop",
            about_zh="花蓮優質肉舖",
            about_en="Premium meat shop in Hualien",
            address_zh="花蓮市中正路123號",
            address_en="123 Zhongzheng Rd, Hualien City",
            phone="03-1234567",
            email="info@mingchang.com.tw",
            business_hours_zh="週一至週六 8:00-18:00",
            business_hours_en="Mon-Sat 8:00-18:00"
        )
        
        # Should return the company info
        self.assertEqual(CompanyInfo.get_company_info(), company)
