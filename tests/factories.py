"""
Factory classes for generating test data using factory_boy
"""

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from decimal import Decimal

fake = Faker(['zh_TW', 'en_US'])


class CategoryFactory(DjangoModelFactory):
    """Factory for Category model"""
    
    class Meta:
        model = 'shop.Category'
    
    name_zh = factory.Sequence(lambda n: f"類別{n}")
    name_en = factory.Sequence(lambda n: f"Category{n}")
    slug = factory.Sequence(lambda n: f"category-{n}")
    description_zh = factory.Faker('text', max_nb_chars=200, locale='zh_TW')
    description_en = factory.Faker('text', max_nb_chars=200)
    display_order = factory.Sequence(lambda n: n)
    is_active = True


class ProductFactory(DjangoModelFactory):
    """Factory for Product model"""
    
    class Meta:
        model = 'shop.Product'
    
    category = factory.SubFactory(CategoryFactory)
    name_zh = factory.Faker('word', locale='zh_TW')
    name_en = factory.Faker('word')
    slug = factory.Sequence(lambda n: f"product-{n}")
    description_zh = factory.Faker('text', max_nb_chars=500, locale='zh_TW')
    description_en = factory.Faker('text', max_nb_chars=500)
    price = factory.LazyFunction(lambda: Decimal(fake.random_int(min=100, max=2000)))
    unit = factory.Iterator(['kg', '斤', 'piece', 'pack'])
    weight_grams = factory.Faker('random_int', min=100, max=5000)
    origin_zh = factory.Faker('city', locale='zh_TW')
    origin_en = factory.Faker('city')
    is_featured = factory.Faker('boolean', chance_of_getting_true=30)
    is_available = True
    stock_status = factory.Iterator(['in_stock', 'low_stock', 'out_of_stock', 'seasonal'])
    display_order = factory.Sequence(lambda n: n)


class ProductImageFactory(DjangoModelFactory):
    """Factory for ProductImage model"""
    
    class Meta:
        model = 'shop.ProductImage'
    
    product = factory.SubFactory(ProductFactory)
    alt_text_zh = factory.Faker('sentence', nb_words=3, locale='zh_TW')
    alt_text_en = factory.Faker('sentence', nb_words=3)
    display_order = factory.Sequence(lambda n: n)
    is_primary = False


class CompanyInfoFactory(DjangoModelFactory):
    """Factory for CompanyInfo model"""
    
    class Meta:
        model = 'shop.CompanyInfo'
    
    name_zh = "明昌肉鋪"
    name_en = "MingChang Meat Shop"
    about_zh = factory.Faker('text', max_nb_chars=1000, locale='zh_TW')
    about_en = factory.Faker('text', max_nb_chars=1000)
    address_zh = "花蓮市中正路123號"
    address_en = "No. 123, Zhongzheng Rd, Hualien City"
    phone = "03-1234567"
    email = "info@mingchang-meat.com"
    latitude = Decimal("23.9871")
    longitude = Decimal("121.6015")
    business_hours_zh = "週一至週六 08:00-18:00"
    business_hours_en = "Mon-Sat 08:00-18:00"
    line_id = "@mingchang"
    whatsapp = "+886912345678"
    facebook_url = "https://facebook.com/mingchang"


class ContactInquiryFactory(DjangoModelFactory):
    """Factory for ContactInquiry model"""
    
    class Meta:
        model = 'contact.ContactInquiry'
    
    name = factory.Faker('name', locale='zh_TW')
    phone = factory.Faker('phone_number', locale='zh_TW')
    email = factory.Faker('email')
    message = factory.Faker('text', max_nb_chars=500, locale='zh_TW')
    language = factory.Iterator(['zh-hant', 'en'])
    is_read = False
