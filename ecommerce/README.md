# 🛍️ Simple E-commerce Store (Django)

> **CodeAlpha Internship — Task 1: Simple E-commerce Store**  
> A feature-complete, modern, and responsive e-commerce web application built using Python, Django, HTML5, CSS3, and JavaScript with SQLite database, Django Authentication, and an Admin control panel.

---

## 🚀 Key Features

- **🛍️ Product Listing & Catalog**:
  - Grid view of available products with images, titles, pricing, and stock status.
  - Interactive search bar to search products by title, description, or category.
  - Category filter pills for easy 1-click filtering (Electronics, Fashion, Footwear, Home & Kitchen, Stationery).

- **🔎 Product Details Page**:
  - Detailed product view with high-resolution image, category tag, full description, and real-time stock indicator.
  - Dynamic quantity selector (limited to available stock).
  - "Add to Cart" with instantaneous feedback and "Continue Shopping" navigation.
  - Related product recommendations in the same category.
  - Assurance perks (fast dispatch, genuine quality, 7-day returns).

- **🛒 Session-Based Shopping Cart**:
  - Add items, increment/decrement quantities, remove single items, or clear cart.
  - Persistent across navigation using Django sessions.
  - Live cart badge counter in the top navigation bar.
  - Real-time order summary calculation (item counts, subtotal, and free delivery).

- **📦 Checkout & Order Processing**:
  - Shipping address and contact information form with full validation.
  - Real-time stock validation to prevent over-purchasing.
  - Automatic order creation and inventory decrement.
  - Payment method selection (Cash on Delivery / Pay on Delivery demo).
  - Order success confirmation page with detailed summary.

- **🧾 Order History**:
  - "My Orders" customer portal listing past orders with timestamps and totals.
  - Color-coded order status badges (*Pending, Processing, Shipped, Delivered, Cancelled*).
  - Detailed order view showing individual items, quantities, and delivery details.

- **👤 Authentication & User Management**:
  - User registration with validation and automatic login.
  - User login & logout with secure Django password hashing and session management.
  - Dynamic navbar updating based on authenticated state.

- **⚙️ Admin Panel**:
  - Django Admin at `/admin/` for managing products, categories, stock, and orders.
  - Tabular inline for viewing and managing `OrderItem` records inside an `Order`.
  - Search fields, filters by category/status/date, and editable fields (`price`, `stock`, `status`).

- **📱 Clean & Responsive UI**:
  - Custom modern CSS design system with CSS custom properties (variables), cards, badges, and responsive flex/grid layouts.
  - Mobile-friendly responsive navbar and adaptive product grid.

---

## 🏗️ Project Architecture

```text
ecommerce/
│
├── manage.py                       # Django CLI utility
│
├── ecommerce/                      # Project Configuration
│   ├── __init__.py
│   ├── settings.py                 # App settings, DB, static/media, auth
│   ├── urls.py                     # Root URL router
│   ├── wsgi.py
│   └── asgi.py
│
├── store/                          # Main Application
│   ├── migrations/                 # Database migrations
│   ├── management/commands/        # Custom management commands
│   │   └── seed_data.py            # Automated sample data seeder
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py
│   ├── cart.py                     # Session cart business logic
│   ├── context_processors.py       # Cart context processor for templates
│   ├── forms.py                    # Registration, Login, and Checkout forms
│   ├── models.py                   # Product, Order, OrderItem models
│   ├── tests.py                    # Automated test suite (6 passing tests)
│   ├── urls.py                     # Store URL endpoints
│   └── views.py                    # View controllers
│
├── templates/                      # HTML Templates
│   ├── base.html                   # Master layout with navbar & footer
│   ├── store/
│   │   ├── home.html               # Product catalog & hero banner
│   │   ├── product_detail.html     # Product details & related items
│   │   ├── cart.html               # Shopping cart & order preview
│   │   ├── checkout.html           # Shipping form & order checkout
│   │   ├── order_success.html      # Post-checkout confirmation
│   │   ├── order_history.html      # User order list
│   │   └── order_detail.html       # Single order breakdown
│   └── registration/
│       ├── login.html              # User login form
│       └── register.html           # User registration form
│
├── static/                         # Static Assets
│   ├── css/
│   │   └── style.css               # Modern responsive stylesheet
│   └── js/
│       └── script.js               # Client notifications & interactivity
│
├── media/                          # User-uploaded & seeded media
│   └── products/                   # Product images
│
└── db.sqlite3                      # SQLite Database
```

---

## 🗄️ Database Design

```text
User (Django Built-in)
 │
 └──────< Order
             │
             └──────< OrderItem >──── Product
```

### Models

- **Product**:
  - `id`: AutoField (Primary Key)
  - `name`: CharField (max 200)
  - `description`: TextField
  - `price`: DecimalField (max 10 digits, 2 decimal places)
  - `image`: ImageField (uploaded to `products/`)
  - `stock`: PositiveIntegerField
  - `category`: CharField (max 100)
  - `created_at`: DateTimeField (auto_now_add)

- **Order**:
  - `id`: AutoField (Primary Key)
  - `user`: ForeignKey (User, on_delete=CASCADE)
  - `total_amount`: DecimalField
  - `status`: CharField (Pending, Processing, Shipped, Delivered, Cancelled)
  - `full_name`, `email`, `phone`, `shipping_address`, `city`, `postal_code`: Shipping info
  - `created_at`: DateTimeField (auto_now_add)

- **OrderItem**:
  - `id`: AutoField (Primary Key)
  - `order`: ForeignKey (Order, related_name='items')
  - `product`: ForeignKey (Product)
  - `quantity`: PositiveIntegerField
  - `price`: DecimalField (price at the time of purchase)

---

## ⚡ Quick Start & Setup Guide

### 1. Prerequisites
- Python 3.10+ installed
- Git

### 2. Navigate to the Project Root
```bash
cd "ecommerce"
```

### 3. Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies (if not already installed)
```bash
pip install Django pillow
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Populate Sample Data (Optional but Recommended)
Run the built-in seeding command to generate superuser, demo customer, and 9 sample products across multiple categories with images:
```bash
python manage.py seed_data
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full access to Django Admin (`/admin/`) |
| **Customer** | `customer` | `customer123` | Pre-seeded with 1 completed past order |

*(You can also register any new customer account at `/register/`)*

---

## 🧪 Running Automated Tests

Run the full Django test suite verifying all views, cart logic, stock decrements, and checkout processing:

```bash
python manage.py test store
```

Expected output:
```text
Ran 6 tests in ~1.5s
OK
```

---

## 🌐 URL Routes

| URL Pattern | View Name | Description |
|---|---|---|
| `/` | `home` | Store homepage with product grid and category filter |
| `/product/<id>/` | `product_detail` | Detailed view for an individual product |
| `/cart/` | `cart` | View shopping cart items and order summary |
| `/cart/add/<id>/` | `cart_add` | Add product to cart (POST / GET) |
| `/cart/decrement/<id>/` | `cart_decrement` | Decrement product quantity in cart |
| `/cart/remove/<id>/` | `cart_remove` | Remove item from cart |
| `/cart/clear/` | `cart_clear` | Empty the shopping cart |
| `/checkout/` | `checkout` | Checkout shipping form & place order |
| `/order/success/<id>/` | `order_success` | Order confirmation receipt |
| `/orders/` | `order_history` | User order history portal |
| `/orders/<id>/` | `order_detail` | Detailed invoice view of past order |
| `/login/` | `login` | User login |
| `/register/` | `register` | New user registration |
| `/logout/` | `logout` | User sign out |
| `/admin/` | `admin:index` | Django administrative panel |

---

## ☁️ Deploying on Render (render.com)

This project is pre-configured for **1-click deployment on Render** using `render.yaml`, `build.sh`, `gunicorn`, and `whitenoise`.

### Method 1: Blueprint Deployment (Easiest)
1. Sign in to [Render](https://render.com).
2. Go to the **Dashboard** and click **New +** &rarr; **Blueprint**.
3. Connect your GitHub repository: `utkarsharma12/codealpha_Simple-ecommerce-website`.
4. Render automatically reads `render.yaml` and sets up the build and start commands.
5. Click **Apply** to deploy!

### Method 2: Manual Web Service
1. Click **New +** &rarr; **Web Service**.
2. Connect repository `utkarsharma12/codealpha_Simple-ecommerce-website`.
3. Configure the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --chdir ecommerce ecommerce.wsgi:application`
4. In **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `DEBUG`: `False`
   - `SECRET_KEY`: *(Generate a random string or click generate)*
5. Click **Deploy Web Service**.

---

## 📜 Internship Project Details
- **Organization**: [CodeAlpha](https://www.codealpha.tech)
- **Task**: Task 1 — Simple E-commerce Store

