<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import api from '@/services/api'

const trending = ref<any[]>([])
const categories = ref([
  { id: 1, name: 'Artisan Coffee', count: '128 products', image: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&q=80', color: 'from-amber-600 to-orange-700' },
  { id: 2, name: 'Handwoven Textiles', count: '96 products', image: 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80', color: 'from-rose-500 to-pink-700' },
  { id: 3, name: 'Ceramics & Pottery', count: '74 products', image: 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=600&q=80', color: 'from-teal-600 to-cyan-800' },
  { id: 4, name: 'Heritage Jewelry', count: '112 products', image: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80', color: 'from-amber-500 to-yellow-700' },
])

const demoProducts = ref([
  { id: 101, name: 'Ethiopian Sidamo Coffee — 500g', description: 'Single-origin, floral & bright — roasted in Addis', price: 890, stock_quantity: 42, category_name: 'Coffee', image_url: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&q=80', rating: 4.9, reviews_count: 128 },
  { id: 102, name: 'Handwoven Netela Scarf', description: 'Cotton tibeb border, made by Women Weavers Co-op', price: 1450, stock_quantity: 18, category_name: 'Textiles', image_url: 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80', rating: 4.8, reviews_count: 64 },
  { id: 103, name: 'Kebero Ceramic Vase Set', description: 'Glazed terracotta, set of 3 — Lalibela artisan', price: 2200, stock_quantity: 7, category_name: 'Ceramics', image_url: 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=600&q=80', rating: 4.9, reviews_count: 41 },
  { id: 104, name: 'Silver Cross Pendant — Axum', description: 'Hand-hammered sterling, heritage design', price: 3200, stock_quantity: 15, category_name: 'Jewelry', image_url: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80', rating: 5.0, reviews_count: 89 },
  { id: 105, name: 'Buna Coffee Ceremony Set', description: 'Jebena + 6 cups + incense burner — complete', price: 1850, stock_quantity: 3, category_name: 'Coffee', image_url: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80', rating: 4.7, reviews_count: 56 },
  { id: 106, name: 'Gabi Cotton Blanket', description: 'Extra-large, natural dye, Addis Ababa market', price: 2750, stock_quantity: 22, category_name: 'Textiles', image_url: 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=600&q=80', rating: 4.8, reviews_count: 33 },
  { id: 107, name: 'Brass Coffee Grinder — Vintage', description: 'Manual, adjustable burr, heirloom quality', price: 1650, stock_quantity: 0, category_name: 'Artisan', image_url: 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600&q=80', rating: 4.9, reviews_count: 72 },
  { id: 108, name: 'Shepherd Leather Satchel', description: 'Full-grain leather, brass buckles, Addis-made', price: 4200, stock_quantity: 11, category_name: 'Accessories', image_url: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80', rating: 4.8, reviews_count: 19 },
])

onMounted(async () => {
  try {
    const res = await api.get('/products')
    const data = res.data?.data || res.data
    const items = data?.items || data || []
    if (Array.isArray(items) && items.length) trending.value = items.slice(0, 8)
    else trending.value = demoProducts.value
  } catch {
    trending.value = demoProducts.value
  }
})
</script>

<template>
  <div class="bg-[#fffaf0]">
    <!-- HERO -->
    <section class="max-w-7xl mx-auto px-4 pt-6">
      <div class="relative overflow-hidden rounded-[28px] bg-gradient-to-br from-ink-900 via-ink-800 to-heritage-900 text-white">
        <div class="absolute inset-0 opacity-20" style="background-image: radial-gradient(circle at 20% 20%, #f5a623 0%, transparent 50%), radial-gradient(circle at 80% 80%, #e67e00 0%, transparent 50%);"></div>
        <div class="absolute -right-24 -top-24 w-[420px] h-[420px] rounded-full bg-heritage-500/20 blur-3xl"></div>
        <div class="relative grid lg:grid-cols-2 gap-0">
          <div class="p-8 lg:p-12">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 text-xs font-bold tracking-widest uppercase">★ Trusted by 12k+ Ethiopians</div>
            <h1 class="mt-4 font-display font-extrabold text-[38px] lg:text-[48px] leading-[0.95] tracking-tight">
              Heritage<br />crafted for<br /><span class="text-heritage-300">your home.</span>
            </h1>
            <p class="mt-4 text-[15px] leading-6 text-white/80 max-w-md">Discover authentic Ethiopian artisan goods — coffee, textiles, ceramics & jewelry — with local payments, next-day delivery in Addis, and AI-curated recommendations.</p>
            <div class="mt-6 flex flex-wrap gap-3">
              <RouterLink to="/shop" class="px-7 py-3.5 rounded-full bg-white text-ink-900 font-bold hover:bg-ink-50 transition">Shop Collections →</RouterLink>
              <RouterLink to="/shop?q=coffee" class="px-7 py-3.5 rounded-full bg-white/10 border border-white/20 font-semibold hover:bg-white/15 transition">Explore Coffee</RouterLink>
            </div>
            <div class="mt-7 flex items-center gap-6 text-sm">
              <div class="flex -space-x-2"><img v-for="i in 4" :key="i" :src="`https://i.pravatar.cc/100?img=${i+10}`" class="w-8 h-8 rounded-full border-2 border-ink-900" /></div>
              <div><div class="font-bold">4.9/5 from 2,431 reviews</div><div class="text-white/70 text-xs">Verified buyers • Real artisans</div></div>
            </div>
          </div>
          <div class="relative min-h-[340px] lg:min-h-[460px] bg-gradient-to-br from-heritage-400/30 to-transparent">
            <img src="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=900&q=80" alt="Ethiopian coffee ceremony" class="absolute inset-0 w-full h-full object-cover mix-blend-luminosity opacity-90" />
            <div class="absolute inset-0 bg-gradient-to-t from-ink-900/40 via-transparent to-transparent"></div>
            <!-- floating card -->
            <div class="absolute bottom-4 left-4 right-4 lg:left-auto lg:right-6 lg:w-[320px] bg-white rounded-2xl p-4 shadow-lifted text-ink-900">
              <div class="flex gap-3">
                <img src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=200&q=80" class="w-16 h-16 rounded-xl object-cover" />
                <div class="flex-1">
                  <div class="text-xs font-bold tracking-widest text-heritage-600 uppercase">Today's pick</div>
                  <div class="font-semibold leading-tight">Sidamo Single-Origin — Floral notes</div>
                  <div class="text-sm font-extrabold">890 ETB <span class="text-xs font-normal text-ink-400 line-through">1,100 ETB</span></div>
                </div>
              </div>
              <div class="mt-3 flex items-center gap-2 text-xs">
                <span class="px-2 py-1 rounded-full bg-emerald-50 text-emerald-700 font-semibold">● In stock • Ships today</span>
                <span class="ml-auto text-ink-500">★★★★★ 4.9</span>
              </div>
            </div>
          </div>
        </div>
        <!-- trust bar inside hero -->
        <div class="relative border-t border-white/10 bg-ink-900/40 backdrop-blur">
          <div class="grid grid-cols-2 lg:grid-cols-4 divide-x divide-white/10">
            <div class="px-6 py-4 flex items-center gap-3"><span class="w-9 h-9 rounded-full bg-white/10 grid place-items-center">🚚</span><div><div class="text-sm font-bold">Next-day delivery</div><div class="text-xs text-white/70">Addis Ababa • Major cities</div></div></div>
            <div class="px-6 py-4 flex items-center gap-3"><span class="w-9 h-9 rounded-full bg-white/10 grid place-items-center">💳</span><div><div class="text-sm font-bold">Pay your way</div><div class="text-xs text-white/70">Telebirr • Chapa • COD</div></div></div>
            <div class="px-6 py-4 hidden lg:flex items-center gap-3"><span class="w-9 h-9 rounded-full bg-white/10 grid place-items-center">🤖</span><div><div class="text-sm font-bold">AI Shopping Assistant</div><div class="text-xs text-white/70">“Find me gift under 2k”</div></div></div>
            <div class="px-6 py-4 hidden lg:flex items-center gap-3"><span class="w-9 h-9 rounded-full bg-white/10 grid place-items-center">🛡️</span><div><div class="text-sm font-bold">Buyer protection</div><div class="text-xs text-white/70">Verified artisans only</div></div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- CATEGORIES -->
    <section class="max-w-7xl mx-auto px-4 mt-8">
      <div class="flex items-end justify-between">
        <h2 class="font-display font-extrabold text-[26px] tracking-tight">Shop by heritage</h2>
        <RouterLink to="/shop" class="text-sm font-semibold text-heritage-700 hover:text-heritage-800">View all →</RouterLink>
      </div>
      <div class="mt-4 grid grid-cols-2 lg:grid-cols-4 gap-4">
        <RouterLink v-for="c in categories" :key="c.id" :to="`/shop?category=${c.id}`" class="group relative overflow-hidden rounded-[22px] h-[180px] border border-ink-100 shadow-soft hover:shadow-lifted transition">
          <img :src="c.image" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-700" />
          <div class="absolute inset-0 bg-gradient-to-t from-ink-900/80 via-ink-900/20 to-transparent"></div>
          <div class="absolute bottom-0 p-4 text-white">
            <div class="font-display font-bold text-lg leading-none">{{ c.name }}</div>
            <div class="text-xs text-white/80 mt-1">{{ c.count }}</div>
            <span class="mt-2 inline-flex items-center gap-1 text-xs font-bold bg-white text-ink-900 px-3 py-1.5 rounded-full">Explore →</span>
          </div>
        </RouterLink>
      </div>
    </section>

    <!-- FEATURED -->
    <section class="max-w-7xl mx-auto px-4 mt-10">
      <div class="flex flex-wrap items-center gap-3">
        <h2 class="font-display font-extrabold text-[26px]">Featured & trending</h2>
        <span class="px-3 py-1 rounded-full bg-heritage-100 text-heritage-800 text-xs font-bold">AI Curated</span>
        <div class="ml-auto flex gap-2">
          <RouterLink to="/shop?sort=popular" class="px-4 py-2 rounded-full bg-white border border-ink-200 text-sm font-semibold hover:bg-ink-50">Best sellers</RouterLink>
          <RouterLink to="/shop?sort=newest" class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-semibold">New in</RouterLink>
        </div>
      </div>
      <div class="mt-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <ProductCard v-for="p in (trending.length ? trending : demoProducts)" :key="p.id" :product="p" />
      </div>
    </section>

    <!-- PROMO STRIP -->
    <section class="max-w-7xl mx-auto px-4 mt-8">
      <div class="grid lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2 relative overflow-hidden rounded-[22px] bg-gradient-to-br from-heritage-600 to-heritage-800 p-6 text-white">
          <div class="absolute -right-12 -top-12 w-64 h-64 rounded-full bg-white/10 blur-2xl"></div>
          <div class="relative flex gap-4">
            <div class="flex-1">
              <div class="inline-flex px-3 py-1 rounded-full bg-white text-heritage-700 text-xs font-extrabold">FLASH SALE • 48H ONLY</div>
              <h3 class="mt-3 font-display font-extrabold text-2xl leading-tight">Coffee ceremony<br />bundle — Save 30%</h3>
              <p class="mt-2 text-sm text-white/80">Jebena + 6 Sini + incense — everything for a perfect Buna.</p>
              <RouterLink to="/shop?q=buna" class="mt-4 inline-flex px-5 py-2.5 rounded-full bg-white text-ink-900 font-bold text-sm">Claim offer →</RouterLink>
            </div>
            <img src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&q=80" class="hidden sm:block w-40 h-40 rounded-2xl object-cover shadow-lifted" />
          </div>
        </div>
        <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
          <div class="text-xs font-bold tracking-widest text-heritage-600 uppercase">Artisan spotlight</div>
          <div class="mt-2 flex gap-3">
            <img src="https://i.pravatar.cc/100?img=32" class="w-12 h-12 rounded-full object-cover" />
            <div><div class="font-bold">Alem's Weaving Co-op</div><div class="text-sm text-ink-500">Addis Ababa • 12 years crafting</div></div>
          </div>
          <p class="mt-3 text-sm text-ink-600 leading-6">“Every Netela carries a story — we use natural dyes and patterns passed from our grandmothers.”</p>
          <RouterLink to="/shop?category=2" class="mt-4 inline-flex text-sm font-bold text-heritage-700">Visit store →</RouterLink>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS & NEWSLETTER -->
    <section class="max-w-7xl mx-auto px-4 mt-8 grid lg:grid-cols-3 gap-4 pb-10">
      <div class="lg:col-span-2 rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
        <h3 class="font-display font-bold text-xl">Loved by heritage keepers</h3>
        <div class="mt-4 grid sm:grid-cols-3 gap-4">
          <div v-for="i in 3" :key="i" class="rounded-2xl bg-ink-50 p-4 border border-ink-100">
            <div class="text-amber-400 text-sm">★★★★★</div>
            <p class="mt-2 text-sm leading-6 text-ink-700">“Authentic, fast delivery to Bishoftu. My guests always ask where I got the coffee set.” — Sara, Bishoftu</p>
            <div class="mt-3 flex items-center gap-2"><img :src="`https://i.pravatar.cc/100?img=${i+20}`" class="w-7 h-7 rounded-full" /><span class="text-xs font-semibold">Verified buyer</span><span class="ml-auto text-xs text-emerald-600">● Delivered</span></div>
          </div>
        </div>
      </div>
      <div class="rounded-[22px] bg-ink-900 text-white p-6">
        <h3 class="font-display font-bold text-xl leading-tight">Get 10% off<br />your first order</h3>
        <p class="mt-2 text-sm text-white/70">Join 8,400+ heritage lovers. Weekly drops, artisan stories & ETB deals.</p>
        <div class="mt-4 flex gap-2">
          <input placeholder="Your email" class="flex-1 px-4 py-3 rounded-full bg-white text-ink-900 text-sm outline-none" />
          <button class="px-6 py-3 rounded-full bg-heritage-600 font-bold text-sm hover:bg-heritage-700">Join</button>
        </div>
        <p class="mt-2 text-xs text-white/50">No spam. Unsubscribe anytime. By joining you agree to Terms.</p>
      </div>
    </section>
  </div>
</template>
