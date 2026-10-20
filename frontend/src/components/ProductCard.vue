<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useUiStore } from '@/stores/ui'
const props = defineProps<{ product: any }>()
const cart = useCartStore()
const wishlist = useWishlistStore()
const ui = useUiStore()
function add() {
  cart.addLocal(props.product)
  ui.toast(`Added ${props.product.name} to cart`, 'success')
}
</script>

<template>
  <div class="group relative bg-white rounded-[22px] border border-ink-100 overflow-hidden hover:shadow-lifted hover:-translate-y-1 transition-all duration-300">
    <div class="absolute top-3 left-3 z-10 flex gap-2">
      <span v-if="product.stock_quantity <= 5 && product.stock_quantity > 0" class="px-2.5 py-1 rounded-full bg-amber-500 text-white text-[11px] font-bold">LOW STOCK</span>
      <span v-if="product.stock_quantity === 0" class="px-2.5 py-1 rounded-full bg-ink-900 text-white text-[11px] font-bold">SOLD OUT</span>
      <span v-else-if="product.stock_quantity > 20" class="px-2.5 py-1 rounded-full bg-emerald-600 text-white text-[11px] font-bold">IN STOCK</span>
    </div>
    <button @click="wishlist.toggleLocal(product.id)" class="absolute top-3 right-3 z-10 w-9 h-9 rounded-full bg-white/95 backdrop-blur border border-ink-100 grid place-items-center shadow-soft hover:scale-105 transition">
      <svg class="w-4.5 h-4.5" :class="wishlist.has(product.id) ? 'fill-heritage-600 stroke-heritage-600' : 'stroke-ink-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
    </button>

    <RouterLink :to="`/product/${product.id}`" class="block aspect-[4/3] bg-ink-50 overflow-hidden">
      <img :src="product.image_url || `https://picsum.photos/seed/${product.id}/600/400`" :alt="product.name" class="w-full h-full object-cover group-hover:scale-[1.06] transition duration-700" loading="lazy" />
    </RouterLink>

    <div class="p-4">
      <div class="text-[11px] tracking-widest font-bold text-heritage-600 uppercase">{{ product.category_name || 'Heritage Collection' }}</div>
      <RouterLink :to="`/product/${product.id}`" class="mt-1 line-clamp-1 font-semibold text-ink-900 hover:text-heritage-700 leading-tight">{{ product.name }}</RouterLink>
      <p class="mt-1 text-sm text-ink-500 line-clamp-1">{{ product.description }}</p>

      <div class="mt-3 flex items-center justify-between">
        <div>
          <div class="font-display font-extrabold text-lg text-ink-900">{{ Number(product.price).toLocaleString() }} <span class="text-xs font-sans font-bold text-ink-500">ETB</span></div>
          <div class="text-xs text-ink-400 line-through" v-if="product.compare_at">{{ Number(product.compare_at).toLocaleString() }} ETB</div>
        </div>
        <button @click="add" :disabled="product.stock_quantity===0" class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-semibold hover:bg-ink-800 disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg> Add
        </button>
      </div>

      <div class="mt-3 flex items-center gap-1.5 text-xs text-ink-500">
        <span class="flex text-amber-400">★★★★★</span>
        <span class="font-medium">{{ (product.rating || 4.8).toFixed(1) }}</span>
        <span>({{ product.reviews_count || 24 }} reviews)</span>
        <span class="ml-auto w-2 h-2 rounded-full bg-emerald-500"></span> Verified
      </div>
    </div>
  </div>
</template>
