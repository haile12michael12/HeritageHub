import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCart, addToCart as apiAdd, removeFromCart as apiRemove, decrementCart } from '@/services/api'

export const useCartStore = defineStore('cart', () => {
  const items = ref<any[]>([])
  const total = ref(0)
  const totalQty = ref(0)
  const loading = ref(false)

  const count = computed(() => totalQty.value)

  async function fetch() {
    loading.value = true
    try {
      const res = await getCart()
      const data = res.data || res
      items.value = data.items || []
      total.value = Number(data.totalPrice || 0)
      totalQty.value = data.totalQuantity || 0
    } catch {
      // demo fallback
      // keep existing
    } finally { loading.value = false }
  }
  async function add(productId: number, qty = 1) {
    await apiAdd(productId, qty)
    await fetch()
  }
  async function remove(productId: number) {
    await apiRemove(productId)
    await fetch()
  }
  async function decrement(productId: number) {
    await decrementCart(productId)
    await fetch()
  }

  // local demo cart for preview without backend
  function addLocal(product: any) {
    const found = items.value.find((i: any) => i.product_id === product.id)
    if (found) found.quantity += 1
    else items.value.push({ id: Date.now(), product_id: product.id, product_name: product.name, product_price: product.price, product_image: product.image_url, quantity: 1, subtotal: product.price })
    totalQty.value = items.value.reduce((s, i) => s + i.quantity, 0)
    total.value = items.value.reduce((s, i) => s + Number(i.product_price) * i.quantity, 0)
  }

  return { items, total, totalQty, count, loading, fetch, add, remove, decrement, addLocal }
})
