#!/usr/bin/env python
"""Download real product images from Unsplash"""
import urllib.request
import os

# Create temp directory
os.makedirs('media/products/temp', exist_ok=True)

# Product images from Unsplash (free to use)
images = [
    ('https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=800&q=80', '1855-prime-bone-in-ribeye.jpg'),
    ('https://images.unsplash.com/photo-1588168333986-5078d3ae3976?w=800&q=80', 'angus-beef-steak.jpg'),
    ('https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=800&q=80', 'black-pork-belly.jpg'),
    ('https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=800&q=80', 'free-range-chicken.jpg'),
]

print("Downloading product images...")
for url, filename in images:
    try:
        filepath = os.path.join('media', 'products', 'temp', filename)
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath)
        print(f"  ✓ Downloaded {filename} ({size:,} bytes)")
    except Exception as e:
        print(f"  ✗ Failed to download {filename}: {e}")

print("\nDone! Images saved to media/products/temp/")
print("Now run: python manage.py shell < update_product_images.py")
