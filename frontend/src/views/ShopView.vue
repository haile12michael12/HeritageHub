<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '@/components/ProductCard.vue'
import api from '@/services/api'

const route = useRoute()
const products = ref<any[]>([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = 12
const filters = ref({
  q: (route.query.q as string) || '',
  category_id: route.query.category ? Number(route.query.category) : undefined,
  min_price: undefined as number | undefined,
  max_price: undefined as number | undefined,
  sort_by: (route.query.sort as string) || 'newest',
})

const demo = [
  { id: 101, name: 'Ethiopian Sidamo Coffee — 500g', description: 'Single-origin, floral & bright', price: 890, stock_quantity: 42, image_url: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&q=80' },
  { id: 102, name: 'Handwoven Netela Scarf', description: 'Cotton tibeb border', price: 1450, stock_quantity: 18, image_url: 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80' },
  { id: 103, name: 'Kebero Ceramic Vase Set', description: 'Glazed terracotta, set of 3', price: 2200, stock_quantity: 7, image_url: 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=600&q=80' },
  { id: 104, name: 'Silver Cross Pendant — Axum', description: 'Hand-hammered sterling', price: 3200, stock_quantity: 15, image_url: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80' },
  { id: 105, name: 'Buna Coffee Ceremony Set', description: 'Jebena + 6 cups + incense', price: 1850, stock_quantity: 3, image_url: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80' },
  { id: 106, name: 'Gabi Cotton Blanket', description: 'Extra-large, natural dye', price: 2750, stock_quantity: 22, image_url: 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=600&q=80' },
  { id: 107, name: 'Brass Coffee Grinder — Vintage', description: 'Manual, adjustable burr', price: 1650, stock_quantity: 0, image_url: 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600&q=80' },
  { id: 108, name: 'Shepherd Leather Satchel', description: 'Full-grain leather', price: 4200, stock_quantity: 11, image_url: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80' },
]

async function fetch() {
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: pageSize, ...filters.value }
    // clean undefined
    Object.keys(params).forEach(k => params[k] === undefined || params[k]==='' ? delete params[k] : null)
    const res = await api.get('/products', { params })
    const data = res.data?.data || res.data
    const items = data?.items || data || []
    if (Array.isArray(items) && items.length) {
      products.value = items
      total.value = data?.total || items.length
    } else {
      // search filtering on demo
      let list = demo
      if (filters.value.q) list = list.filter(p => p.name.toLowerCase().includes(filters.value.q.toLowerCase()))
      if (filters.value.min_price) list = list.filter(p => p.price >= filters.value.min_price!)
      if (filters.value.max_price) list = list.filter(p => p.price <= filters.value.max_price!)
      products.value = list
      total.value = list.length
    }
  } catch {
    products.value = demo
    total.value = demo.length
  } finally { loading.value = false }
}

onMounted(fetch)
watch(() => route.query, (q) => {
  filters.value.q = (q.q as string) || ''
  filters.value.category_id = q.category ? Number(q.category) : undefined
  if (q.sort) filters.value.sort_by = q.sort as string
  fetch()
})
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Breadcrumb -->
      <div class="text-xs text-ink-500 flex items-center gap-2"><RouterLink to="/" class="hover:text-ink-700">Home</RouterLink><span>/</span><span class="font-semibold text-ink-900">Shop</span><span class="ml-auto hidden sm:inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-ink-200 text-xs"><span class="w-2 h-2 bg-emerald-500 rounded-full"></span> {{ total }} products • Updated live</span></div>

      <div class="mt-4 grid lg:grid-cols-[260px_1fr] gap-6">
        <!-- Filters -->
        <aside class="hidden lg:block">
          <div class="sticky top-[88px] space-y-4">
            <div class="rounded-[22px] bg-white border border-ink-100 p-5 shadow-soft">
              <h3 class="font-bold">Filters</h3>
              <div class="mt-4 space-y-4">
                <div>
                  <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Search</div>
                  <input v-model="filters.q" @keydown.enter="fetch()" placeholder="AI: e.g. gift under 2000 ETB" class="input mt-2 text-sm" />
                  <button @click="fetch()" class="btn-primary w-full mt-2 py-2.5 text-sm">Search</button>
                </div>
                <div>
                  <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Price Range (ETB)</div>
                  <div class="mt-2 grid grid-cols-2 gap-2">
                    <input v-model.number="filters.min_price" type="number" placeholder="Min" class="input text-sm" />
                    <input v-model.number="filters.max_price" type="number" placeholder="Max" class="input text-sm" />
                  </div>
                  <button @click="fetch()" class="w-full mt-2 py-2 rounded-full border border-ink-200 text-sm font-semibold hover:bg-ink-50">Apply</button>
                </div>
                <div>
                  <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Category</div>
                  <div class="mt-2 space-y-1 text-sm">
                    <label class="flex items-center gap-2"><input type="radio" :value="undefined" v-model="filters.category_id" @change="fetch()" /> All</label>
                    <label class="flex items-center gap-2"><input type="radio" :value="1" v-model="filters.category_id" @change="fetch()" /> Coffee</label>
                    <label class="flex items-center gap-2"><input type="radio" :value="2" v-model="filters.category_id" @change="fetch()" /> Textiles</label>
                    <label class="flex items-center gap-2"><input type="radio" :value="3" v-model="filters.category_id" @change="fetch()" /> Ceramics</label>
                    <label class="flex items-center gap-2"><input type="radio" :value="4" v-model="filters.category_id" @change="fetch()" /> Jewelry</label>
                  </div>
                </div>
                <div class="rounded-2xl bg-gradient-to-br from-heritage-50 to-heritage-100 border border-heritage-200 p-4">
                  <div class="text-xs font-bold text-heritage-700">HERITAGE AI</div>
                  <p class="text-sm mt-1 leading-5">Try: “Show me a laptop for programming under 50,000 ETB” — AI converts to filters automatically.</p>
                </div>
              </div>
            </div>
            <div class="rounded-[22px] bg-ink-900 text-white p-5">
              <div class="text-sm font-bold">Need help choosing?</div>
              <p class="text-sm text-white/70 mt-1">Chat with our artisan concierge.</p>
              <button class="mt-3 w-full py-2.5 rounded-full bg-white text-ink-900 font-bold text-sm">Open Chat</button>
            </div>
          </div>
        </aside>

        <!-- Listing -->
        <div>
          <div class="flex flex-wrap items-center gap-3 bg-white rounded-full border border-ink-100 p-2 shadow-soft">
            <div class="px-4 text-sm font-semibold">{{ total }} results <span class="text-ink-400 hidden sm:inline">• Page {{ page }}</span></div>
            <div class="ml-auto flex items-center gap-2">
              <span class="text-xs font-bold tracking-widest uppercase text-ink-500 hidden sm:inline">Sort:</span>
              <select v-model="filters.sort_by" @change="fetch()" class="px-3 py-2 rounded-full bg-ink-50 border border-ink-200 text-sm">
                <option value="newest">Newest</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="popular">Most Popular</option>
              </select>
            </div>
          </div>

          <div v-if="loading" class="mt-6 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            <div v-for="i in 6" :key="i" class="h-[320px] rounded-[22px] bg-white border border-ink-100 animate-pulse"></div>
          </div>
          <div v-else class="mt-6 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            <ProductCard v-for="p in products" :key="p.id" :product="p" />
          </div>
          <div v-if="!loading && !products.length" class="mt-12 text-center">
            <p class="font-semibold">No products found</p>
            <p class="text-sm text-ink-500">Try adjusting filters or search.</p>
          </div>

          <div class="mt-8 flex justify-center gap-2">
            <button @click="page=Math.max(1,page-1); fetch()" :disabled="page===1" class="px-4 py-2 rounded-full border border-ink-200 disabled:opacity-40">← Prev</button>
            <span class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-bold">{{ page }}</span>
            <button @click="page+=1; fetch()" :disabled="products.length < pageSize" class="px-4 py-2 rounded-full border border-ink-200 disabled:opacity-40">Next →</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
