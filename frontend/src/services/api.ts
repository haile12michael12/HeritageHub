import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8084/api',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('heritage_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  config.headers['X-Request-ID'] = Math.random().toString(36).slice(2, 8)
  return config
})

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('heritage_token')
      // don't redirect on login page itself
    }
    return Promise.reject(err)
  }
)

export default api

// Helpers
export const getProducts = (params: any = {}) => api.get('/products', { params }).then(r => r.data)
export const getProduct = (id: number) => api.get(`/products/${id}`).then(r => r.data)
export const getCategories = () => api.get('/categories').then(r => r.data)
export const searchProducts = (params: any) => api.get('/search', { params }).then(r => r.data)
export const getTrending = () => api.get('/search/trending').then(r => r.data)
export const getSuggestions = (q: string) => api.get('/search/suggestions', { params: { q } }).then(r => r.data)
export const getWishlist = () => api.get('/wishlist').then(r => r.data)
export const addWishlist = (product_id: number) => api.post('/wishlist/add', { productId: product_id }).then(r => r.data)
export const removeWishlist = (product_id: number) => api.delete(`/wishlist/${product_id}`).then(r => r.data)
export const getCart = () => api.get('/cart').then(r => r.data)
export const addToCart = (product_id: number, quantity = 1) => api.post('/cart/add', { productId: product_id, quantity }).then(r => r.data)
export const removeFromCart = (product_id: number) => api.delete(`/cart/remove/${product_id}`).then(r => r.data)
export const decrementCart = (product_id: number) => api.post(`/cart/decrement/${product_id}`).then(r => r.data)
export const checkout = () => api.post('/orders/checkout').then(r => r.data)
export const myOrders = () => api.get('/orders/me').then(r => r.data)
export const validateCoupon = (code: string, order_amount: number) => api.post('/coupons/validate', { code, orderAmount: order_amount }).then(r => r.data)
export const analyticsOverview = () => api.get('/analytics/overview').then(r => r.data)
export const revenueChart = (days = 7) => api.get('/analytics/revenue-chart', { params: { days } }).then(r => r.data)
