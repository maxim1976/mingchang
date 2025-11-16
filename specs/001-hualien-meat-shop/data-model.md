# Data Model: Hualien Meat E-Shop

**Feature**: 001-hualien-meat-shop  
**Date**: 2025-11-12  
**Purpose**: Define database schema, entities, relationships, and validation rules

## Overview

This data model supports a bilingual (Traditional Chinese/English) e-commerce site for a meat shop. Phase 1 covers product catalog, company info, and contact inquiries. Phase 2 adds cart, orders, and payment tracking.

---

## Phase 1: MVP Entities

### 1. Category

Represents product categories (e.g., beef, pork, chicken, seafood).

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `name_zh` | String(100) | NOT NULL, Indexed | Category name in Traditional Chinese |
| `name_en` | String(100) | NOT NULL, Indexed | Category name in English |
| `slug` | String(100) | UNIQUE, NOT NULL | URL-friendly identifier (e.g., "beef", "pork") |
| `description_zh` | Text | NULLABLE | Category description in Chinese |
| `description_en` | Text | NULLABLE | Category description in English |
| `display_order` | Integer | DEFAULT 0 | Sort order for display (0 = first) |
| `is_active` | Boolean | DEFAULT TRUE | Whether category is visible |
| `created_at` | DateTime | AUTO_NOW_ADD | Creation timestamp |
| `updated_at` | DateTime | AUTO_NOW | Last update timestamp |

**Indexes:**
- `name_zh`, `name_en` (for search)
- `slug` (unique, for URL routing)
- `display_order` (for sorted queries)

**Validation Rules:**
- `slug` must match pattern `^[a-z0-9-]+$` (lowercase, numbers, hyphens only)
- At least one of `name_zh` or `name_en` must be non-empty
- `display_order` must be >= 0

**Example Data:**
```python
Category(name_zh="牛肉", name_en="Beef", slug="beef", display_order=1)
Category(name_zh="豬肉", name_en="Pork", slug="pork", display_order=2)
Category(name_zh="雞肉", name_en="Chicken", slug="chicken", display_order=3)
Category(name_zh="海鮮", name_en="Seafood", slug="seafood", display_order=4)
```

---

### 2. Product

Represents meat products available for sale.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `category` | ForeignKey | NOT NULL, ON DELETE PROTECT | Reference to Category |
| `name_zh` | String(200) | NOT NULL, Indexed | Product name in Traditional Chinese |
| `name_en` | String(200) | NOT NULL, Indexed | Product name in English |
| `slug` | String(200) | UNIQUE, NOT NULL | URL-friendly identifier |
| `description_zh` | Text | NULLABLE | Product description in Chinese |
| `description_en` | Text | NULLABLE | Product description in English |
| `price` | Decimal(10,2) | NOT NULL, CHECK >= 0 | Price in TWD |
| `unit` | String(50) | NOT NULL | Unit of measurement (e.g., "kg", "斤", "piece") |
| `weight_grams` | Integer | NULLABLE, CHECK > 0 | Weight in grams (for shipping calculations Phase 2) |
| `origin_zh` | String(200) | NULLABLE | Origin/source in Chinese (e.g., "花蓮本地", "台東") |
| `origin_en` | String(200) | NULLABLE | Origin/source in English |
| `nutritional_info_zh` | Text | NULLABLE | Nutritional information in Chinese |
| `nutritional_info_en` | Text | NULLABLE | Nutritional information in English |
| `is_featured` | Boolean | DEFAULT FALSE | Show on homepage featured section |
| `is_available` | Boolean | DEFAULT TRUE | Available for viewing/ordering |
| `stock_status` | String(20) | DEFAULT 'in_stock' | in_stock, low_stock, out_of_stock, seasonal |
| `display_order` | Integer | DEFAULT 0 | Sort order within category |
| `created_at` | DateTime | AUTO_NOW_ADD | Creation timestamp |
| `updated_at` | DateTime | AUTO_NOW | Last update timestamp |

**Indexes:**
- `category` (foreign key)
- `name_zh`, `name_en` (for search)
- `slug` (unique, for URL routing)
- `is_featured`, `is_available` (for filtered queries)
- Composite: (`category`, `display_order`) for sorted category listings

**Validation Rules:**
- `price` must be >= 0
- `slug` must match pattern `^[a-z0-9-]+$`
- `stock_status` must be in ['in_stock', 'low_stock', 'out_of_stock', 'seasonal']
- If `is_featured=True`, `is_available` must be `True`

**Relationships:**
- **Category** (Many-to-One): Each product belongs to one category
- **ProductImage** (One-to-Many): Each product can have multiple images

**Example Data:**
```python
Product(
    category=beef_category,
    name_zh="澳洲和牛沙朗牛排",
    name_en="Australian Wagyu Sirloin Steak",
    slug="australian-wagyu-sirloin",
    description_zh="澳洲進口和牛，油花分布均勻，口感鮮嫩",
    description_en="Imported Australian Wagyu, well-marbled, tender texture",
    price=850.00,
    unit="kg",
    weight_grams=1000,
    origin_zh="澳洲",
    origin_en="Australia",
    is_featured=True,
    stock_status='in_stock'
)
```

---

### 3. ProductImage

Represents images for products (multiple images per product).

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `product` | ForeignKey | NOT NULL, ON DELETE CASCADE | Reference to Product |
| `image` | ImageField | NOT NULL | Image file (stored in /media/products/) |
| `thumbnail` | ImageField | AUTO-GENERATED | Thumbnail (150x150, generated by django-imagekit) |
| `card_image` | ImageField | AUTO-GENERATED | Card size (400x300, generated by django-imagekit) |
| `detail_image` | ImageField | AUTO-GENERATED | Detail size (800x600, generated by django-imagekit) |
| `alt_text_zh` | String(200) | NULLABLE | Alt text for accessibility (Chinese) |
| `alt_text_en` | String(200) | NULLABLE | Alt text for accessibility (English) |
| `display_order` | Integer | DEFAULT 0 | Order in product image gallery |
| `is_primary` | Boolean | DEFAULT FALSE | Primary image for product card/list views |
| `created_at` | DateTime | AUTO_NOW_ADD | Upload timestamp |

**Indexes:**
- `product` (foreign key)
- Composite: (`product`, `display_order`) for ordered image galleries

**Validation Rules:**
- Image file size must be <= 5MB before optimization
- Image dimensions must be >= 400x400 pixels
- Only one image per product can have `is_primary=True` (enforced in model save)
- Allowed formats: JPEG, PNG, WebP

**Relationships:**
- **Product** (Many-to-One): Each image belongs to one product

**Image Processing:**
- On upload, django-imagekit automatically generates:
  - `thumbnail`: 150x150 (for admin, thumbnails)
  - `card_image`: 400x300 (for product cards)
  - `detail_image`: 800x600 (for product detail page)
- WebP versions generated for all sizes with JPEG/PNG fallback

---

### 4. CompanyInfo

Represents business information (singleton model - only one instance).

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Always 1 (singleton) |
| `name_zh` | String(200) | NOT NULL | Shop name in Chinese |
| `name_en` | String(200) | NOT NULL | Shop name in English |
| `about_zh` | Text | NOT NULL | About/story in Chinese |
| `about_en` | Text | NOT NULL | About/story in English |
| `address_zh` | String(300) | NOT NULL | Physical address in Chinese |
| `address_en` | String(300) | NOT NULL | Physical address in English |
| `phone` | String(20) | NOT NULL | Phone number (format: +886-x-xxxx-xxxx) |
| `email` | EmailField | NOT NULL | Contact email |
| `latitude` | Decimal(9,6) | NULLABLE | GPS latitude for map |
| `longitude` | Decimal(9,6) | NULLABLE | GPS longitude for map |
| `business_hours_zh` | Text | NOT NULL | Business hours in Chinese |
| `business_hours_en` | Text | NOT NULL | Business hours in English |
| `facebook_url` | URLField | NULLABLE | Facebook page URL |
| `line_id` | String(50) | NULLABLE | LINE official account ID |
| `whatsapp_number` | String(20) | NULLABLE | WhatsApp number with country code |
| `instagram_url` | URLField | NULLABLE | Instagram profile URL |
| `logo` | ImageField | NULLABLE | Shop logo |
| `hero_image` | ImageField | NULLABLE | Homepage hero image |
| `updated_at` | DateTime | AUTO_NOW | Last update timestamp |

**Validation Rules:**
- Phone number must match Taiwan format: `^(\+886|0)[0-9-]{9,15}$`
- If `latitude` is set, `longitude` must also be set (and vice versa)
- Latitude range: 21.0 to 26.0 (Taiwan bounds)
- Longitude range: 119.0 to 122.5 (Taiwan bounds)

**Singleton Pattern:**
- Django model override `save()` to ensure only one instance exists (id=1)
- Admin interface auto-creates instance if missing

**Example Data:**
```python
CompanyInfo(
    id=1,
    name_zh="花蓮明昌肉品",
    name_en="Hualien MingChang Meat Shop",
    about_zh="在花蓮經營超過20年的老字號肉品店...",
    about_en="A trusted meat shop in Hualien for over 20 years...",
    address_zh="花蓮縣花蓮市中正路123號",
    address_en="No. 123, Zhongzheng Rd., Hualien City, Hualien County",
    phone="+886-3-1234-5678",
    email="info@mingchang-meat.tw",
    latitude=23.9769,
    longitude=121.6019,
    line_id="@mingchang",
    whatsapp_number="+886912345678"
)
```

---

### 5. ContactInquiry

Represents customer inquiries submitted via contact form.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `name` | String(100) | NOT NULL | Customer name |
| `phone` | String(20) | NOT NULL | Customer phone |
| `email` | EmailField | NOT NULL | Customer email |
| `subject` | String(200) | NULLABLE | Inquiry subject (optional) |
| `message` | Text | NOT NULL | Inquiry message |
| `language` | String(10) | DEFAULT 'zh-hant' | Language used (zh-hant, en) |
| `status` | String(20) | DEFAULT 'new' | new, read, replied, archived |
| `ip_address` | GenericIPAddressField | NULLABLE | Submitter IP (for spam prevention) |
| `user_agent` | String(300) | NULLABLE | Browser user agent |
| `created_at` | DateTime | AUTO_NOW_ADD | Submission timestamp |
| `replied_at` | DateTime | NULLABLE | When shop owner replied |
| `notes` | Text | NULLABLE | Internal notes (admin only) |

**Indexes:**
- `status` (for filtering in admin)
- `created_at` (for sorting by date)
- `email` (for finding previous inquiries from same customer)

**Validation Rules:**
- `phone` must match pattern `^[\d\s\-\+()]+$`
- `email` must be valid email format
- `language` must be in ['zh-hant', 'en']
- `status` must be in ['new', 'read', 'replied', 'archived']
- `message` length: 10 to 2000 characters

**State Transitions:**
```
new → read → replied → archived
  ↓             ↓
  └─────────────┴──→ archived
```

**Email Notifications:**
- On submission: Send confirmation email to customer
- On submission: Send notification email to shop owner
- On reply (Phase 2): Send reply email to customer

---

## Phase 2: Order Management Entities

### 6. Cart (Phase 2)

Represents a shopping cart session.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `session_key` | String(40) | UNIQUE, NOT NULL, Indexed | Django session key |
| `created_at` | DateTime | AUTO_NOW_ADD | Cart creation timestamp |
| `updated_at` | DateTime | AUTO_NOW | Last modification timestamp |
| `expires_at` | DateTime | NOT NULL | Expiration (7 days from creation) |

**Relationships:**
- **CartItem** (One-to-Many): Each cart has multiple items

**Cleanup:**
- Expired carts (older than 7 days) auto-deleted by daily cron job

---

### 7. CartItem (Phase 2)

Represents a product in a shopping cart.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `cart` | ForeignKey | NOT NULL, ON DELETE CASCADE | Reference to Cart |
| `product` | ForeignKey | NOT NULL, ON DELETE CASCADE | Reference to Product |
| `quantity` | Integer | NOT NULL, CHECK > 0 | Quantity ordered |
| `price_at_addition` | Decimal(10,2) | NOT NULL | Product price when added (price snapshot) |
| `created_at` | DateTime | AUTO_NOW_ADD | When added to cart |
| `updated_at` | DateTime | AUTO_NOW | Last quantity update |

**Indexes:**
- `cart` (foreign key)
- Composite: (`cart`, `product`) UNIQUE (prevent duplicate products in same cart)

**Validation Rules:**
- `quantity` must be > 0 and <= 999
- `price_at_addition` must match product's current price at time of addition

**Relationships:**
- **Cart** (Many-to-One): Each item belongs to one cart
- **Product** (Many-to-One): Each item references one product

---

### 8. Order (Phase 2)

Represents a completed customer order.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `order_number` | String(20) | UNIQUE, NOT NULL | Human-readable order ID (e.g., "ORD-20251112-0001") |
| `customer_name` | String(100) | NOT NULL | Customer name |
| `customer_phone` | String(20) | NOT NULL | Customer phone |
| `customer_email` | EmailField | NOT NULL | Customer email |
| `delivery_address_zh` | Text | NOT NULL | Delivery address in Chinese |
| `delivery_address_en` | Text | NULLABLE | Delivery address in English |
| `delivery_notes` | Text | NULLABLE | Special delivery instructions |
| `delivery_date_preference` | DateField | NULLABLE | Preferred delivery date |
| `delivery_time_preference` | String(50) | NULLABLE | Preferred time slot |
| `subtotal` | Decimal(10,2) | NOT NULL | Sum of order items |
| `delivery_fee` | Decimal(10,2) | DEFAULT 0.00 | Delivery charge |
| `total` | Decimal(10,2) | NOT NULL | Subtotal + delivery_fee |
| `payment_method` | String(50) | NOT NULL | credit_card, atm, cvs |
| `payment_status` | String(20) | DEFAULT 'pending' | pending, paid, failed, refunded |
| `order_status` | String(20) | DEFAULT 'pending' | pending, confirmed, preparing, shipped, delivered, cancelled |
| `language` | String(10) | NOT NULL | Customer's language preference |
| `created_at` | DateTime | AUTO_NOW_ADD | Order placement timestamp |
| `updated_at` | DateTime | AUTO_NOW | Last status update |
| `paid_at` | DateTime | NULLABLE | Payment completion timestamp |
| `delivered_at` | DateTime | NULLABLE | Delivery completion timestamp |
| `admin_notes` | Text | NULLABLE | Internal notes |

**Indexes:**
- `order_number` (unique)
- `customer_email` (for finding customer order history)
- `order_status`, `payment_status` (for admin filtering)
- `created_at` (for sorting by date)

**Validation Rules:**
- `order_number` format: `^ORD-\d{8}-\d{4}$`
- `payment_method` must be in ['credit_card', 'atm', 'cvs']
- `payment_status` must be in ['pending', 'paid', 'failed', 'refunded']
- `order_status` must be in ['pending', 'confirmed', 'preparing', 'shipped', 'delivered', 'cancelled']
- `subtotal` must equal sum of order items
- `total` must equal `subtotal + delivery_fee`

**State Machine:**

**Order Status:**
```
pending → confirmed → preparing → shipped → delivered
    ↓          ↓          ↓
    └──────────┴──────────┴──→ cancelled
```

**Payment Status:**
```
pending → paid
    ↓       ↓
    └───────┴──→ failed → refunded
```

**Relationships:**
- **OrderItem** (One-to-Many): Each order has multiple items
- **PaymentTransaction** (One-to-Many): Each order can have multiple payment attempts

---

### 9. OrderItem (Phase 2)

Represents a product in an order (immutable after creation).

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `order` | ForeignKey | NOT NULL, ON DELETE PROTECT | Reference to Order |
| `product` | ForeignKey | NOT NULL, ON DELETE PROTECT | Reference to Product |
| `product_name_zh` | String(200) | NOT NULL | Product name snapshot (Chinese) |
| `product_name_en` | String(200) | NOT NULL | Product name snapshot (English) |
| `quantity` | Integer | NOT NULL, CHECK > 0 | Quantity ordered |
| `unit_price` | Decimal(10,2) | NOT NULL | Price per unit at time of order |
| `subtotal` | Decimal(10,2) | NOT NULL | quantity * unit_price |

**Indexes:**
- `order` (foreign key)
- `product` (for analytics)

**Validation Rules:**
- All fields immutable after creation (historical record)
- `subtotal` must equal `quantity * unit_price`

**Rationale for Snapshots:**
- Store product name and price at time of order
- Allows product details/prices to change without affecting historical orders

**Relationships:**
- **Order** (Many-to-One): Each item belongs to one order
- **Product** (Many-to-One): Each item references one product (for reference)

---

### 10. PaymentTransaction (Phase 2)

Represents ECPay payment transaction records.

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique identifier |
| `order` | ForeignKey | NOT NULL, ON DELETE PROTECT | Reference to Order |
| `ecpay_trade_no` | String(100) | UNIQUE, NULLABLE | ECPay transaction ID |
| `merchant_trade_no` | String(20) | UNIQUE, NOT NULL | Our transaction ID (same as order_number) |
| `payment_type` | String(50) | NOT NULL | Credit_CreditCard, WebATM_TAISHIN, CVS_CVS, etc. |
| `amount` | Decimal(10,2) | NOT NULL | Transaction amount |
| `status` | String(20) | DEFAULT 'pending' | pending, success, failed, cancelled |
| `ecpay_response` | JSONField | NULLABLE | Full ECPay callback response |
| `error_message` | Text | NULLABLE | Error details if failed |
| `created_at` | DateTime | AUTO_NOW_ADD | Transaction initiation |
| `completed_at` | DateTime | NULLABLE | Transaction completion |

**Indexes:**
- `order` (foreign key)
- `ecpay_trade_no` (unique)
- `merchant_trade_no` (unique)
- `status` (for filtering)

**Validation Rules:**
- `merchant_trade_no` must match order's `order_number`
- `amount` must match order's `total`
- `status` must be in ['pending', 'success', 'failed', 'cancelled']

**Security:**
- Never store credit card numbers or CVV
- Only store ECPay transaction references
- Log all ECPay webhook callbacks for auditing

**Relationships:**
- **Order** (Many-to-One): Each transaction belongs to one order

---

## Entity Relationship Diagram (ERD)

```
Phase 1 (MVP):
┌──────────────┐         ┌─────────────┐
│   Category   │◄───┐    │   Product   │
│              │    │    │             │
│ - name_zh    │    └────│ + category  │
│ - name_en    │         │ - name_zh   │
│ - slug       │         │ - name_en   │
│ - is_active  │         │ - price     │
└──────────────┘         │ - is_featured│
                         └──────┬──────┘
                                │
                                │ 1:N
                                ▼
                         ┌──────────────┐
                         │ProductImage  │
                         │              │
                         │ - image      │
                         │ - alt_text   │
                         │ - is_primary │
                         └──────────────┘

┌──────────────────┐     ┌──────────────────┐
│  CompanyInfo     │     │ ContactInquiry   │
│  (Singleton)     │     │                  │
│ - name_zh/en     │     │ - name           │
│ - about_zh/en    │     │ - email          │
│ - address        │     │ - message        │
│ - phone          │     │ - status         │
│ - lat/lng        │     │ - created_at     │
└──────────────────┘     └──────────────────┘


Phase 2 (Orders):
┌──────────────┐         ┌──────────────┐
│     Cart     │◄───┐    │   CartItem   │
│              │    │    │              │
│ - session_key│    └────│ + cart       │
│ - expires_at │         │ + product    │
└──────────────┘         │ - quantity   │
                         └──────────────┘

┌──────────────┐         ┌──────────────┐
│    Order     │◄───┐    │  OrderItem   │
│              │    │    │              │
│ - order_no   │    └────│ + order      │
│ - customer   │         │ + product    │
│ - total      │         │ - quantity   │
│ - status     │         │ - unit_price │
└──────┬───────┘         │ - subtotal   │
       │                 └──────────────┘
       │ 1:N
       ▼
┌────────────────────┐
│ PaymentTransaction │
│                    │
│ - ecpay_trade_no   │
│ - amount           │
│ - status           │
└────────────────────┘
```

---

## Database Indexes Strategy

**Critical Indexes (Must Have):**
1. **Products**: `(category, display_order)` - Fast category page listings
2. **Products**: `name_zh`, `name_en` - Full-text search
3. **ProductImage**: `(product, display_order)` - Fast image gallery loading
4. **ContactInquiry**: `status`, `created_at` - Admin dashboard filtering
5. **Orders**: `order_number`, `customer_email`, `created_at` - Order lookups

**Performance Indexes (Recommended):**
1. **Products**: `(is_featured, is_available)` - Homepage featured products
2. **Products**: `slug` - Fast product detail lookups
3. **Categories**: `slug` - Fast category lookups
4. **PaymentTransaction**: `ecpay_trade_no` - ECPay webhook processing

---

## Data Migration Strategy

**Phase 1 to Phase 2:**
- No breaking changes to existing tables
- New tables added: Cart, CartItem, Order, OrderItem, PaymentTransaction
- Zero-downtime deployment possible

**Initial Data Loading:**
1. Create admin superuser
2. Load CompanyInfo (singleton)
3. Load Categories (4-6 initial)
4. Load Products with images (20-50 initial)
5. Test contact form submission

---

## Constitution Compliance Check

**Phase 1 Data Model** ✅

- **Code Quality**: Clear field names, single responsibility per model
- **Type Safety**: All fields have explicit types, validators defined
- **UX Consistency**: Bilingual fields support i18n requirements
- **Performance**: Indexes planned for all high-frequency queries

**Ready for Phase 1 Contracts**: API endpoint design can now proceed.
