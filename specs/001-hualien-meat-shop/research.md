# Research: Hualien Meat E-Shop

**Feature**: 001-hualien-meat-shop  
**Date**: 2025-11-12  
**Purpose**: Technical research and decision rationale for implementation choices

## Overview

This document consolidates research findings for building a bilingual e-commerce site for a meat shop in Hualien, Taiwan. The research focuses on technology choices that balance simplicity (for non-technical owners), performance (for mobile users in Taiwan), and maintainability.

---

## 1. Backend Framework: Django 5.x

### Decision
Use Django 5.x as the backend framework with server-side rendering.

### Rationale
- **Batteries Included**: Django provides ORM, admin interface, i18n/l10n, authentication, and form handling out-of-the-box—reducing development time
- **Admin Interface**: Django admin gives non-technical owners a familiar, low-learning-curve interface to manage products and view orders
- **Internationalization**: Built-in i18n framework supports Traditional Chinese and English with minimal configuration
- **Mature Ecosystem**: Extensive documentation, large community, well-tested in production e-commerce environments
- **Python Type Hints**: Python 3.11+ type hints satisfy constitution's type safety requirements
- **Security**: Built-in protections against SQL injection, XSS, CSRF—critical for e-commerce

### Alternatives Considered
- **FastAPI**: Rejected—overkill for server-rendered site; lacks built-in admin interface
- **Flask**: Rejected—too minimal, would require many third-party extensions for features Django provides
- **Node.js (Express)**: Rejected—team expertise in Python; Django admin superior for non-technical users

### Best Practices
- Use Django 5.x LTS for long-term support
- Implement class-based views (CBVs) for consistency and reusability
- Use Django REST Framework only for Phase 2 API endpoints (ECPay webhooks)
- Enable Django's security middleware (CSRF, XSS, clickjacking protection)
- Use `django-environ` for environment-based configuration

---

## 2. Frontend: HTMX + Tailwind CSS

### Decision
Use HTMX for dynamic interactions with Tailwind CSS for styling, avoiding heavy JavaScript frameworks.

### Rationale
- **Lightweight**: HTMX (~14KB) + Tailwind CSS (~50KB optimized) fits within 300KB JS budget
- **Server-Side Rendering**: HTMX enables dynamic content without client-side state management—simpler to maintain
- **Progressive Enhancement**: Works without JavaScript; degrades gracefully on older browsers
- **Mobile Performance**: Minimal JavaScript improves performance on older mobile devices (iOS 12+, Android 8+)
- **Developer Experience**: Tailwind utility classes speed up responsive design; HTMX attributes simplify AJAX interactions
- **SEO-Friendly**: Server-rendered content ensures search engines index product pages correctly

### Alternatives Considered
- **React/Next.js**: Rejected—too complex for this use case; requires Node.js build process; higher maintenance burden
- **Vue.js**: Rejected—unnecessary for primarily static content with occasional dynamic interactions
- **Vanilla CSS**: Rejected—Tailwind CSS accelerates responsive design and ensures consistency

### Best Practices
- Use HTMX `hx-boost` for progressive enhancement of navigation
- Implement Tailwind's `@apply` for reusable component styles
- Add Alpine.js (10KB) only if complex client-side state needed (e.g., cart quantity updates)
- Use Tailwind's JIT mode to minimize CSS bundle size
- Lazy-load HTMX partials for product listings to improve FCP

---

## 3. Database: PostgreSQL (Production) / SQLite (Development)

### Decision
PostgreSQL 15+ for production on Railway; SQLite 3 for local development.

### Rationale
- **PostgreSQL (Production)**:
  - **ACID Compliance**: Critical for order transactions in Phase 2
  - **Full-Text Search**: Built-in support for product search in Chinese and English
  - **JSON Fields**: Flexible storage for product attributes (e.g., nutritional info)
  - **Scalability**: Handles 100-2000+ concurrent users with proper indexing
  - **Railway Support**: Native PostgreSQL support with automatic backups
- **SQLite (Development)**:
  - **Zero Configuration**: Developers start immediately without database setup
  - **File-Based**: Easy to reset/seed test data
  - **Django Compatibility**: Django abstracts differences for most operations

### Alternatives Considered
- **MySQL**: Rejected—PostgreSQL superior for full-text search and JSON support
- **MongoDB**: Rejected—relational data (products, categories, orders) fits SQL better
- **PostgreSQL Everywhere**: Rejected—SQLite simplifies local development for team members

### Best Practices
- Use Django migrations to keep schema consistent across SQLite and PostgreSQL
- Index foreign keys, product names (Chinese/English), and created_at timestamps
- Enable PostgreSQL's `pg_trgm` extension for fuzzy product search
- Use database constraints (CHECK, UNIQUE) to enforce data integrity
- Configure connection pooling (pgBouncer) if concurrent users exceed 100

---

## 4. Image Optimization Strategy

### Decision
Use Pillow with django-imagekit for automatic image optimization; serve WebP with JPEG/PNG fallbacks.

### Rationale
- **Performance**: WebP images 25-35% smaller than JPEG/PNG while maintaining quality
- **Mobile-First**: Lazy loading + optimized images critical for 3G connections in Taiwan
- **Automated**: django-imagekit generates thumbnails and optimized versions on upload
- **Fallback Support**: Serve JPEG/PNG to older browsers (IE11, iOS <14)
- **CDN-Ready**: Optimized images can be served via Railway's CDN or Cloudflare

### Best Practices
- Generate multiple image sizes: thumbnail (150x150), card (400x300), detail (800x600), full (1200x900)
- Use `loading="lazy"` attribute for images below the fold
- Compress uploads to max 200KB using Pillow before saving
- Store images in `/media/products/` with organized subdirectories by category
- Use Cloudflare CDN (free tier) for Taiwan region caching

---

## 5. Internationalization (i18n): Django i18n Framework

### Decision
Use Django's built-in i18n/l10n framework with `django.middleware.locale.LocaleMiddleware`.

### Rationale
- **Built-In**: No third-party dependencies; battle-tested in production
- **Cookie-Based**: Language preference persists across sessions
- **Template Support**: `{% trans %}` and `{% blocktrans %}` tags for translatable strings
- **Database Support**: Separate fields for Chinese/English product names and descriptions
- **URL Patterns**: Optional language prefix in URLs (`/zh-hant/products/`, `/en/products/`)

### Alternatives Considered
- **Separate Domains**: Rejected—too complex for 2-language site
- **django-modeltranslation**: Rejected—simpler to use separate fields (name_zh, name_en) for this scale

### Best Practices
- Default language: Traditional Chinese (`zh-Hant`)
- Use `LANGUAGE_CODE = 'zh-hant'` in settings
- Store translations in `/locale/zh_Hant/` and `/locale/en/` directories
- Use `gettext_lazy` for model verbose names and help_text
- Add language switcher in navbar with HTMX for instant switching without page reload

---

## 6. Testing Strategy

### Decision
- **Unit Tests**: pytest with pytest-django for models, forms, utilities
- **Integration Tests**: pytest for view testing and user journey flows
- **E2E Tests**: Playwright for critical paths (browsing, contact form, Phase 2 checkout)

### Rationale
- **pytest**: More Pythonic than Django's unittest; better fixtures and parametrization
- **pytest-django**: Seamless Django integration with database fixtures
- **Playwright**: Modern E2E testing; supports mobile emulation for responsive testing
- **factory-boy**: Generate realistic test data for products, categories, orders

### Best Practices
- Target >80% code coverage (constitution requirement)
- Write tests BEFORE implementation (TDD, constitution Principle II)
- Use `pytest-cov` to track coverage
- Run E2E tests in CI/CD before deployment
- Create fixtures for common scenarios (product catalog, contact form submission)

---

## 7. Deployment: Docker + Railway

### Decision
Deploy Django application via Docker containers to Railway.

### Rationale
- **Docker**: Consistent environments (dev, staging, production); easy rollback
- **Railway**:
  - **Simplicity**: Git-based deployment (push to deploy)
  - **PostgreSQL**: Managed PostgreSQL with automatic backups
  - **Environment Variables**: Secure secrets management
  - **Taiwan Region**: Can deploy to Asia Pacific regions for low latency
  - **Cost**: Affordable for small e-commerce site ($5-20/month estimated)
  - **Scaling**: Vertical and horizontal scaling available if traffic grows

### Alternatives Considered
- **Heroku**: Rejected—higher cost, less flexibility than Railway
- **DigitalOcean**: Rejected—requires more manual DevOps; Railway simpler for small team
- **Vercel**: Rejected—optimized for Next.js/static sites, not Django
- **AWS/GCP**: Rejected—overkill for this scale; higher complexity

### Best Practices
- Use multi-stage Dockerfile to minimize image size
- Configure `whitenoise` for efficient static file serving
- Set `DEBUG=False` in production via environment variables
- Use Railway's automatic HTTPS certificates
- Configure `ALLOWED_HOSTS` to Railway domain
- Enable Railway's automatic health checks and restarts

---

## 8. Payment Gateway: ECPay (Phase 2)

### Decision
Integrate ECPay payment gateway for Phase 2 online orders.

### Rationale
- **Taiwan Market Leader**: Most trusted payment gateway in Taiwan
- **Multiple Payment Methods**: Credit card, ATM transfer, convenience store payment (7-11, FamilyMart)
- **Django Integration**: Community packages available (django-ecpay)
- **Documentation**: Chinese and English documentation available
- **Compliance**: PCI-DSS compliant; handles sensitive payment data securely
- **Settlement**: Direct bank transfer to merchant account in TWD

### Best Practices
- Use ECPay test environment for development
- Implement webhook endpoints for payment confirmation
- Store only ECPay transaction IDs, never credit card details
- Log all payment events for auditing
- Implement retry logic for failed webhook deliveries
- Display clear payment instructions for ATM and convenience store methods

---

## 9. SEO & Accessibility

### Decision
- **SEO**: Server-side rendering, semantic HTML, meta tags, sitemap.xml, robots.txt
- **Accessibility**: WCAG 2.1 AA compliance with aria-labels, keyboard navigation, screen reader support

### Rationale
- **SEO Critical**: Local search in Hualien for "meat shop" / "肉品店花蓮" must rank well
- **Accessibility**: Constitution Principle III requires WCAG 2.1 AA; also improves usability for older customers

### Best Practices
- Use Django's `django.contrib.sitemaps` for automatic sitemap generation
- Add structured data (Schema.org) for products, business info
- Implement `<title>`, `<meta description>`, Open Graph tags for each page
- Use semantic HTML (`<nav>`, `<main>`, `<article>`, `<footer>`)
- Ensure 44px minimum touch target size (constitution requirement)
- Test with NVDA/JAWS screen readers and axe DevTools
- Add skip navigation link for keyboard users

---

## 10. Email Notifications

### Decision
Use Django's email backend with SMTP (Gmail, SendGrid, or Railway's email service).

### Rationale
- **Simple Setup**: Django's built-in email framework sufficient for contact form and order confirmations
- **Reliability**: SMTP services provide delivery guarantees and bounce handling
- **Future Scaling**: Can migrate to Mailgun/SendGrid if email volume grows

### Best Practices
- Use environment variables for SMTP credentials
- Implement HTML + plain text email templates
- Queue emails asynchronously if response time is critical (Celery + Redis optional)
- Include unsubscribe link for order notification emails (if future marketing emails added)
- Test email delivery in staging before production

---

## Summary of Key Decisions

| Area | Decision | Primary Reason |
|------|----------|----------------|
| Backend | Django 5.x | Admin interface for non-technical owners, built-in i18n |
| Frontend | HTMX + Tailwind CSS | Lightweight, mobile-first, server-rendered |
| Database | PostgreSQL + SQLite | Production reliability + dev simplicity |
| Deployment | Docker + Railway | Simple Git-based deployment, Taiwan region support |
| Testing | pytest + Playwright | Constitution compliance (TDD, >80% coverage) |
| i18n | Django i18n | Built-in, cookie-based language switching |
| Images | Pillow + django-imagekit | Automatic optimization, WebP support |
| Payment | ECPay | Taiwan market leader, multiple payment methods |
| SEO | Server-side rendering | Critical for local search rankings |
| Email | Django SMTP | Simple, reliable for contact form notifications |

---

## Constitution Compliance

**Phase 0 Research Complete** ✅

All technical decisions align with Shop MingChang Constitution v1.0.0:

- **Code Quality**: Python type hints, Django's structure enforces single responsibility
- **Test-First**: pytest + Playwright enable TDD workflow, >80% coverage achievable
- **UX Consistency**: Tailwind CSS design system, WCAG 2.1 AA compliance planned
- **Performance**: HTMX + optimized images meet FCP <1.5s, TTI <3s, LCP <2.5s goals

**Ready for Phase 1**: Data model and contract design can now proceed.
