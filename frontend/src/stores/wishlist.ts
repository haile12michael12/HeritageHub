import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getWishlist, addWishlist, removeWishlist } from '@/services/api'

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref<any[]>([])
  const ids = ref<Set<number>>(new Set())

  async function fetch() {
    try {
      const res = await getWishlist()
      items.value = res.data || res || []
      ids.value = new Set(items.value.map((i: any) => i.productId || i.product_id))
    } catch {}
  }
  async function toggle(productId: number) {
    if (ids.value.has(productId)) {
      await removeWishlist(productId)
      ids.value.delete(productId)
    } else {
      await addWishlist(productId)
      ids.value.add(productId)
    }
    await fetch()
  }
  function has(productId: number) { return ids.value.has(productId) }

  // local fallback
  function toggleLocal(productId: number) {
    if (ids.value.has(productId)) ids.value.delete(productId)
    else ids.value.add(productId)
  }

  return { items, ids, fetch, toggle, has, toggleLocal }
})
