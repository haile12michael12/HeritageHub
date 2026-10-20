<script setup lang="ts">
import { useWishlistStore } from '@/stores/wishlist'
import ProductCard from '@/components/ProductCard.vue'
const wishlist = useWishlistStore()
const demo = [
  { id: 102, name: 'Handwoven Netela Scarf', description: 'Cotton tibeb border', price: 1450, stock_quantity: 18, image_url: 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80' },
  { id: 104, name: 'Silver Cross Pendant — Axum', description: 'Hand-hammered sterling', price: 3200, stock_quantity: 15, image_url: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80' },
]
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <h1 class="font-display font-extrabold text-2xl">Wishlist</h1>
      <p class="text-sm text-ink-500">Save favorites • Get price-drop alerts</p>
      <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <ProductCard v-for="p in demo" :key="p.id" :product="p" />
      </div>
      <div class="mt-8 rounded-[22px] bg-white border border-ink-100 p-6">
        <h3 class="font-bold">Wishlist benefits</h3>
        <ul class="mt-2 text-sm text-ink-600 list-disc ml-5"><li>Back-in-stock notifications</li><li>Price-drop alerts</li><li>Share with friends & family</li></ul>
      </div>
    </div>
  </div>
</template>
