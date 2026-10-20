<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useUiStore } from '@/stores/ui'
import api from '@/services/api'

const route = useRoute()
const product = ref<any>(null)
const qty = ref(1)
const activeImg = ref(0)
const related = ref<any[]>([])
const cart = useCartStore()
const ui = useUiStore()

const demo = {
  id: 101,
  name: 'Ethiopian Sidamo Coffee — 500g',
  description: 'Single-origin beans from the highlands of Sidamo. Washed process, floral aroma with citrus finish. Roasted in small batches in Addis Ababa and nitrogen-sealed. Perfect for pour-over, French press or traditional Jebena.',
  price: 890,
  stock_quantity: 42,
  category_name: 'Artisan Coffee',
  image_url: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=900&q=80',
  images: [
    'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=900&q=80',
    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=900&q=80',
    'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=900&q=80',
  ],
  rating: 4.9,
  reviews: [
    { id: 1, rating: 5, comment: 'Best coffee I have had outside Yirgacheffe! Fast delivery to Bishoftu.', username: 'Meron T.', createdAt: '2026-10-10' },
    { id: 2, rating: 5, comment: 'Authentic taste, reminds me of my grandmother’s Buna.', username: 'Abel K.', createdAt: '2026-10-08' },
  ]
}

onMounted(async () => {
  const id = Number(route.params.id)
  try {
    const res = await api.get(`/products/${id}`)
    product.value = res.data?.data || res.data || null
    if (!product.value || !product.value.name) product.value = { ...demo, id }
  } catch {
    product.value = { ...demo, id }
  }
  related.value = [
    { id: 102, name: 'Handwoven Netela Scarf', description: 'Cotton tibeb border', price: 1450, stock_quantity: 18, image_url: 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80', rating: 4.8 },
    { id: 103, name: 'Kebero Ceramic Vase Set', description: 'Glazed terracotta, set of 3', price: 2200, stock_quantity: 7, image_url: 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=600&q=80', rating: 4.9 },
    { id: 105, name: 'Buna Coffee Ceremony Set', description: 'Jebena + 6 cups + incense', price: 1850, stock_quantity: 3, image_url: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80', rating: 4.7 },
  ]
})

function addToCart() {
  cart.addLocal(product.value)
  for (let i=1;i<qty.value;i++) cart.addLocal(product.value)
  ui.toast(`Added ${qty.value}× ${product.value.name} to cart`, 'success')
  ui.cartOpen = true
}
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <div class="text-xs text-ink-500 flex items-center gap-2"><RouterLink to="/" class="hover:text-ink-700">Home</RouterLink><span>/</span><RouterLink to="/shop" class="hover:text-ink-700">Shop</RouterLink><span>/</span><span class="font-semibold text-ink-900 line-clamp-1">{{ product?.name }}</span></div>

      <div v-if="!product" class="mt-8 h-96 rounded-[22px] bg-white border border-ink-100 animate-pulse"></div>

      <div v-else class="mt-6 grid lg:grid-cols-2 gap-6">
        <!-- Gallery -->
        <div>
          <div class="rounded-[22px] overflow-hidden bg-white border border-ink-100 shadow-soft aspect-[4/3]">
            <img :src="(product.images ? (product.images[activeImg] ?? demo.images[0]) : (product.image_url || demo.images[0])) as string" class="w-full h-full object-cover" />
          </div>
          <div class="mt-3 grid grid-cols-3 gap-3">
            <button v-for="(img, i) in (product.images || demo.images)" :key="i" @click="activeImg = Number(i)" class="rounded-2xl overflow-hidden border-2" :class="activeImg===Number(i) ? 'border-heritage-600' : 'border-ink-100'"><img :src="img as string" class="w-full h-24 object-cover" /></button>
          </div>
          <div class="mt-4 rounded-2xl bg-white border border-ink-100 p-4 flex items-center gap-3 text-sm">
            <span class="w-8 h-8 rounded-full bg-emerald-50 grid place-items-center">✓</span> <span class="font-semibold">Free returns within 14 days</span><span class="ml-auto text-ink-500">Ships from Addis • Next-day to Bishoftu</span>
          </div>
        </div>

        <!-- Details -->
        <div>
          <div class="inline-flex px-3 py-1 rounded-full bg-heritage-100 text-heritage-800 text-xs font-bold tracking-widest uppercase">{{ product.category_name || product.category?.name || 'Heritage Collection' }}</div>
          <h1 class="mt-2 font-display font-extrabold text-[28px] leading-tight">{{ product.name }}</h1>
          <div class="mt-2 flex items-center gap-2 text-sm"><span class="text-amber-400">★★★★★</span><span class="font-bold">{{ product.rating || 4.9 }}</span><span class="text-ink-500">({{ product.reviews?.length || 42 }} reviews) • {{ product.stock_quantity }} in stock</span><span class="ml-auto px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">● Verified artisan</span></div>

          <div class="mt-4 rounded-[22px] bg-white border border-ink-100 p-5 shadow-soft">
            <div class="flex items-baseline gap-3">
              <div class="font-display font-extrabold text-3xl">{{ Number(product.price).toLocaleString() }} <span class="text-sm font-sans font-bold text-ink-500">ETB</span></div>
              <span class="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold">Save 19%</span>
              <span class="text-sm text-ink-400 line-through">{{ (Number(product.price)*1.25).toFixed(0) }} ETB</span>
            </div>
            <p class="mt-3 text-sm leading-6 text-ink-600">{{ product.description }}</p>

            <div class="mt-5 flex items-center gap-3">
              <div class="flex items-center gap-2 px-2 py-1.5 rounded-full bg-ink-50 border border-ink-200">
                <button @click="qty=Math.max(1,qty-1)" class="w-8 h-8 rounded-full bg-white border border-ink-200 grid place-items-center">−</button>
                <span class="w-8 text-center font-bold">{{ qty }}</span>
                <button @click="qty++" class="w-8 h-8 rounded-full bg-white border border-ink-200 grid place-items-center">+</button>
              </div>
              <button @click="addToCart" class="flex-1 btn-primary py-3.5">Add to Cart — {{ (Number(product.price)*Number(qty)).toLocaleString() }} ETB</button>
              <button class="w-12 h-12 rounded-full bg-white border border-ink-200 grid place-items-center">♡</button>
            </div>

            <div class="mt-4 grid grid-cols-3 gap-2 text-xs">
              <div class="rounded-2xl bg-ink-50 p-3 text-center"><div class="font-bold">Telebirr</div><div class="text-ink-500">Pay on delivery</div></div>
              <div class="rounded-2xl bg-ink-50 p-3 text-center"><div class="font-bold">Chapa</div><div class="text-ink-500">Secure checkout</div></div>
              <div class="rounded-2xl bg-ink-50 p-3 text-center"><div class="font-bold">Stripe</div><div class="text-ink-500">Cards & wallet</div></div>
            </div>

            <div class="mt-4 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 p-4 flex gap-3">
              <span class="text-xl">🎟️</span>
              <div class="flex-1">
                <div class="text-sm font-bold">Use code HERITAGE10 for 10% off</div>
                <div class="text-xs text-ink-600">Min 2,000 ETB • Valid until Oct 30</div>
              </div>
              <button class="px-4 py-2 rounded-full bg-ink-900 text-white text-xs font-bold">Copy</button>
            </div>
          </div>

          <!-- Delivery estimator -->
          <div class="mt-4 rounded-[22px] bg-white border border-ink-100 p-5">
            <h3 class="font-bold">Delivery to Bishoftu</h3>
            <div class="mt-3 space-y-2 text-sm">
              <div class="flex justify-between"><span class="text-ink-500">Standard (1–2 days)</span><span class="font-bold">Free over 2,000 ETB</span></div>
              <div class="flex justify-between"><span class="text-ink-500">Express (today)</span><span class="font-bold">150 ETB</span></div>
              <div class="h-px bg-ink-100 my-2"></div>
              <div class="flex items-center gap-2 text-emerald-700 font-semibold"><span class="w-2 h-2 bg-emerald-500 rounded-full"></span> In stock • Ships today if ordered within 3h 12m</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews -->
      <div class="mt-8 grid lg:grid-cols-[1fr_340px] gap-6">
        <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
          <h3 class="font-display font-bold text-xl">Customer reviews</h3>
          <div class="mt-4 flex gap-6">
            <div class="text-center"><div class="font-display font-extrabold text-4xl">4.9</div><div class="text-amber-400">★★★★★</div><div class="text-xs text-ink-500">42 reviews</div></div>
            <div class="flex-1 space-y-1">
              <div v-for="i in 5" :key="i" class="flex items-center gap-2 text-xs"><span class="w-6">{{ 6-i }}★</span><div class="flex-1 h-2 rounded-full bg-ink-100"><div class="h-2 rounded-full bg-heritage-600" :style="{ width: i===1 ? '84%' : i===2 ? '12%' : '4%' }"></div></div><span class="w-8 text-ink-500">{{ i===1 ? '36' : i===2 ? '5' : '1' }}</span></div>
            </div>
          </div>
          <div class="mt-6 space-y-4">
            <div v-for="r in (product.reviews || demo.reviews)" :key="r.id" class="rounded-2xl bg-ink-50 border border-ink-100 p-4">
              <div class="flex items-center gap-2"><span class="text-amber-400 text-sm">{{ '★'.repeat(r.rating) }}</span><span class="font-semibold text-sm">{{ r.username }}</span><span class="ml-auto text-xs text-ink-500">Verified purchase</span></div>
              <p class="mt-2 text-sm leading-6">{{ r.comment }}</p>
            </div>
          </div>
        </div>
        <div class="rounded-[22px] bg-ink-900 text-white p-6">
          <h3 class="font-bold">Frequently bought together</h3>
          <div class="mt-4 space-y-3">
            <div v-for="p in related.slice(0,2)" :key="p.id" class="flex gap-3 p-3 rounded-2xl bg-white/10 border border-white/10">
              <img :src="p.image_url" class="w-14 h-14 rounded-xl object-cover" />
              <div class="flex-1"><div class="text-sm font-semibold leading-tight">{{ p.name }}</div><div class="text-sm font-bold">{{ p.price }} ETB</div></div>
              <button @click="cart.addLocal(p); ui.toast('Added to cart','success')" class="px-3 py-1.5 rounded-full bg-white text-ink-900 text-xs font-bold">+ Add</button>
            </div>
          </div>
          <button class="mt-4 w-full py-3 rounded-full bg-heritage-600 font-bold">Add both to cart</button>
        </div>
      </div>
    </div>
  </div>
</template>
