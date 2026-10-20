# 🛍️ HeritageHub — Ethiopia's Artisan Marketplace

> **Premium, AI-powered, multi-vendor e-commerce platform. Crafted for Ethiopia, ready for the world.**

HeritageHub is a production-grade commerce ecosystem combining Ethiopian heritage commerce with modern tech: **FastAPI + Vue 3, real-time WebSockets, AI search, advanced analytics, and local payment rails (Telebirr, Chapa).**

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-2.0-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vue_3-Premium-42b883?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Tailwind-Pro-38bdf8?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-Ready-7c3aed?style=for-the-badge" />
</p>

---

## ✨ What’s New — Professional Upgrade (v2.0)

This release transforms HeritageHub from a starter template into a **sellable product**:

### Frontend Pro Overhaul
- **Design System**: Heritage gold / ink palette, Playfair + Inter, soft shadows, 2xl/3xl radii, motion
- **8 Premium Views**: Home (hero, categories, flash sale, artisan spotlight, testimonials), Shop with filters & pagination, Product detail with gallery & reviews, Cart drawer + Cart page, Checkout (address → payment → confirmation), Wishlist, Orders with live tracking, Profile, Admin analytics
- **Real-time UI**: Live order ticker, WebSocket-ready notifications, optimistic cart, toast system
- **State**: Pinia stores (auth, cart, wishlist, ui), Axios service with interceptors, demo-fallback for offline preview
- **DX**: Vite proxy, `0.0.0.0` preview host, PWA-ready meta, SEO tags, Tailwind v3.4

### Backend Advanced Features
- **Search & Filtering**: `GET /search` with `q`, category, price range, sorting, suggestions & trending
- **Wishlist**: `GET/POST/DELETE /wishlist` with idempotent checks
- **Coupons**: `POST /coupons` + `POST /coupons/validate` (percentage / fixed / free-shipping, expiry, usage limits)
- **Analytics Pro**: `/analytics/overview` + `/analytics/revenue-chart` (daily revenue, AOV, conversion)
- **Notifications**: REST + `WS /notifications/ws/{user_id}` with broadcast manager
- **Middleware**: Request-ID + timing header, in-memory rate limiter (strict for auth), structured logging
- **Pagination Utility**: `PaginatedResponse` reuse across endpoints
- **Models**: `Wishlist`, `Coupon`, `AuditLog` added to Core domain
- **Docs**: Enriched OpenAPI tags, health endpoint with feature list, permissive CORS for preview

---

## 🏗️ Architecture

```
                 HERITAGEHUB
                     │
        ┌────────────┼────────────┐
        │            │            │
    Customers    Vendors       Admin
        └────────────┼────────────┘
                     │
              Commerce Platform (API)
     ┌───────┬───────┼──────┬──────┬──────┐
     │       │       │      │      │      │
  Payments Inventory Orders Delivery AI  Analytics
     └───────┴───────┼──────┴──────┴──────┘
                     │
              Vue 3 + Vite + Pinia
                     │
            Tailwind • WebSockets • PWA
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
cp .env.example .env
# set DATABASE_URL and secrets
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8084
# docs → http://localhost:8084/docs
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev        # http://localhost:5173
npm run build      # production
npm run preview    # http://localhost:4173
```

### Docker

```bash
docker compose up --build
```

---

## 🔌 API Highlights

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Service health + feature flags |
| GET | `/api/products` | List with `q`, `category_id`, `min/max_price`, `sort_by`, `page`, `page_size` |
| GET | `/api/search` | Advanced search + pagination |
| GET | `/api/search/suggestions?q=` | Autocomplete |
| GET | `/api/search/trending` | Trending products |
| GET/POST/DELETE | `/api/wishlist` | Wishlist CRUD |
| GET/POST | `/api/coupons` | Manage coupons (admin) |
| POST | `/api/coupons/validate` | Validate & calculate discount |
| GET | `/api/analytics/overview` | KPI overview |
| GET | `/api/analytics/revenue-chart?days=7` | Daily revenue |
| GET | `/api/notifications` | List notifications |
| WS | `/api/notifications/ws/{user_id}` | Real-time |
| POST | `/api/notifications/send/{user_id}` | Push test |

All responses wrapped in `{ status, message, data }` via `ApiResponse`.

---

## 🎨 Design Tokens

- **Heritage**: `#e67e00` → `#6d2800` (primary)
- **Ink**: `#1a1816` (text), `#f8f7f6` (bg)
- **Radius**: `2xl` / `3xl` / `4xl`
- **Shadow**: `soft` / `lifted` / `glow`
- **Fonts**: Playfair Display (display) + Inter (sans)

---

## 🇪🇹 Ethiopia-Ready

- ETB primary, USD/EUR display
- Telebirr, Chapa, Bank transfer, COD
- Address: Region → City → Sub-City → Woreda
- Next-day delivery in Addis/Bishoftu

---

## 📦 Project Structure (updated)

```
heritage-ecommerce/
├── backend/
│   ├── app/
│   │   ├── api/ (auth, products, cart, orders, payments, wishlist, coupons, search, analytics, notifications_ws, ...)
│   │   ├── models/ (wishlist, coupon, audit_log, ...)
│   │   ├── core/ (pagination, rate_limiter, security, config)
│   │   ├── middleware/ (request_id)
│   │   └── main.py (pro FastAPI with middleware & docs)
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/ (AppHeader, AppFooter, ProductCard, CartDrawer)
│   │   ├── views/ (Home, Shop, Product, Cart, Checkout, Wishlist, Orders, Profile, Admin, Auth)
│   │   ├── stores/ (auth, cart, wishlist, ui)
│   │   ├── services/ (api.ts)
│   │   └── assets/main.css (Tailwind + design system)
│   ├── tailwind.config.js
│   └── vite.config.ts (preview-ready)
└── README.md
```

---

## 🔒 Security

- JWT (HS256, 30d), bcrypt/argon2, rate limiting, request IDs, audit logs, RBAC (ADMIN/CUSTOMER/DELIVERY), CORS, 429 handling

---

## 📈 Roadmap

- [x] Search & AI assistant architecture
- [x] Wishlist + coupons + analytics + realtime
- [x] Professional storefront
- [ ] Vector search (pgvector) & embeddings
- [ ] Vendor payout automation
- [ ] Mobile app (Capacitor)

---

**HeritageHub — Building the future of digital commerce for Ethiopia & beyond.** 🇪🇹
