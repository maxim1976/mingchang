# Quickstart Guide: Hualien Meat E-Shop

**Feature**: 001-hualien-meat-shop  
**Date**: 2025-11-12  
**Purpose**: Developer setup and integration testing instructions

## Prerequisites

Before starting development, ensure you have:

- **Python**: 3.11 or higher
- **pip**: Latest version (`python -m pip install --upgrade pip`)
- **Git**: For version control
- **Code Editor**: VS Code recommended with Python extension
- **PostgreSQL**: 15+ (optional for local dev; Railway provides production DB)
- **Docker**: For containerized deployment (optional for local dev)

**Optional but Recommended:**
- **pyenv**: Python version management
- **virtualenv** or **venv**: Virtual environment management
- **PostgreSQL GUI**: pgAdmin, DBeaver, or Postico for database inspection

---

## Local Development Setup

### Step 1: Clone Repository & Checkout Branch

```bash
# Clone the repository
git clone https://github.com/your-org/shop_mingchang.git
cd shop_mingchang

# Checkout feature branch
git checkout 001-hualien-meat-shop
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (testing, linting)
pip install -r requirements-dev.txt
```

**Key Dependencies:**
- Django 5.x
- Pillow (image processing)
- psycopg2-binary (PostgreSQL adapter)
- django-environ (environment configuration)
- whitenoise (static files)
- django-imagekit (image optimization)
- pytest, pytest-django, pytest-cov (testing)
- factory-boy (test fixtures)
- playwright (E2E testing)

### Step 4: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
```

**`.env` Configuration (Development):**

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-generate-with-python-secrets
DJANGO_SETTINGS_MODULE=config.settings.development

# Database (SQLite for local dev)
DATABASE_URL=sqlite:///db.sqlite3

# Or use PostgreSQL locally:
# DATABASE_URL=postgresql://username:password@localhost:5432/shop_mingchang

# Email (for contact form notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# Language Settings
LANGUAGE_CODE=zh-hant
TIME_ZONE=Asia/Taipei

# Static & Media Files
STATIC_URL=/static/
MEDIA_URL=/media/

# Security (local dev can be permissive)
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Google Maps API (optional for development)
GOOGLE_MAPS_API_KEY=your-api-key-here
```

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 5: Run Database Migrations

```bash
# Create database tables
python manage.py migrate

# Create superuser for Django admin
python manage.py createsuperuser
# Username: admin
# Email: admin@mingchang.local
# Password: [your choice]
```

### Step 6: Load Initial Data (Optional)

```bash
# Load sample categories and products
python manage.py loaddata fixtures/initial_data.json

# Or create data via Django admin at http://localhost:8000/admin/
```

### Step 7: Collect Static Files

```bash
# Gather static files (CSS, JS, images) for serving
python manage.py collectstatic --no-input
```

### Step 8: Compile Translation Files

```bash
# Generate translation message files
python manage.py makemessages -l zh_Hant
python manage.py makemessages -l en

# Compile translations
python manage.py compilemessages
```

### Step 9: Run Development Server

```bash
# Start Django development server
python manage.py runserver

# Server running at: http://localhost:8000
# Admin panel at: http://localhost:8000/admin/
```

**Verify Setup:**
1. Visit `http://localhost:8000/` - Homepage should load
2. Visit `http://localhost:8000/admin/` - Login with superuser credentials
3. Add a product via admin panel
4. Visit `http://localhost:8000/products/` - Product should appear

---

## Testing Setup

### Run Unit & Integration Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=apps --cov-report=html --cov-report=term

# Run specific test file
pytest apps/shop/tests/test_models.py

# Run tests with verbose output
pytest -v

# Run tests in parallel (faster)
pytest -n auto
```

**Coverage Target:** >80% (constitution requirement)

### Run E2E Tests (Playwright)

```bash
# Install Playwright browsers (first time only)
playwright install

# Run E2E tests
pytest tests/e2e/

# Run with headed browser (see what's happening)
pytest tests/e2e/ --headed

# Run specific browser
pytest tests/e2e/ --browser firefox
```

**E2E Test Scenarios:**
- Browse homepage and navigate to products
- Filter products by category
- View product details
- Submit contact form
- Switch languages
- Test mobile responsive layouts

### Linting & Code Quality

```bash
# Run Black formatter
black apps/ config/ tests/

# Run isort (import sorting)
isort apps/ config/ tests/

# Run Flake8 linter
flake8 apps/ config/ tests/

# Run mypy type checker
mypy apps/ config/
```

---

## Database Management

### Django Admin Panel

**Access**: `http://localhost:8000/admin/`

**Manage:**
- Products (add, edit, delete)
- Categories (organize products)
- Company Info (business details, location)
- Contact Inquiries (view customer messages)
- Orders (Phase 2)

**Admin User Permissions:**
- Shop owners: Staff status + Shop app permissions only
- Developers: Superuser status (full access)

### Database Inspection

**SQLite (Local Development):**
```bash
# Open SQLite shell
sqlite3 db.sqlite3

# Common queries
.tables                          # List all tables
SELECT * FROM shop_product;      # View products
.schema shop_product             # Show table structure
.quit                            # Exit
```

**PostgreSQL (Production/Local):**
```bash
# Connect to database
psql $DATABASE_URL

# Common queries
\dt                              # List tables
\d shop_product                  # Describe table
SELECT * FROM shop_product;      # View products
\q                               # Exit
```

### Migrations

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate app_name 0001
```

---

## Running with Docker (Optional)

### Docker Compose (Local Development)

**docker-compose.yml:**
```yaml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: shop_mingchang
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/shop_mingchang
      DJANGO_SETTINGS_MODULE: config.settings.development
    depends_on:
      - db

volumes:
  postgres_data:
```

**Run with Docker:**
```bash
# Start services
docker-compose up

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser in container
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

---

## Integration Testing Scenarios

### Scenario 1: Browse Products (User Story P1)

**Test Steps:**
1. **Navigate to homepage** → Verify featured products display
2. **Click "Products" menu** → Product listing page loads
3. **Click category filter** (e.g., "Beef") → Product grid updates via HTMX
4. **Click product card** → Product detail page opens
5. **View image gallery** → Thumbnail clicks update main image
6. **Click "About"** → Company info and map display
7. **Switch to English** → All content translates
8. **Switch back to Chinese** → Content reverts

**Expected Results:**
- All pages load within performance targets (<3s TTI)
- HTMX interactions update content without page reload
- Language switching persists across navigation
- Images lazy-load and are optimized (WebP)

**Playwright Test:**
```python
def test_browse_products_flow(page):
    # Navigate to homepage
    page.goto("http://localhost:8000/")
    assert page.title() == "花蓮明昌肉品 - Hualien MingChang Meat Shop"
    
    # Click products link
    page.click('a[href="/products/"]')
    page.wait_for_selector('#product-grid')
    
    # Filter by category
    page.click('button[data-category="beef"]')
    page.wait_for_load_state('networkidle')
    assert 'category=beef' in page.url
    
    # Click first product
    page.click('.product-card:first-child a')
    page.wait_for_selector('.product-detail')
    
    # Verify product details visible
    assert page.query_selector('.product-name')
    assert page.query_selector('.product-price')
    assert page.query_selector('.product-description')
```

---

### Scenario 2: Submit Contact Form (User Story P3)

**Test Steps:**
1. **Navigate to contact page** → Form displays
2. **Fill out form:**
   - Name: "張小明"
   - Phone: "0912-345-678"
   - Email: "test@example.com"
   - Message: "請問澳洲和牛沙朗牛排還有貨嗎？"
3. **Click Submit** → Form submits via HTMX
4. **Verify success message** → Confirmation displays without page reload
5. **Check email** → Confirmation sent to customer, notification to shop owner
6. **Check admin panel** → Contact inquiry appears with status "new"

**Expected Results:**
- Form submission completes within 500ms
- Validation errors display inline (if invalid input)
- Emails sent successfully
- Database record created

**Playwright Test:**
```python
def test_contact_form_submission(page):
    # Navigate to contact page
    page.goto("http://localhost:8000/contact/")
    
    # Fill form
    page.fill('input[name="name"]', "張小明")
    page.fill('input[name="phone"]', "0912-345-678")
    page.fill('input[name="email"]', "test@example.com")
    page.fill('textarea[name="message"]', "請問澳洲和牛沙朗牛排還有貨嗎？")
    
    # Submit form
    page.click('button[type="submit"]')
    
    # Wait for success message
    page.wait_for_selector('.success-message')
    assert "感謝您的留言" in page.inner_text('.success-message')
```

---

### Scenario 3: Mobile Responsive (User Story P2)

**Test Steps:**
1. **Set viewport to mobile** (375x667 - iPhone SE)
2. **Navigate to homepage** → Layout adapts, no horizontal scroll
3. **Open mobile menu** → Hamburger icon toggles menu
4. **Navigate to products** → Product grid stacks vertically
5. **View product detail** → Images are touch-friendly
6. **Tap phone number** → Click-to-call link works
7. **Test on tablet viewport** (768x1024)
8. **Test on desktop** (1920x1080)

**Expected Results:**
- All touch targets >= 44px
- Text readable without zooming
- Images scale appropriately
- Navigation menu collapses on mobile

**Playwright Test:**
```python
@pytest.mark.parametrize("viewport", [
    {"width": 375, "height": 667},   # Mobile
    {"width": 768, "height": 1024},  # Tablet
    {"width": 1920, "height": 1080}  # Desktop
])
def test_responsive_design(page, viewport):
    page.set_viewport_size(viewport)
    page.goto("http://localhost:8000/")
    
    # Verify no horizontal scroll
    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    viewport_width = viewport["width"]
    assert scroll_width <= viewport_width + 1  # Allow 1px tolerance
    
    # Verify content visible
    assert page.is_visible('.hero-section')
    assert page.is_visible('.featured-products')
```

---

### Scenario 4: Language Switching

**Test Steps:**
1. **Navigate to homepage** (defaults to Chinese based on browser)
2. **Click language toggle** → Page content switches to English
3. **Verify URL** → Language prefix added (`/en/`)
4. **Navigate to products** → Maintains English language
5. **Click product** → Product name/description in English
6. **Switch back to Chinese** → All content reverts
7. **Refresh page** → Language persists (cookie-based)

**Expected Results:**
- Language switch occurs within 1 second
- No page flickering or reload
- Cookie set correctly
- All text translates (no mixed languages)

---

## Troubleshooting

### Common Issues

**1. Port 8000 already in use:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Or run on different port
python manage.py runserver 8080
```

**2. Database migration errors:**
```bash
# Reset database (development only!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**3. Static files not loading:**
```bash
# Recollect static files
python manage.py collectstatic --clear --no-input

# Verify STATIC_ROOT in settings
```

**4. Import errors:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**5. Playwright installation issues:**
```bash
# Install Playwright with dependencies
pip install playwright
playwright install --with-deps
```

---

## Deployment to Railway

### Step 1: Create Railway Account

1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub account
3. Link repository

### Step 2: Configure Project

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 3: Add PostgreSQL Service

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Copy `DATABASE_URL` from environment variables

### Step 4: Set Environment Variables

In Railway dashboard, add:
```
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
SECRET_KEY=<generate-secure-key>
DATABASE_URL=<auto-provided-by-railway>
ALLOWED_HOSTS=<your-app>.railway.app
CSRF_TRUSTED_ORIGINS=https://<your-app>.railway.app
```

### Step 5: Deploy

```bash
# Push to GitHub (Railway auto-deploys)
git add .
git commit -m "feat: add Hualien meat shop MVP"
git push origin 001-hualien-meat-shop

# Or deploy via Railway CLI
railway up
```

### Step 6: Run Production Migrations

```bash
# Via Railway dashboard > Shell
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

---

## Constitution Compliance Checklist

**Phase 1 Quickstart Complete** ✅

- [x] **Code Quality**: Virtual environment, linting tools configured
- [x] **Test-First**: pytest setup with >80% coverage target
- [x] **UX Consistency**: Responsive testing across viewports
- [x] **Performance**: Load time verification in integration tests

**Ready for `/speckit.tasks`**: Task breakdown can now proceed.

---

## Next Steps

1. **Generate Tasks**: Run `/speckit.tasks` to create detailed task list
2. **Start Implementation**: Follow TDD workflow (tests first!)
3. **Verify Constitution Compliance**: Check all gates in plan.md
4. **Deploy MVP**: Complete Phase 1 (User Stories P1-P3)
5. **Review with Owners**: Demo to shop owners before Phase 2

---

## Support & Resources

**Documentation:**
- Django: https://docs.djangoproject.com/en/5.0/
- HTMX: https://htmx.org/docs/
- Tailwind CSS: https://tailwindcss.com/docs
- Playwright: https://playwright.dev/python/

**Community:**
- Django Forum: https://forum.djangoproject.com/
- HTMX Discord: https://htmx.org/discord

**Project-Specific:**
- Repository: `https://github.com/your-org/shop_mingchang`
- Issue Tracker: GitHub Issues
- Documentation: `/docs/` directory
- Constitution: `.specify/memory/constitution.md`
