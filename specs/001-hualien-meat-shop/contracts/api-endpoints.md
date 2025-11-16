# API Endpoints & Contracts: Hualien Meat E-Shop

**Feature**: 001-hualien-meat-shop  
**Date**: 2025-11-12  
**Purpose**: Define URL routes, view contracts, and HTMX interactions

## Overview

This document defines the URL structure and view contracts for the Hualien Meat E-Shop. Phase 1 uses Django template views with HTMX for dynamic interactions. Phase 2 adds REST API endpoints for cart/checkout operations and ECPay webhooks.

---

## Phase 1: Template Views (MVP)

### URL Structure

**Base URL**: `https://mingchang-meat.railway.app` (or custom domain)

**Language Prefix**: Optional `/<lang>/` where `lang` = `zh-hant` or `en`
- Examples: `/zh-hant/products/`, `/en/products/`, or `/products/` (uses cookie/browser language)

---

### 1. Homepage

**URL**: `/` or `/<lang>/`  
**View**: `apps.shop.views.HomeView`  
**Method**: GET  
**Template**: `templates/shop/home.html`

**Purpose**: Display shop introduction, featured products, and navigation.

**Response Data:**
```python
{
    'company': CompanyInfo,           # Business name, hero image, about snippet
    'featured_products': List[Product],  # Up to 6 featured products
    'categories': List[Category],     # All active categories for navigation
    'language': str                   # Current language code
}
```

**HTMX Enhancements**: None (static page)

**SEO**:
- Title: `{shop_name} - {tagline}`
- Meta description: Company about text (first 160 chars)
- Canonical URL: `/{lang}/`

---

### 2. Product Listing (Category View)

**URL**: `/products/` or `/<lang>/products/`  
**View**: `apps.shop.views.ProductListView`  
**Method**: GET  
**Template**: `templates/shop/product_list.html`

**Purpose**: Display all products, optionally filtered by category.

**Query Parameters:**
- `category` (optional): Category slug (e.g., `?category=beef`)
- `search` (optional): Search term for product name (e.g., `?search=steak`)
- `sort` (optional): Sort order (`price-asc`, `price-desc`, `name`, `featured`)

**Response Data:**
```python
{
    'products': Paginated[Product],   # 12 products per page
    'categories': List[Category],     # All categories for filter
    'current_category': Category,     # Selected category (if filtered)
    'search_query': str,              # Search term (if searched)
    'sort_option': str,               # Current sort
    'page_obj': Page                  # Pagination object
}
```

**HTMX Enhancements**:
- **Category Filter**: `hx-get="/products/?category={slug}" hx-target="#product-grid" hx-push-url="true"`
  - Replaces product grid without full page reload
- **Search**: `hx-get="/products/?search={query}" hx-trigger="keyup changed delay:500ms"`
  - Live search with debounce
- **Pagination**: `hx-get="/products/?page={n}" hx-target="#product-grid" hx-swap="outerHTML"`

**Performance**:
- Paginate 12 products per page
- Eager load product images (only primary image)
- Cache category list (1 hour)

**SEO**:
- Title: `{category_name} Products - {shop_name}`
- Meta description: Category description or "Browse our selection of {category}"
- Canonical URL: `/{lang}/products/?category={slug}`

---

### 3. Product Detail

**URL**: `/products/<slug>/` or `/<lang>/products/<slug>/`  
**View**: `apps.shop.views.ProductDetailView`  
**Method**: GET  
**Template**: `templates/shop/product_detail.html`

**Purpose**: Display full product information with images, description, pricing.

**Response Data:**
```python
{
    'product': Product,               # Full product details
    'images': List[ProductImage],     # All product images, sorted by display_order
    'related_products': List[Product], # 4 products from same category
    'primary_image': ProductImage     # Main display image
}
```

**HTMX Enhancements**:
- **Image Gallery**: `hx-get="/products/<slug>/image/{id}/" hx-target="#main-image"`
  - Switch main display image on thumbnail click
- **Add to Cart (Phase 2)**: `hx-post="/cart/add/" hx-target="#cart-count"`

**Performance**:
- Lazy load non-primary images
- Cache product data (15 minutes)
- Preload related products query

**SEO**:
- Title: `{product_name} - {shop_name}`
- Meta description: Product description (first 160 chars)
- Canonical URL: `/{lang}/products/{slug}/`
- Open Graph tags: Product name, image, price
- Structured data: Product schema (Schema.org)

---

### 4. About & Location

**URL**: `/about/` or `/<lang>/about/`  
**View**: `apps.shop.views.AboutView`  
**Method**: GET  
**Template**: `templates/shop/about.html`

**Purpose**: Display company information, story, location with map.

**Response Data:**
```python
{
    'company': CompanyInfo,           # Full business details
    'google_maps_embed_url': str     # Google Maps embed URL with lat/lng
}
```

**HTMX Enhancements**: None (static page)

**Google Maps Integration**:
```html
<iframe 
  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d{zoom}!2d{lng}!3d{lat}"
  width="100%" 
  height="450" 
  style="border:0;" 
  allowfullscreen="" 
  loading="lazy">
</iframe>
```

**SEO**:
- Title: `About Us - {shop_name}`
- Meta description: Company about text
- Canonical URL: `/{lang}/about/`
- Structured data: Local Business schema

---

### 5. Contact

**URL**: `/contact/` or `/<lang>/contact/`  
**View**: `apps.contact.views.ContactView`  
**Method**: GET, POST  
**Template**: `templates/contact/contact.html`

**Purpose**: Display contact form and submit inquiries.

**GET Response Data:**
```python
{
    'form': ContactForm,              # Empty form
    'company': CompanyInfo            # Contact details (phone, email, social)
}
```

**POST Request (Form Data):**
```python
{
    'name': str,                      # Required, max 100 chars
    'phone': str,                     # Required, Taiwan phone format
    'email': str,                     # Required, valid email
    'subject': str,                   # Optional, max 200 chars
    'message': str                    # Required, 10-2000 chars
}
```

**POST Response (Success):**
- HTMX: Return success message partial
- Traditional: Redirect to `/contact/success/`

**POST Response (Validation Error):**
```python
{
    'form': ContactForm,              # Form with errors
    'errors': Dict[str, List[str]]    # Field-specific errors
}
```

**HTMX Enhancements**:
- **Form Submit**: `hx-post="/contact/" hx-target="#contact-form" hx-swap="outerHTML"`
  - Submit without page reload
  - Show inline validation errors
  - Display success message in place

**Side Effects**:
1. Create `ContactInquiry` record in database
2. Send confirmation email to customer
3. Send notification email to shop owner (config.email)

**Validation Rules**:
- Name: 2-100 characters
- Phone: Match Taiwan phone pattern `^(\+886|0)[0-9-]{9,15}$`
- Email: Valid email format
- Message: 10-2000 characters
- Rate limit: Max 5 submissions per IP per hour (spam prevention)

**SEO**:
- Title: `Contact Us - {shop_name}`
- Meta description: "Get in touch with {shop_name} in Hualien..."
- Canonical URL: `/{lang}/contact/`

---

### 6. Language Switcher

**URL**: `/set-language/`  
**View**: `django.views.i18n.set_language`  
**Method**: POST  
**Template**: None (redirects)

**Purpose**: Switch interface language (Traditional Chinese ↔ English).

**POST Request:**
```python
{
    'language': str,                  # 'zh-hant' or 'en'
    'next': str                       # Redirect URL after switch
}
```

**Response**:
- Set `django_language` cookie
- Redirect to `next` URL with new language prefix

**HTMX Enhancement**:
- **Language Toggle**: `hx-post="/set-language/" hx-vals='{"language": "en", "next": "/en/"}' hx-swap="none"`
  - Switch language, then `window.location.href = nextUrl`

---

## Phase 2: REST API Endpoints (Future)

### 7. Add to Cart (AJAX)

**URL**: `/api/cart/add/`  
**View**: `apps.orders.views.CartAddView`  
**Method**: POST  
**Content-Type**: `application/json`

**Purpose**: Add product to shopping cart (HTMX AJAX call).

**Request Body:**
```json
{
    "product_id": 123,
    "quantity": 2
}
```

**Response (Success - 200):**
```json
{
    "success": true,
    "cart_count": 5,              // Total items in cart
    "cart_total": "1250.00",      // Cart total in TWD
    "message": "Product added to cart"
}
```

**Response (Error - 400):**
```json
{
    "success": false,
    "error": "Product out of stock",
    "errors": {
        "quantity": ["Exceeds available stock"]
    }
}
```

**Side Effects**:
- Create/update `CartItem` for session
- Update `Cart.updated_at`

**Validation**:
- Product exists and `is_available=True`
- Quantity > 0 and <= 999
- Stock available (if stock tracking enabled)

---

### 8. View Cart

**URL**: `/cart/` or `/<lang>/cart/`  
**View**: `apps.orders.views.CartView`  
**Method**: GET  
**Template**: `templates/orders/cart.html`

**Purpose**: Display shopping cart contents.

**Response Data:**
```python
{
    'cart': Cart,
    'cart_items': List[CartItem],     # With product details
    'subtotal': Decimal,              # Sum of all items
    'delivery_fee': Decimal,          # Calculated based on total
    'total': Decimal                  # Subtotal + delivery_fee
}
```

**HTMX Enhancements**:
- **Update Quantity**: `hx-post="/api/cart/update/{item_id}/" hx-target="#cart-item-{id}"`
- **Remove Item**: `hx-delete="/api/cart/remove/{item_id}/" hx-target="#cart-item-{id}" hx-swap="outerHTML"`

---

### 9. Checkout

**URL**: `/checkout/` or `/<lang>/checkout/`  
**View**: `apps.orders.views.CheckoutView`  
**Method**: GET, POST  
**Template**: `templates/orders/checkout.html`

**Purpose**: Collect delivery information and initiate payment.

**GET Response Data:**
```python
{
    'form': CheckoutForm,             # Delivery details form
    'cart_items': List[CartItem],
    'total': Decimal
}
```

**POST Request (Form Data):**
```python
{
    'customer_name': str,
    'customer_phone': str,
    'customer_email': str,
    'delivery_address_zh': str,
    'delivery_address_en': str,       # Optional
    'delivery_date_preference': date,
    'delivery_time_preference': str,
    'delivery_notes': str,            # Optional
    'payment_method': str             # 'credit_card', 'atm', 'cvs'
}
```

**POST Response (Success):**
- Create `Order` and `OrderItem` records
- Create `PaymentTransaction` record
- Redirect to ECPay payment page
- Return ECPay payment form HTML

**Validation**:
- All required fields present
- Cart not empty
- Products still available
- Phone/email valid format

---

### 10. ECPay Webhook (Payment Callback)

**URL**: `/api/payment/ecpay/callback/`  
**View**: `apps.orders.views.ECPayCallbackView`  
**Method**: POST  
**Content-Type**: `application/x-www-form-urlencoded`

**Purpose**: Receive payment confirmation from ECPay.

**Request Body (ECPay sends):**
```python
{
    'MerchantID': str,
    'MerchantTradeNo': str,           # Our order_number
    'RtnCode': int,                   # 1 = success
    'RtnMsg': str,
    'TradeNo': str,                   # ECPay transaction ID
    'TradeAmt': int,
    'PaymentDate': str,
    'PaymentType': str,
    'CheckMacValue': str              # Security hash
}
```

**Response (Required by ECPay):**
```
1|OK
```

**Side Effects**:
1. Verify `CheckMacValue` signature
2. Update `Order.payment_status` to 'paid'
3. Update `PaymentTransaction.status` to 'success'
4. Send order confirmation email to customer
5. Send order notification email to shop owner

**Security**:
- Verify CheckMacValue matches computed hash
- Log all callback attempts (success and failure)
- Idempotent processing (handle duplicate callbacks)

---

### 11. Order Confirmation

**URL**: `/orders/<order_number>/` or `/<lang>/orders/<order_number>/`  
**View**: `apps.orders.views.OrderDetailView`  
**Method**: GET  
**Template**: `templates/orders/order_confirmation.html`

**Purpose**: Display order confirmation after successful payment.

**Response Data:**
```python
{
    'order': Order,                   # Full order details
    'order_items': List[OrderItem],   # Ordered products
    'payment': PaymentTransaction     # Payment status
}
```

**Access Control**:
- No authentication required (order_number acts as token)
- Rate limit lookups to prevent brute force

---

## HTMX Interaction Patterns

### Pattern 1: Partial Updates (Product Grid)

**Trigger**: Category filter click

```html
<button 
  hx-get="/products/?category=beef" 
  hx-target="#product-grid" 
  hx-push-url="true"
  class="filter-btn">
  牛肉 Beef
</button>
```

**Response**: HTML fragment
```html
<div id="product-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4">
  <!-- Updated product cards -->
</div>
```

---

### Pattern 2: Form Submission (Contact)

**Trigger**: Form submit

```html
<form 
  hx-post="/contact/" 
  hx-target="#contact-form" 
  hx-swap="outerHTML">
  <!-- Form fields -->
  <button type="submit">Send Message</button>
</form>
```

**Success Response**: Success message HTML
```html
<div class="success-message">
  <p>Thank you! We'll respond within 24 hours.</p>
</div>
```

**Error Response**: Form with errors
```html
<form id="contact-form" ...>
  <input name="email" class="error" />
  <span class="error-msg">Invalid email format</span>
</form>
```

---

### Pattern 3: Loading States

**HTMX Indicators**: Show spinner during requests

```html
<button hx-post="/cart/add/" class="htmx-indicator">
  <span class="spinner hidden">⏳</span>
  <span class="label">Add to Cart</span>
</button>
```

CSS:
```css
.htmx-request .spinner { display: inline-block; }
.htmx-request .label { display: none; }
```

---

## URL Routing Summary

**Phase 1 (MVP):**

| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/` | HomeView | Homepage |
| `/products/` | ProductListView | Product catalog |
| `/products/<slug>/` | ProductDetailView | Product details |
| `/about/` | AboutView | Company info & location |
| `/contact/` | ContactView | Contact form |
| `/set-language/` | set_language | Language switcher |
| `/admin/` | Django Admin | Owner product management |

**Phase 2 (Orders):**

| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/cart/` | CartView | View cart |
| `/api/cart/add/` | CartAddView | Add to cart (AJAX) |
| `/api/cart/update/<id>/` | CartUpdateView | Update quantity (AJAX) |
| `/api/cart/remove/<id>/` | CartRemoveView | Remove item (AJAX) |
| `/checkout/` | CheckoutView | Checkout form |
| `/orders/<number>/` | OrderDetailView | Order confirmation |
| `/api/payment/ecpay/callback/` | ECPayCallbackView | ECPay webhook |

---

## Test Coverage Requirements

**Contract Tests (pytest):**
1. All URL patterns resolve correctly
2. GET requests return 200 for valid URLs
3. POST requests validate input correctly
4. HTMX partial responses return correct HTML fragments
5. Language switching persists across requests
6. ECPay webhook signature validation

**Integration Tests (Playwright):**
1. Homepage loads with featured products
2. Product listing filters by category
3. Product detail displays images and description
4. Contact form submission sends email
5. Language toggle switches all content
6. Mobile responsive layout (320px, 768px, 1024px)

**Constitution Compliance**: >80% test coverage required ✅

---

## Performance Targets

**Page Load Times:**
- Homepage: <1.5s FCP, <3s TTI
- Product listing: <2s with 12 products
- Product detail: <1.8s with images

**API Response Times:**
- Product listing: <200ms (cached)
- Product detail: <150ms (cached)
- Contact form submit: <500ms
- Cart add (Phase 2): <100ms

**Caching Strategy:**
- Categories: 1 hour (rarely change)
- Product listings: 15 minutes
- Product details: 15 minutes
- Company info: 1 hour
- Static files: 1 year (versioned)

---

## Security Considerations

**CSRF Protection:**
- All POST requests require CSRF token
- Django middleware enforces CSRF validation

**Rate Limiting:**
- Contact form: 5 submissions per IP per hour
- Order lookups: 10 per IP per minute
- ECPay webhook: IP whitelist only

**Input Validation:**
- All form inputs sanitized
- Product search: Prevent SQL injection via ORM
- File uploads: Image type validation, max 5MB

**HTTPS:**
- Enforce HTTPS in production (Railway provides cert)
- Set `SECURE_SSL_REDIRECT=True`
- Use `SECURE_HSTS_SECONDS=31536000`

---

## Constitution Compliance Check

**Phase 1 Contracts** ✅

- **Code Quality**: RESTful URL patterns, single responsibility per view
- **Test-First**: Contract tests defined before implementation
- **UX Consistency**: HTMX ensures smooth interactions, no page flicker
- **Performance**: Caching strategy meets response time requirements

**Ready for Quickstart**: Development workflow documentation can now proceed.
