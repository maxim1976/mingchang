from django import forms
from django.core.validators import RegexValidator
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    """Contact form for customer inquiries."""
    
    # Phone validator for Taiwan phone numbers
    phone_validator = RegexValidator(
        regex=r'^[\d\-\s\(\)\+]+$',
        message='請輸入有效的電話號碼 Please enter a valid phone number'
    )
    
    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'email', 'subject', 'message', 'product_name', 'language_preference']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize form fields
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': '您的姓名 Your Name'
        })
        
        self.fields['phone'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': '手機號碼 Phone Number (例如: 0912-345-678)'
        })
        self.fields['phone'].validators.append(self.phone_validator)
        
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': 'email@example.com'
        })
        
        self.fields['subject'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': '主旨 Subject (選填 Optional)'
        })
        
        self.fields['product_name'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'placeholder': '詢問的產品名稱 Product Name (選填 Optional)'
        })
        
        self.fields['message'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'rows': 5,
            'placeholder': '請輸入您的詢問內容... Please enter your inquiry...'
        })
        
        self.fields['language_preference'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent'
        })
        
        # Set field labels with bilingual support
        self.fields['name'].label = '姓名 Name *'
        self.fields['phone'].label = '電話 Phone *'
        self.fields['email'].label = '電子信箱 Email *'
        self.fields['subject'].label = '主旨 Subject'
        self.fields['product_name'].label = '詢問產品 Product of Interest'
        self.fields['message'].label = '詢問內容 Message *'
        self.fields['language_preference'].label = '語言偏好 Language Preference'
        
    def clean_phone(self):
        """Validate and clean phone number."""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove all non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, phone))
            
            # Taiwan phone number validation
            if len(digits_only) < 8 or len(digits_only) > 15:
                raise forms.ValidationError(
                    '電話號碼長度不正確 Phone number length is incorrect'
                )
            
            # Taiwan mobile number pattern (09xxxxxxxx)
            if digits_only.startswith('09') and len(digits_only) == 10:
                return phone
            
            # Taiwan landline pattern (area code + number)
            if len(digits_only) >= 8 and len(digits_only) <= 10:
                return phone
            
            # International format
            if digits_only.startswith('886') or phone.startswith('+886'):
                return phone
                
            raise forms.ValidationError(
                '請輸入有效的台灣電話號碼 Please enter a valid Taiwan phone number'
            )
        
        return phone
    
    def clean_message(self):
        """Validate message length."""
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError(
                '詢問內容至少需要10個字符 Message must be at least 10 characters long'
            )
        return message


class ProductInquiryForm(ContactForm):
    """Specialized form for product-specific inquiries."""
    
    def __init__(self, product=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if product:
            # Pre-fill product information
            self.fields['product_name'].initial = f"{product.name_zh} ({product.name_en})"
            self.fields['subject'].initial = f"詢問產品: {product.name_zh} Product Inquiry: {product.name_en}"
            
            # Make product field readonly since it's pre-filled
            self.fields['product_name'].widget.attrs['readonly'] = True
            self.fields['product_name'].widget.attrs['class'] += ' bg-gray-50'
            
            # Update message placeholder
            self.fields['message'].widget.attrs['placeholder'] = (
                f'您好，我想詢問關於「{product.name_zh}」的相關資訊...\n\n'
                f'Hello, I would like to inquire about "{product.name_en}"...'
            )