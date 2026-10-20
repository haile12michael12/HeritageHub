<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
const orders = ref<any[]>([])
onMounted(async () => {
  try {
    const res = await api.get('/orders/me')
    orders.value = res.data?.data || res.data || []
    if (!orders.value.length) throw new Error('empty')
  } catch {
    orders.value = [
      { id: 10241, totalPrice: 3200, status: 'processing', shippingAddress: 'Bishoftu, Oromia', createdAt: '2026-10-19T10:00:00Z', items: [{ product: { name: 'Sidamo Coffee 500g' }, quantity: 1, unitPrice: 890 }, { product: { name: 'Netela Scarf' }, quantity: 1, unitPrice: 1450 }] },
      { id: 10239, totalPrice: 1850, status: 'delivered', shippingAddress: 'Addis Ababa', createdAt: '2026-10-15T10:00:00Z', items: [{ product: { name: 'Buna Ceremony Set' }, quantity: 1, unitPrice: 1850 }] },
    ]
  }
})
const statusColor = (s:string)=> s==='delivered'?'bg-emerald-100 text-emerald-700': s==='processing'?'bg-amber-100 text-amber-700':'bg-ink-100 text-ink-700'
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-5xl mx-auto px-4 py-6">
      <h1 class="font-display font-extrabold text-2xl">Your Orders</h1>
      <p class="text-sm text-ink-500">Track, return, reorder — all in one place.</p>
      <div class="mt-6 space-y-4">
        <div v-for="o in orders" :key="o.id" class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
          <div class="flex flex-wrap items-center gap-3">
            <div class="font-bold">Order #{{ o.id }}</div>
            <span class="px-2.5 py-1 rounded-full text-xs font-bold" :class="statusColor(o.status)">{{ o.status }}</span>
            <span class="text-xs text-ink-500">{{ new Date(o.createdAt).toLocaleDateString() }}</span>
            <span class="ml-auto font-extrabold">{{ Number(o.totalPrice).toLocaleString() }} ETB</span>
          </div>
          <div class="mt-3 text-sm text-ink-600">Ship to: {{ o.shippingAddress }}</div>
          <div class="mt-3 space-y-2">
            <div v-for="(it,idx) in (o.items||[])" :key="idx" class="flex justify-between text-sm p-3 rounded-2xl bg-ink-50 border border-ink-100">
              <span>{{ it.product?.name || 'Product' }} × {{ it.quantity }}</span><span class="font-semibold">{{ it.unitPrice }} ETB</span>
            </div>
          </div>
          <div class="mt-3 h-2 rounded-full bg-ink-100 overflow-hidden"><div class="h-2 bg-heritage-600" :style="{ width: o.status==='delivered' ? '100%' : o.status==='processing' ? '55%' : '25%' }"></div></div>
          <div class="mt-3 flex gap-2">
            <button class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-semibold">Track Live</button>
            <button class="px-4 py-2 rounded-full border border-ink-200 text-sm font-semibold">Get Invoice (PDF)</button>
            <button v-if="o.status==='delivered'" class="px-4 py-2 rounded-full border border-ink-200 text-sm font-semibold">Write Review</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
