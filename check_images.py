#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.shop.models import Product, ProductImage

print('=' * 50)
print('DATABASE CHECK')
print('=' * 50)
print(f'Total Products: {Product.objects.count()}')
print(f'Total ProductImages: {ProductImage.objects.count()}')
print()

print('Product Details:')
print('-' * 50)
for product in Product.objects.all():
    print(f'\nProduct: {product.name_en} (slug: {product.slug})')
    print(f'  Is Featured: {product.is_featured}')
    print(f'  Primary Image: {product.primary_image}')
    print(f'  Total Images: {product.images.count()}')
    
    for img in product.images.all():
        print(f'    - Image: {img.image.name}')
        print(f'      Is Primary: {img.is_primary}')
        print(f'      File Exists: {os.path.exists(img.image.path)}')

print()
print('=' * 50)
