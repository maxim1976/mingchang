from apps.shop.models import Product
from django.core.files.storage import default_storage

p = Product.objects.first()
if p:
    print(f'Product: {p.name_en}')
    img = p.primary_image
    if img:
        print(f'Image path: {img.image.name}')
        print(f'Source exists: {default_storage.exists(img.image.name)}')
        print(f'Has medium: {hasattr(img, "medium")}')
        try:
            print(f'Medium URL: {img.medium.url}')
        except Exception as e:
            print(f'Error getting medium URL: {e}')
    else:
        print('No primary image')
else:
    print('No products')
