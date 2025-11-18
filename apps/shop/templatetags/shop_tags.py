"""
Custom template tags for Shop MingChang
"""

from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter(name='get_translated_field')
def get_translated_field(obj, field_name):
    """
    Get bilingual field value with format: "中文 English"
    Usage: {{ product|get_translated_field:"name" }}
    Returns: "牛肉 Beef"
    """
    zh_value = getattr(obj, f"{field_name}_zh", "")
    en_value = getattr(obj, f"{field_name}_en", "")
    
    if zh_value and en_value:
        return f"{zh_value} {en_value}"
    elif zh_value:
        return zh_value
    elif en_value:
        return en_value
    return ""


@register.filter(name='format_twd')
def format_twd(value):
    """
    Format price in Taiwan Dollar with comma separators and NT$ prefix
    Usage: {{ product.price|format_twd }}
    Returns: "NT$ 1,234.56"
    """
    if value is None:
        return "NT$ 0.00"
    
    try:
        # Convert to Decimal for precise handling
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Format with comma separators and 2 decimal places
        formatted = "{:,.2f}".format(value)
        return f"NT$ {formatted}"
    except (ValueError, TypeError, InvalidOperation):
        return "NT$ 0.00"


@register.simple_tag
def bilingual_text(zh_text, en_text, css_class="bilingual"):
    """
    Generate bilingual HTML span elements
    Usage: {% bilingual_text "產品" "Products" %}
    Returns: <div class="bilingual"><span class="zh">產品</span><span class="en">Products</span></div>
    """
    return f'<div class="{css_class}"><span class="zh">{zh_text}</span><span class="en">{en_text}</span></div>'


@register.filter
def weight_display(weight_grams):
    """
    Display weight in appropriate unit (g or kg).
    
    Usage: {{ product.weight_grams|weight_display }}
    """
    if not weight_grams:
        return ""
    
    if weight_grams >= 1000:
        kg = weight_grams / 1000
        if kg == int(kg):  # Is whole number
            return f"{int(kg)} kg"
        else:
            return f"{kg:.1f} kg"
    else:
        return f"{weight_grams} g"


@register.filter
def safe_image_url(image_spec):
    """
    Safely get image URL, return empty string if file doesn't exist.
    
    Usage: {{ image.large|safe_image_url }}
    """
    try:
        if image_spec and hasattr(image_spec, 'url'):
            # For ImageSpecField, just return the URL
            # ImageKit will generate the file on-demand when accessed
            return image_spec.url
        return ""
    except Exception:
        return ""

