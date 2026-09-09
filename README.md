# 🛍️ Heritage Ecommerce

> **Modern AI-powered, multi-vendor e-commerce platform built with FastAPI and Vue.js**

Heritage Ecommerce is a scalable and production-ready e-commerce platform designed to provide a complete digital shopping experience for customers, vendors, administrators, and delivery agents.

The platform combines **modern e-commerce functionality, multi-vendor marketplace capabilities, secure payments, inventory management, delivery tracking, analytics, real-time communication, and AI-powered shopping features**.

---

## 🚀 Project Overview

Heritage Ecommerce is designed as a complete commerce ecosystem:

```text
                         HERITAGE ECOMMERCE
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
         Customers           Vendors            Admin
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                         Commerce Platform
                                │
          ┌─────────────┬───────┼────────┬─────────────┐
          │             │       │        │             │
       Payments      Inventory Orders  Delivery       AI
          │             │       │        │             │
          └─────────────┴───────┼────────┴─────────────┘
                                │
                         Analytics & Security
```

---

# ✨ Key Features

## 👤 Customer Features

* User registration and authentication
* Email verification
* Password reset
* Social authentication
* User profile
* Multiple delivery addresses
* Product browsing
* Product search
* Advanced filtering
* Product categories
* Product variants
* Product comparison
* Wishlist
* Recently viewed products
* Related products
* Frequently bought together
* Personalized recommendations
* Product reviews
* Verified purchase reviews
* Product questions and answers
* Price-drop notifications
* Back-in-stock notifications

---

# 🛒 Advanced Shopping Cart

* Guest cart
* Persistent cart
* Cart synchronization
* Cart merge after login
* Quantity management
* Stock validation
* Save for later
* Coupon application
* Automatic discounts
* Shipping calculation
* Tax calculation
* Abandoned-cart detection

### Cart Flow

```text
Product
   ↓
Add to Cart
   ↓
Cart Validation
   ↓
Coupon / Discount
   ↓
Shipping
   ↓
Checkout
```

---

# 💳 Payment System

Heritage Ecommerce uses a flexible payment architecture that allows multiple payment providers.

### Supported Payment Architecture

```text
                    Payment Service
                          │
           ┌──────────────┼──────────────┐
           │              │              │
        Stripe         Local Bank      Wallet
           │              │              │
           └──────────────┼──────────────┘
                          │
                   Payment Transaction
```

### Features

* Payment processing
* Payment verification
* Payment webhooks
* Payment transaction history
* Failed payment handling
* Payment retry
* Refunds
* Partial refunds
* Payment status tracking
* Cash on delivery
* Bank transfer support
* Ethiopian payment gateway integration

---

# 📦 Order Management

Complete order lifecycle:

```text
Pending
   ↓
Confirmed
   ↓
Processing
   ↓
Packed
   ↓
Shipped
   ↓
Out for Delivery
   ↓
Delivered
```

### Order Features

* Create order
* Order history
* Order details
* Order tracking
* Order cancellation
* Return requests
* Exchange requests
* Refund requests
* Partial refunds
* Order timeline
* Invoice generation
* PDF invoice
* Customer order notifications

---

# 🏪 Multi-Vendor Marketplace

Vendors can operate their own stores inside Heritage Ecommerce.

### Vendor Features

* Vendor registration
* Vendor verification
* Store profile
* Product management
* Product variants
* Inventory management
* Order management
* Customer management
* Coupon management
* Sales analytics
* Revenue reports
* Commission tracking
* Withdrawal requests
* Vendor ratings
* Vendor reviews

### Vendor Architecture

```text
Vendor
  │
  ├── Store
  ├── Products
  ├── Orders
  ├── Customers
  ├── Inventory
  ├── Coupons
  ├── Reviews
  ├── Analytics
  ├── Commissions
  └── Payouts
```

---

# 📦 Inventory Management

Heritage Ecommerce supports advanced inventory management.

### Features

* SKU management
* Product variants
* Multiple warehouses
* Stock tracking
* Reserved stock
* Available stock
* Low-stock alerts
* Stock adjustments
* Stock transfers
* Stock movement history
* Inventory audit
* Purchase orders

### Inventory Structure

```text
Product
   ↓
Variant
   ↓
Warehouse
   ↓
Inventory
   ↓
Stock Movement
```

---

# 🚚 Delivery & Logistics

Dedicated delivery management system.

### Delivery Agent Features

* Delivery agent accounts
* Assigned deliveries
* Delivery dashboard
* Order details
* Customer information
* Delivery status updates
* Delivery proof
* Customer signature
* Delivery photo
* Failed delivery reasons
* Delivery history

### Delivery Tracking

```text
Order Created
      ↓
Warehouse
      ↓
Packed
      ↓
Shipped
      ↓
Delivery Agent
      ↓
Out for Delivery
      ↓
Customer
      ↓
Delivered
```

---

# 🤖 AI-Powered Features

Heritage Ecommerce includes an AI-ready architecture.

### AI Product Recommendations

The recommendation engine can use:

* Browsing history
* Purchase history
* Wishlist
* Product interactions
* Categories
* Similar products

```text
Customer Behavior
       ↓
Recommendation Engine
       ↓
AI Processing
       ↓
Personalized Products
```

### AI Shopping Assistant

Customers can search using natural language.

Example:

```text
"Show me a laptop for programming
under 50,000 ETB with 16GB RAM."
```

The system can convert the request into structured product filters.

### Other AI Features

* AI product search
* Personalized recommendations
* Similar-product recommendations
* Smart upselling
* Smart cross-selling
* Review sentiment analysis
* Product description generation
* Customer behavior analysis

---

# 🔎 Advanced Search

* Full-text search
* Search suggestions
* Typo tolerance
* Product filters
* Category filtering
* Brand filtering
* Price filtering
* Rating filtering
* Availability filtering
* Search history
* Popular searches
* Search analytics
* Zero-result tracking

Future-ready search architecture:

```text
Vue.js
   ↓
FastAPI
   ↓
Search Service
   ↓
PostgreSQL / OpenSearch
   ↓
Products
```

---

# 🔔 Notification System

Central notification architecture supporting:

* In-app notifications
* Email notifications
* SMS notifications
* Push notifications

### Events

* Order placed
* Payment successful
* Order shipped
* Order delivered
* Refund completed
* Product back in stock
* Price dropped
* New promotion
* Vendor notification
* Admin notification

---

# 💬 Customer Support

Built-in support system.

### Features

* Support tickets
* Ticket categories
* Priority management
* Ticket assignment
* Support agents
* Internal notes
* Attachments
* Customer messages
* Ticket history
* SLA tracking

---

# 💬 Real-Time Communication

FastAPI WebSockets can be used for real-time functionality.

### Real-Time Features

* Live order status
* Delivery updates
* Real-time notifications
* Customer support chat
* Vendor notifications
* Live inventory updates
* Admin notifications

---

# 🎟️ Promotion Engine

Advanced promotional rules:

```text
IF
Customer = New
AND
Cart > 2,000 ETB

THEN
Discount = 10%
```

### Promotion Types

* Percentage discount
* Fixed discount
* Buy X Get Y
* Free shipping
* Category discount
* Product discount
* Vendor discount
* First-order discount
* Flash sales
* Coupon codes
* Usage limits
* Expiration dates

---

# 🛡️ Security

Security is a core part of the platform.

### Authentication

* JWT authentication
* Access tokens
* Refresh tokens
* Token rotation
* Password hashing
* Email verification
* Password reset
* OAuth
* Optional 2FA
* Session management
* Login history

### Role-Based Access Control

```text
SUPER_ADMIN
     │
ADMIN
     │
 ┌───┼───────────────┐
 │   │               │
Vendor Support   Delivery Agent
 │
Customer
```

### Permission Examples

```text
product.create
product.read
product.update
product.delete

order.read
order.update
order.refund

vendor.verify
vendor.suspend

user.create
user.update
user.delete
```

---

# 🚨 Fraud Detection

The platform can assign a risk score to suspicious orders.

Example:

```text
Order #10025

Risk Score: 82 / 100

Reasons:
✓ New account
✓ High-value order
✓ Multiple failed payments
✓ Different billing/shipping address

Status:
Manual Review
```

---

# 📊 Admin Dashboard

The administration panel provides complete control.

### Admin Modules

```text
Dashboard
├── Users
├── Vendors
├── Products
├── Categories
├── Brands
├── Orders
├── Payments
├── Refunds
├── Inventory
├── Warehouses
├── Deliveries
├── Coupons
├── Promotions
├── Reviews
├── Support
├── Notifications
├── Analytics
├── CMS
├── Audit Logs
└── Settings
```

### Analytics

* Revenue
* Orders
* Customers
* Vendors
* Products
* Profit
* Refunds
* Conversion rate
* Average order value
* Customer growth
* Top products
* Top vendors
* Top categories
* Sales by location
* Payment methods

---

# 📈 Analytics & Event Tracking

Heritage Ecommerce can track customer behavior.

### Events

```text
product_view
search
add_to_cart
remove_from_cart
wishlist_added
checkout_started
payment_started
purchase_completed
review_created
```

### Business Metrics

```text
Conversion Rate
Cart Abandonment Rate
Average Order Value
Customer Lifetime Value
Repeat Purchase Rate
Revenue Growth
```

---

# 🇪🇹 Ethiopia-Ready Features

Heritage Ecommerce is designed to support the Ethiopian market.

### Currency

```text
ETB
USD
EUR
```

### Ethiopian Payment Integration

The payment layer is designed to support local providers such as:

* Telebirr
* Chapa
* Bank transfer
* Other local payment providers

### Ethiopian Address Structure

```text
Region
   ↓
City
   ↓
Sub-City
   ↓
Woreda
   ↓
Delivery Area
```

---

# 📱 Progressive Web App

The frontend can be configured as a PWA.

Features:

* Installable web application
* Mobile-first interface
* Push notifications
* Offline caching
* Fast loading
* Add to home screen
* Responsive checkout

---

# 🏗️ Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* Celery / background workers
* JWT
* Pydantic
* WebSockets
* REST API

## Frontend

* Vue.js
* Vite
* JavaScript / TypeScript
* Pinia
* Vue Router
* Axios
* Tailwind CSS

## Infrastructure

* Docker
* Docker Compose
* Nginx
* PostgreSQL
* Redis
* Object Storage
* CI/CD

## AI

Architecture can support:

* LLM APIs
* Local AI models
* Embedding models
* Vector database
* Recommendation engine
* Semantic search

---

# 📁 Project Structure

```text
heritage-ecommerce/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── products.py
│   │   │       ├── categories.py
│   │   │       ├── cart.py
│   │   │       ├── checkout.py
│   │   │       ├── orders.py
│   │   │       ├── payments.py
│   │   │       ├── vendors.py
│   │   │       ├── inventory.py
│   │   │       ├── delivery.py
│   │   │       ├── reviews.py
│   │   │       ├── coupons.py
│   │   │       ├── notifications.py
│   │   │       ├── support.py
│   │   │       └── analytics.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── workers/
│   │   ├── events/
│   │   ├── middleware/
│   │   ├── core/
│   │   └── main.py
│   │
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── views/
│   │   │   ├── customer/
│   │   │   ├── admin/
│   │   │   ├── vendor/
│   │   │   └── delivery/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── composables/
│   │   ├── router/
│   │   ├── types/
│   │   └── utils/
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── docker/
├── nginx/
├── docs/
├── scripts/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 🗄️ Core Database Entities

```text
users
roles
permissions
user_roles
role_permissions

products
product_variants
product_images
categories
brands
attributes
attribute_values

warehouses
inventories
stock_movements

carts
cart_items
wishlists

orders
order_items
order_addresses
order_status_history

payments
payment_transactions
refunds

vendors
vendor_products
vendor_commissions
vendor_payouts

coupons
promotions
promotion_products

reviews
review_images

shipments
delivery_agents
delivery_tracking

notifications
notification_preferences

support_tickets
support_messages

search_history
product_views
analytics_events

audit_logs
```

---

# ⚙️ Installation

## 1. Clone the Project

```bash
git clone <repository-url>

cd heritage-ecommerce
```

---

# Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```bash
cp .env.example .env
```

Configure:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/heritage_ecommerce

REDIS_URL=redis://localhost:6379

SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=30

STRIPE_SECRET_KEY=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
```

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

```bash
cd frontend

npm install
```

Create:

```text
.env
```

Example:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Run development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🐳 Docker

Run the complete development environment:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

Rebuild:

```bash
docker compose up --build
```

---

# 🧪 Testing

Backend:

```bash
pytest
```

Frontend:

```bash
npm run test
```

Build:

```bash
npm run build
```

---

# 🔐 API Architecture

```text
Vue.js
   │
   │ HTTPS / REST
   ↓
Nginx
   │
   ↓
FastAPI
   │
   ├── Authentication
   ├── Product Service
   ├── Cart Service
   ├── Order Service
   ├── Payment Service
   ├── Vendor Service
   ├── Inventory Service
   ├── Delivery Service
   ├── Notification Service
   ├── Analytics Service
   └── AI Service
          │
          ├── PostgreSQL
          ├── Redis
          └── Vector Database
```

---

# 🔄 Background Jobs

Redis + worker architecture can handle:

* Emails
* Notifications
* Payment processing
* Abandoned carts
* Inventory alerts
* Recommendation calculations
* Report generation
* Invoice generation
* Scheduled promotions

```text
FastAPI
   ↓
Redis Queue
   ↓
Background Worker
   ↓
Task
```

---

# 🚀 Development Roadmap

## Phase 1 — Foundation

* [ ] Project architecture
* [ ] Database
* [ ] Authentication
* [ ] RBAC
* [ ] API versioning
* [ ] Error handling
* [ ] Logging

## Phase 2 — Commerce

* [ ] Products
* [ ] Categories
* [ ] Variants
* [ ] Search
* [ ] Filters
* [ ] Wishlist
* [ ] Reviews
* [ ] Cart

## Phase 3 — Checkout

* [ ] Addresses
* [ ] Shipping
* [ ] Payments
* [ ] Orders
* [ ] Refunds
* [ ] Invoices

## Phase 4 — Marketplace

* [ ] Vendors
* [ ] Vendor dashboard
* [ ] Vendor products
* [ ] Commissions
* [ ] Payouts

## Phase 5 — Logistics

* [ ] Warehouses
* [ ] Delivery agents
* [ ] Shipments
* [ ] Delivery tracking
* [ ] Delivery dashboard

## Phase 6 — Admin

* [ ] Admin dashboard
* [ ] Analytics
* [ ] Inventory
* [ ] Promotions
* [ ] CMS
* [ ] Audit logs

## Phase 7 — AI

* [ ] AI search
* [ ] Recommendations
* [ ] Shopping assistant
* [ ] Sentiment analysis
* [ ] Smart upselling

## Phase 8 — Real-Time

* [ ] WebSockets
* [ ] Live notifications
* [ ] Chat
* [ ] Live inventory
* [ ] Live order tracking

## Phase 9 — Production

* [ ] Docker
* [ ] Redis
* [ ] Background workers
* [ ] Nginx
* [ ] CI/CD
* [ ] Monitoring
* [ ] Backups
* [ ] Security hardening

---

# 🌟 Vision

Heritage Ecommerce aims to become more than a traditional online store.

The long-term vision is to provide an integrated commerce platform combining:

```text
                 HERITAGE
                    │
       ┌────────────┼────────────┐
       │            │            │
   Marketplace   Payments    Logistics
       │            │            │
       └────────────┼────────────┘
                    │
                   AI
                    │
             Analytics
                    │
             Local Commerce
```

The platform is designed to be scalable from a single online store to a complete **multi-vendor marketplace serving customers and businesses across Ethiopia and beyond**.

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-feature

git add .

git commit -m "feat: add new feature"

git push origin feature/new-feature
```

Then create a Pull Request.

---

# 📄 License

This project is intended for educational, portfolio, and commercial development purposes.

Add your preferred license before production deployment.

---

# 👨‍💻 Author

**Heritage Ecommerce Development Team**

Built with:

```text
Python + FastAPI
Vue.js + Vite
PostgreSQL
Redis
Docker
AI
```

---

# ⭐ Project Status

```text
████████████████████░░  Advanced Development

Backend        ███████████████░░░
Frontend       ███████████████░░░
Marketplace    ███████████░░░░░░
Payments       ██████████░░░░░░░
AI             ███████░░░░░░░░░░
Analytics      █████████░░░░░░░░
Logistics      ████████░░░░░░░░░
```

> **Heritage Ecommerce — Building the future of digital commerce.**
