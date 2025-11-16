"""
Pytest configuration and fixtures
"""

import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def client():
    """Django test client"""
    return Client()


@pytest.fixture
def admin_user(db):
    """Admin user for testing admin interface"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, admin_user):
    """Client logged in as admin"""
    client.force_login(admin_user)
    return client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass


@pytest.fixture
def category_factory():
    """Category factory fixture"""
    from tests.factories import CategoryFactory
    return CategoryFactory


@pytest.fixture
def product_factory():
    """Product factory fixture"""
    from tests.factories import ProductFactory
    return ProductFactory


@pytest.fixture
def product_image_factory():
    """ProductImage factory fixture"""
    from tests.factories import ProductImageFactory
    return ProductImageFactory


@pytest.fixture
def company_info_factory():
    """CompanyInfo factory fixture"""
    from tests.factories import CompanyInfoFactory
    return CompanyInfoFactory


@pytest.fixture
def contact_inquiry_factory():
    """ContactInquiry factory fixture"""
    from tests.factories import ContactInquiryFactory
    return ContactInquiryFactory
