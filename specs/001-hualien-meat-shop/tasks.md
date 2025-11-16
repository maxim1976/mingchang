# Tasks: Hualien Meat E-Shop

**Feature**: 001-hualien-meat-shop  
**Branch**: `001-hualien-meat-shop`  
**Date**: 2025-11-12  
**Purpose**: Implementation task breakdown organized by user story

---

## Task Organization

Tasks are organized into phases:
1. **Setup** (T001-T010): Project initialization
2. **Foundational** (T011-T030): Core infrastructure
3. **User Story P1** (T031-T070): Browse Products (MVP)
4. **User Story P2** (T071-T090): Mobile-Friendly
5. **User Story P3** (T091-T110): Contact & Location
6. **Polish** (T111-T130): Performance, SEO, Accessibility

**Phase 2 (Future - User Story P4)**: Cart, checkout, payment integration with ECPay (not included in this task list)

---

## Setup Phase (T001-T010)

Project initialization, dependencies, and deployment configuration.

- [X] T001 [P1] [Setup] Initialize Django 5.x project with settings split (base.py, development.py, production.py, test.py) → `manage.py`, `config/settings/`
- [X] T002 [P1] [Setup] Create requirements.txt with Django 5.x, psycopg2-binary, Pillow, django-imagekit, django-environ, whitenoise, gunicorn → `requirements.txt`
- [X] T003 [P1] [Setup] Create requirements-dev.txt with pytest, pytest-django, pytest-cov, factory-boy, Playwright, ruff, black → `requirements-dev.txt`
- [X] T004 [P1] [Setup] Configure environment variables template with SECRET_KEY, DATABASE_URL, DEBUG, ALLOWED_HOSTS → `.env.example`
- [X] T005 [P1] [Setup] Create Dockerfile for production deployment (Python 3.11, gunicorn, collectstatic) → `Dockerfile`
- [X] T006 [P1] [Setup] Create docker-compose.yml for local PostgreSQL development environment → `docker-compose.yml`
- [X] T007 [P1] [Setup] Configure Railway deployment with railway.json (Taiwan region, PostgreSQL service, build command) → `railway.json`
- [X] T008 [P1] [Setup] Configure pytest with pytest.ini (DJANGO_SETTINGS_MODULE=config.settings.test, coverage settings) → `pytest.ini`
- [X] T009 [P1] [Setup] Create .gitignore for Python, Django, IDEs, environment files, media uploads → `.gitignore`
- [X] T010 [P1] [Setup] Initialize Django apps structure: shop, contact, orders → `apps/shop/`, `apps/contact/`, `apps/orders/`

---

## Foundational Phase (T011-T030)

Core infrastructure: database, static files, templates, admin configuration.

- [X] T011 [P1] [Foundational] Configure PostgreSQL for production in config/settings/production.py with dj-database-url → `config/settings/production.py`
- [X] T012 [P1] [Foundational] Configure SQLite for development in config/settings/development.py → `config/settings/development.py`
- [X] T013 [P1] [Foundational] Configure test database (SQLite in-memory) in config/settings/test.py → `config/settings/test.py`
- [X] T014 [P1] [Foundational] Configure static files with whitenoise (STATIC_ROOT, STATICFILES_STORAGE, compression) → `config/settings/base.py`
- [X] T015 [P1] [Foundational] Configure media files (MEDIA_ROOT, MEDIA_URL, upload_to paths for products/) → `config/settings/base.py`
- [X] T016 [P1] [Foundational] Set up Tailwind CSS with CDN (3.x) in base template → `templates/base.html`
- [X] T017 [P1] [Foundational] Download and configure HTMX 1.9+ library → `static/js/htmx.min.js`, `templates/base.html`
- [X] T018 [P1] [Foundational] Download and configure Alpine.js for minimal interactions → `static/js/alpine.min.js`, `templates/base.html`
- [X] T019 [P1] [Foundational] Create base.html template with bilingual structure (Chinese primary + English secondary inline), HTMX, Tailwind CSS, SEO meta tags → `templates/base.html`
- [X] T020 [P1] [Foundational] Configure Django admin interface in English (LANGUAGE_CODE='en-us') for developer use → `config/settings/base.py`
- [X] T021 [P1] [Foundational] Create reusable navbar component with bilingual navigation (首頁 Home, 產品 Products, 關於我們 About, 聯絡我們 Contact) → `templates/components/navbar.html`
- [X] T022 [P1] [Foundational] Create reusable footer component with bilingual copyright and social media links → `templates/components/footer.html`
- [X] T023 [P1] [Foundational] Configure ImageKit for product image optimization (thumbnail, medium, large specs) → `config/settings/base.py`
- [X] T024 [P1] [Foundational] Set up custom template tags for bilingual field rendering (get_translated_field templatetag) → `apps/shop/templatetags/shop_tags.py`
- [X] T024b [P1] [Foundational] Create Taiwan TWD price formatting template filter with comma separators and NT$ prefix (e.g., NT$ 1,234.56) → `apps/shop/templatetags/shop_tags.py`
- [ ] T025 [P1] [Foundational] Create factory for test data generation using factory-boy → `tests/factories.py`
- [ ] T026 [P1] [Foundational] Configure pytest fixtures for database, client, user → `tests/conftest.py`
- [X] T027 [P1] [Foundational] Set up custom CSS for additional styling beyond Tailwind → `static/css/custom.css`
- [ ] T028 [P1] [Foundational] Create placeholder images for products and company → `static/images/placeholders/`
- [ ] T029 [P1] [Foundational] Configure URL routing in config/urls.py for shop, contact, orders apps → `config/urls.py`
- [X] T030 [P1] [Foundational] Set up error templates (404.html, 500.html) with bilingual messages → `templates/404.html`, `templates/500.html`

---

## User Story P1: Browse Products (MVP) (T031-T070)

**As a customer, I want to browse meat products with details so that I can see what's available.**

### Models & Database (T031-T036)

- [ ] T031 [P1] [Story P1] Create Category model with bilingual fields (name_zh, name_en, slug, description_zh, description_en, display_order, is_active) → `apps/shop/models.py`
- [ ] T032 [P1] [Story P1] Create Product model with bilingual fields (category FK, name_zh, name_en, slug, description_zh, description_en, price, unit, weight_grams, origin_zh, origin_en, nutritional_info_zh, nutritional_info_en, is_featured, is_available, stock_status), include validation for stock_status enum (in_stock, low_stock, out_of_stock, seasonal) → `apps/shop/models.py`
- [ ] T033 [P1] [Story P1] Create ProductImage model (product FK, image, alt_text_zh, alt_text_en, display_order, is_primary), include default placeholder handling for missing images → `apps/shop/models.py`
- [ ] T034 [P1] [Story P1] Create CompanyInfo model with bilingual fields (name_zh, name_en, about_zh, about_en, address_zh, address_en, phone, email, latitude, longitude, business_hours_zh, business_hours_en, line_id, whatsapp, facebook_url, hero_image) → `apps/shop/models.py`
- [ ] T035 [P1] [Story P1] Write unit tests for Category, Product, ProductImage, CompanyInfo models (validation, str methods, ordering) → `apps/shop/tests/test_models.py`
- [ ] T036 [P1] [Story P1] Create and run initial migrations for shop app → `apps/shop/migrations/0001_initial.py`

### Admin Interface (T037-T041)

- [ ] T037 [P1] [Story P1] Register Category in Django admin with bilingual list display, search fields (name_zh, name_en), filters (is_active), ordering by display_order → `apps/shop/admin.py`
- [ ] T038 [P1] [Story P1] Register Product in Django admin with bilingual list display, search (name_zh, name_en), filters (category, is_featured, is_available, stock_status), inline ProductImages → `apps/shop/admin.py`
- [ ] T039 [P1] [Story P1] Register ProductImage in Django admin with image preview, display_order sorting → `apps/shop/admin.py`
- [ ] T040 [P1] [Story P1] Register CompanyInfo in Django admin with full bilingual field display → `apps/shop/admin.py`
- [ ] T041 [P1] [Story P1] Test admin interface: create 4 categories (牛肉 Beef, 豬肉 Pork, 雞肉 Chicken, 海鮮 Seafood), 12 products with images, company info → Manual testing

### Views & Templates (T042-T055)

- [ ] T042 [P1] [Story P1] Create HomeView (TemplateView) to display featured products and company intro → `apps/shop/views.py`
- [ ] T043 [P1] [Story P1] Create home.html template with bilingual hero section, featured products grid (3 columns desktop, 1 column mobile), CTAs → `templates/shop/home.html`
- [ ] T044 [P1] [Story P1] Create ProductListView (ListView) with category filtering, search, sorting (price-asc, price-desc, name, featured), pagination (12 per page) → `apps/shop/views.py`
- [ ] T045 [P1] [Story P1] Create product_list.html template with bilingual category filters (sidebar), product grid (3 columns desktop, 2 tablet, 1 mobile), search bar, sort dropdown → `templates/shop/product_list.html`
- [ ] T046 [P1] [Story P1] Create ProductDetailView (DetailView) with slug lookup, related products (4 from same category) → `apps/shop/views.py`
- [ ] T047 [P1] [Story P1] Create product_detail.html template with bilingual product info, image gallery (primary + thumbnails), price display (NT$ formatting using TWD template filter), nutritional info accordion → `templates/shop/product_detail.html`
- [ ] T048 [P1] [Story P1] Create AboutView (TemplateView) to display company information and location → `apps/shop/views.py`
- [ ] T049 [P1] [Story P1] Create about.html template with bilingual company story, team photos, embedded Google Maps (location overview), business hours table, social media links → `templates/shop/about.html`
- [ ] T050 [P1] [Story P1] Create product_card.html component for reusable product display (image, bilingual name, price with TWD formatting, stock status badge) → `templates/components/product_card.html`
- [ ] T051 [P1] [Story P1] Configure shop app URLs: /, /products/, /products/<slug>/, /about/ → `apps/shop/urls.py`
- [ ] T052 [P1] [Story P1] Add HTMX enhancement for category filtering (hx-get, hx-target="#product-grid", hx-push-url) → `templates/shop/product_list.html`
- [ ] T053 [P1] [Story P1] Add HTMX enhancement for live search (hx-get with delay:500ms, hx-target="#product-grid") → `templates/shop/product_list.html`
- [ ] T054 [P1] [Story P1] Add HTMX enhancement for product image gallery (hx-get for thumbnail clicks, hx-target="#main-image") → `templates/shop/product_detail.html`
- [ ] T055 [P1] [Story P1] Add HTMX enhancement for pagination (hx-get, hx-swap="outerHTML") → `templates/shop/product_list.html`

### Testing (T056-T065)

- [ ] T056 [P1] [Story P1] Write view tests for HomeView (status 200, featured products in context, template used) → `apps/shop/tests/test_views.py`
- [ ] T057 [P1] [Story P1] Write view tests for ProductListView (category filtering, search, sorting, pagination) → `apps/shop/tests/test_views.py`
- [ ] T058 [P1] [Story P1] Write view tests for ProductDetailView (slug lookup, related products, 404 for invalid slug) → `apps/shop/tests/test_views.py`
- [ ] T059 [P1] [Story P1] Write view tests for AboutView (company info in context) → `apps/shop/tests/test_views.py`
- [ ] T060 [P1] [Story P1] Write integration tests for user journey: landing → browse products → filter by category → view product detail → return to list → `apps/shop/tests/test_integration.py`
- [ ] T061 [P1] [Story P1] Write integration tests for search functionality: search query → results displayed → no results handling → `apps/shop/tests/test_integration.py`
- [ ] T062 [P1] [Story P1] Write HTMX interaction tests: category filter triggers partial reload, search debounce works, pagination preserves filters → `apps/shop/tests/test_integration.py`
- [ ] T063 [P1] [Story P1] Verify test coverage >80% for shop app (models, views) → Run `pytest --cov=apps/shop --cov-report=html`
- [ ] T064 [P1] [Story P1] Create Playwright E2E test for browsing flow: visit homepage → click category → click product → verify details displayed → `tests/e2e/test_browsing.py`
- [ ] T065 [P1] [Story P1] Seed database with realistic test data (4 categories, 20 products, company info) using Django management command or fixtures → `apps/shop/management/commands/seed_data.py`

### SEO & Performance (T066-T070)

- [ ] T066 [P1] [Story P1] Add SEO meta tags to all templates (title, description, canonical URL, Open Graph tags) → `templates/shop/*.html`
- [ ] T067 [P1] [Story P1] Add Schema.org structured data for Product pages (JSON-LD) → `templates/shop/product_detail.html`
- [ ] T068 [P1] [Story P1] Configure image lazy loading (loading="lazy" on non-primary images) → `templates/shop/*.html`, `templates/components/product_card.html`
- [ ] T069 [P1] [Story P1] Implement image compression with ImageKit (WebP format with PNG/JPG fallbacks, responsive srcset) → `apps/shop/models.py`, templates
- [ ] T070 [P1] [Story P1] Measure page load performance: verify homepage <3s on 3G, product list <2s on 4G → Manual testing with Chrome DevTools Network throttling

---

## User Story P2: Mobile-Friendly (T071-T090)

**As a customer, I want the website to work perfectly on my mobile phone so that I can browse while on the go.**

### Responsive Design (T071-T080)

- [ ] T071 [P2] [Story P2] Implement responsive breakpoints in base.html and all templates (320px-768px mobile, 768px-1024px tablet, 1024px+ desktop) using Tailwind CSS classes → `templates/base.html`, `templates/shop/*.html`
- [ ] T072 [P2] [Story P2] Optimize navbar for mobile: hamburger menu (Alpine.js toggle), full-screen overlay on mobile → `templates/components/navbar.html`
- [ ] T073 [P2] [Story P2] Optimize product grid for mobile: 1 column on mobile, 2 columns on tablet, 3 columns on desktop using Tailwind grid classes → `templates/shop/product_list.html`, `templates/shop/home.html`
- [ ] T074 [P2] [Story P2] Optimize product detail layout for mobile: single column, image carousel with touch swipe support → `templates/shop/product_detail.html`
- [ ] T075 [P2] [Story P2] Ensure all touch targets ≥44px (buttons, links, form inputs) on mobile → `static/css/custom.css`, all templates
- [ ] T076 [P2] [Story P2] Add viewport meta tag for proper mobile scaling → `templates/base.html`
- [ ] T077 [P2] [Story P2] Configure font sizes for mobile readability (minimum 16px for body text to prevent zoom) → `static/css/custom.css`
- [ ] T078 [P2] [Story P2] Implement sticky header on mobile for easy navigation access → `templates/components/navbar.html`, `static/css/custom.css`
- [ ] T079 [P2] [Story P2] Add click-to-call functionality for phone numbers on mobile (tel: links) → `templates/shop/about.html`, `templates/components/footer.html`
- [ ] T080 [P2] [Story P2] Optimize image loading for mobile: smaller image sizes served on mobile viewports using srcset → `templates/components/product_card.html`, `templates/shop/product_detail.html`

### Testing (T081-T090)

- [ ] T081 [P2] [Story P2] Test responsive layout on mobile (320px, 360px, 375px, 414px widths) using Chrome DevTools → Manual testing
- [ ] T082 [P2] [Story P2] Test responsive layout on tablet (768px, 1024px widths) → Manual testing
- [ ] T083 [P2] [Story P2] Test responsive layout on desktop (1280px, 1920px widths) → Manual testing
- [ ] T084 [P2] [Story P2] Test touch interactions: navbar toggle, image carousel swipe, button taps (verify no double-tap zoom) → Manual testing on mobile device
- [ ] T085 [P2] [Story P2] Create Playwright E2E tests for mobile viewport (375px): browse products, view detail, navigate → `tests/e2e/test_mobile_responsive.py`
- [ ] T086 [P2] [Story P2] Verify all text readable without zooming on mobile (font size ≥16px) → Manual testing
- [ ] T087 [P2] [Story P2] Verify all interactive elements easily tappable (≥44px touch targets) → Manual testing with finger on device
- [ ] T088 [P2] [Story P2] Test horizontal scrolling: verify no unwanted horizontal scroll on mobile → Manual testing
- [ ] T089 [P2] [Story P2] Test performance on 3G mobile connection: verify page load <3s → Chrome DevTools Network throttling
- [ ] T090 [P2] [Story P2] Validate mobile-friendly with Google Mobile-Friendly Test tool → Use https://search.google.com/test/mobile-friendly

---

## User Story P3: Contact & Location (T091-T110)

**As a customer, I want to contact the shop and find its location so that I can ask questions or visit.**

### Models & Database (T091-T093)

- [ ] T091 [P3] [Story P3] Create ContactInquiry model (name, phone, email, message, submitted_at, language, is_read) → `apps/contact/models.py`
- [ ] T092 [P3] [Story P3] Write unit tests for ContactInquiry model (validation, str method, ordering by submitted_at desc) → `apps/contact/tests/test_models.py`
- [ ] T093 [P3] [Story P3] Create and run migrations for contact app → `apps/contact/migrations/0001_initial.py`

### Admin Interface (T094-T095)

- [ ] T094 [P3] [Story P3] Register ContactInquiry in Django admin with list display (name, email, submitted_at, is_read), filters (is_read, submitted_at), search (name, email, message), mark as read action → `apps/contact/admin.py`
- [ ] T095 [P3] [Story P3] Test admin interface: submit test inquiry, mark as read → Manual testing

### Forms & Views (T096-T103)

- [ ] T096 [P3] [Story P3] Create ContactForm (Django ModelForm) with fields: name, phone, email, message, validation (email format, phone format for Taiwan, message max length 1000 chars) → `apps/contact/forms.py`
- [ ] T097 [P3] [Story P3] Create ContactView (FormView) to handle form submission, send email notification to shop owner, display success message → `apps/contact/views.py`
- [ ] T098 [P3] [Story P3] Create contact.html template with bilingual contact form, company contact details (phone, email, LINE, WhatsApp), embedded Google Maps with directions focus (reuses map from About page), business hours → `templates/contact/contact.html`
- [ ] T099 [P3] [Story P3] Configure email backend with SMTP settings (use Railway environment variables for EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD), include basic error handling and logging for failed sends → `config/settings/base.py`, `.env.example`
- [ ] T100 [P3] [Story P3] Create email template for contact inquiry notification to shop owner (bilingual subject, includes customer name, email, phone, message) → `templates/contact/email/inquiry_notification.html`, `templates/contact/email/inquiry_notification.txt`
- [ ] T101 [P3] [Story P3] Add HTMX enhancement for contact form submission (hx-post, hx-target="#form-container", display success message without page reload) → `templates/contact/contact.html`
- [ ] T102 [P3] [Story P3] Add form validation styling (error messages in red, success in green, bilingual validation messages) → `templates/contact/contact.html`, `static/css/custom.css`
- [ ] T103 [P3] [Story P3] Configure contact app URLs: /contact/ → `apps/contact/urls.py`, include in `config/urls.py`

### Testing (T104-T110)

- [ ] T104 [P3] [Story P3] Write view tests for ContactView: GET displays form, POST with valid data creates ContactInquiry and sends email → `apps/contact/tests/test_views.py`
- [ ] T105 [P3] [Story P3] Write form validation tests: empty fields rejected, invalid email rejected, invalid phone rejected, valid submission accepted → `apps/contact/tests/test_forms.py`
- [ ] T106 [P3] [Story P3] Write integration test for contact flow: visit contact page → fill form → submit → verify inquiry saved, email sent, success message displayed → `apps/contact/tests/test_integration.py`
- [ ] T107 [P3] [Story P3] Test email notification delivery (use Django console email backend for testing) → `config/settings/test.py`, manual testing
- [ ] T108 [P3] [Story P3] Verify test coverage >80% for contact app → Run `pytest --cov=apps/contact --cov-report=html`
- [ ] T109 [P3] [Story P3] Create Playwright E2E test for contact flow: navigate to contact → fill form → submit → verify success message → `tests/e2e/test_contact.py`
- [ ] T110 [P3] [Story P3] Test spam protection: verify form submission rate limiting (basic throttling or honeypot field) → `apps/contact/views.py`, `apps/contact/tests/test_views.py`

---

## Polish Phase (T111-T130)

Final optimizations, accessibility, SEO, and documentation.

### Performance Optimization (T111-T117)

- [ ] T111 [Polish] Configure database connection pooling for PostgreSQL on Railway → `config/settings/production.py`
- [ ] T112 [Polish] Enable Django template caching for production (cache category list, company info) → `config/settings/production.py`
- [ ] T113 [Polish] Enable GZip compression with whitenoise for static files → `config/settings/production.py`
- [ ] T114 [Polish] Configure CDN for static files (optional, Railway provides edge caching) → `config/settings/production.py`
- [ ] T115 [Polish] Add database indexes for frequently queried fields (Category.display_order, Product.is_featured, Product.category, ContactInquiry.submitted_at) → New migration
- [ ] T116 [Polish] Optimize queries with select_related and prefetch_related (Product → Category, ProductImages) → `apps/shop/views.py`
- [ ] T117 [Polish] Run performance audit with Lighthouse: target scores Performance >90, Accessibility >90, Best Practices >90, SEO >90 → Chrome DevTools Lighthouse

### Accessibility (T118-T122)

- [ ] T118 [Polish] Add ARIA labels to all interactive elements (buttons, links, form inputs) with bilingual aria-label attributes → All templates
- [ ] T119 [Polish] Ensure proper heading hierarchy (h1 → h2 → h3, no skipped levels) → All templates
- [ ] T120 [Polish] Add alt text to all images (bilingual alt_text_zh, alt_text_en fields) → `apps/shop/models.py`, templates
- [ ] T121 [Polish] Test keyboard navigation: verify all interactive elements accessible via Tab, Enter, Escape keys → Manual testing
- [ ] T122 [Polish] Run accessibility audit with axe DevTools or WAVE: target WCAG 2.1 AA compliance → Browser extension testing

### SEO (T123-T126)

- [ ] T123 [Polish] Create sitemap.xml with all public URLs (products, categories, static pages) → `apps/shop/sitemaps.py`, `config/urls.py`
- [ ] T124 [Polish] Create robots.txt to allow search engine crawling → `static/robots.txt`
- [ ] T125 [Polish] Add bilingual hreflang tags to indicate language alternatives (zh-Hant, en) → `templates/base.html`
- [ ] T126 [Polish] Submit sitemap to Google Search Console and verify indexing → Manual task after deployment

### Documentation (T127-T130)

- [ ] T127 [Polish] Write README.md with project overview, setup instructions, deployment guide → `README.md`
- [ ] T128 [Polish] Document environment variables in .env.example with descriptions → `.env.example`
- [ ] T129 [Polish] Create admin user guide (bilingual) for adding products, managing inquiries → `docs/admin-guide.md`
- [ ] T129b [Polish] Create simplified visual Django admin guide with screenshots for non-technical shop owners → `docs/admin-user-guide-visual.md`
- [ ] T129c [Polish] Test admin workflow with non-technical shop owner, document any usability issues and simplify UI if needed → Manual testing, update admin.py
- [ ] T130 [Polish] Write developer documentation with architecture overview, testing guide, contribution guidelines → `docs/developer-guide.md`

---

## Summary

**Total Tasks**: 132  
**Phase 1 (MVP)**: T001-T110 (User Stories P1, P2, P3)  
**Polish**: T111-T132 (Performance, Accessibility, SEO, Documentation)  
**Phase 2 (Future)**: User Story P4 (Cart, Checkout, ECPay) - Tasks to be generated when approved

**Language Approach**: Bilingual inline display (Chinese primary + English secondary) throughout the site. No separate language versions, no Django i18n middleware, no translation files. Django admin interface configured in English for developer use.

**Testing Strategy**: TDD approach with >80% test coverage. Unit tests for models/forms, view tests for HTTP responses, integration tests for user journeys, Playwright E2E tests for critical flows.

**Deployment**: Docker container on Railway with PostgreSQL database. Environment variables for configuration. Static files served with whitenoise.

**Constitution Compliance**:
- ✅ Code Quality: Models, views, templates follow Django best practices
- ✅ Test-First TDD: Unit tests before implementation, >80% coverage target
- ✅ UX Consistency: Bilingual inline display, responsive design, WCAG 2.1 AA
- ✅ Performance: <3s page load on 3G, lazy loading, image optimization, caching
