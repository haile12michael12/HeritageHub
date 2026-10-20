import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ShopView from '../views/ShopView.vue'
import ProductView from '../views/ProductView.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import AuthView from '../views/AuthView.vue'
import AdminView from '../views/AdminView.vue'
import WishlistView from '../views/WishlistView.vue'
import OrdersView from '../views/OrdersView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() { return { top: 0 } },
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/shop', name: 'shop', component: ShopView },
    { path: '/product/:id', name: 'product', component: ProductView },
    { path: '/cart', name: 'cart', component: CartView },
    { path: '/checkout', name: 'checkout', component: CheckoutView },
    { path: '/wishlist', name: 'wishlist', component: WishlistView },
    { path: '/orders', name: 'orders', component: OrdersView },
    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/login', name: 'login', component: AuthView, props: { mode: 'login' } },
    { path: '/register', name: 'register', component: AuthView, props: { mode: 'register' } },
    { path: '/admin', name: 'admin', component: AdminView },
    { path: '/about', name: 'about', component: () => import('../views/AboutView.vue') },
  ],
})

export default router
