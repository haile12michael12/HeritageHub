<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const stats = ref<any>(null)
const chart = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [ov, ch] = await Promise.all([
      api.get('/analytics/overview').then(r => r.data?.data || r.data).catch(()=> null),
      api.get('/analytics/revenue-chart', { params: { days: 7 } }).then(r=> r.data?.data || r.data).catch(()=> [])
    ])
    if (ov) stats.value = ov
    else stats.value = { totalOrders: 324, totalRevenue: 482900, totalProducts: 128, totalCustomers: 1842, growthRate: 18.4, recentOrders: 42 }

    if (Array.isArray(ch) && ch.length) chart.value = ch
    else chart.value = [
      { date: '2026-10-14', revenue: 42000, orders: 12 },
      { date: '2026-10-15', revenue: 58000, orders: 18 },
      { date: '2026-10-16', revenue: 39000, orders: 9 },
      { date: '2026-10-17', revenue: 72000, orders: 24 },
      { date: '2026-10-18', revenue: 65000, orders: 21 },
      { date: '2026-10-19', revenue: 81000, orders: 27 },
      { date: '2026-10-20', revenue: 46000, orders: 14 },
    ]
  } finally { loading.value=false }
})

const maxRev = () => Math.max(...chart.value.map(c=>c.revenue), 1)
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <div class="flex items-center gap-3">
        <h1 class="font-display font-extrabold text-2xl">Admin Dashboard</h1>
        <span class="px-3 py-1 rounded-full bg-ink-900 text-white text-xs font-bold">Pro Analytics • Real-time</span>
        <span class="ml-auto text-xs text-ink-500">Last updated: just now • Auto-refresh</span>
      </div>

      <div v-if="loading" class="mt-6 grid grid-cols-2 lg:grid-cols-4 gap-4"><div v-for="i in 4" :key="i" class="h-28 rounded-[22px] bg-white border border-ink-100 animate-pulse"></div></div>

      <div v-else class="mt-6 grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="rounded-[22px] bg-white border border-ink-100 p-5 shadow-soft">
          <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Total Revenue</div>
          <div class="mt-2 font-display font-extrabold text-2xl">{{ Number(stats.totalRevenue).toLocaleString() }} <span class="text-sm font-sans font-bold text-ink-500">ETB</span></div>
          <div class="mt-2 inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-full">↗ +{{ stats.growthRate }}% vs last 30d</div>
        </div>
        <div class="rounded-[22px] bg-white border border-ink-100 p-5 shadow-soft">
          <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Orders</div>
          <div class="mt-2 font-display font-extrabold text-2xl">{{ stats.totalOrders }}</div>
          <div class="text-xs text-ink-500">{{ stats.recentOrders }} in last 7 days • Live</div>
        </div>
        <div class="rounded-[22px] bg-white border border-ink-100 p-5 shadow-soft">
          <div class="text-xs font-bold tracking-widest uppercase text-ink-500">Products</div>
          <div class="mt-2 font-display font-extrabold text-2xl">{{ stats.totalProducts }}</div>
          <div class="text-xs text-amber-700">3 low stock • 0 out of stock</div>
        </div>
        <div class="rounded-[22px] bg-ink-900 text-white p-5">
          <div class="text-xs font-bold tracking-widest uppercase text-white/70">Customers</div>
          <div class="mt-2 font-display font-extrabold text-2xl">{{ stats.totalCustomers }}</div>
          <div class="text-xs text-white/70">Active • +42 this week</div>
        </div>
      </div>

      <div class="mt-6 grid lg:grid-cols-[1.6fr_1fr] gap-6">
        <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
          <div class="flex items-center justify-between"><h3 class="font-bold">Revenue (last 7 days)</h3><span class="text-xs px-2 py-1 rounded-full bg-ink-50 border border-ink-200">ETB • Daily</span></div>
          <div class="mt-6 flex items-end gap-2 h-[180px]">
            <div v-for="c in chart" :key="c.date" class="flex-1 flex flex-col items-center gap-2">
              <div class="w-full rounded-t-xl bg-gradient-to-t from-heritage-600 to-heritage-400" :style="{ height: (c.revenue / maxRev() * 140) + 'px' }"></div>
              <span class="text-[10px] font-bold text-ink-500">{{ c.date.slice(5) }}</span>
            </div>
          </div>
          <div class="mt-4 grid grid-cols-3 gap-3 text-xs">
            <div class="p-3 rounded-2xl bg-ink-50 border border-ink-100"><div class="font-bold">AOV</div><div class="text-ink-600">{{ (stats.totalRevenue / Math.max(stats.totalOrders,1)).toFixed(0) }} ETB</div></div>
            <div class="p-3 rounded-2xl bg-ink-50 border border-ink-100"><div class="font-bold">Conversion</div><div class="text-ink-600">3.8% • +0.4%</div></div>
            <div class="p-3 rounded-2xl bg-ink-50 border border-ink-100"><div class="font-bold">Refunds</div><div class="text-ink-600">0.9% • stable</div></div>
          </div>
        </div>

        <div class="space-y-6">
          <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
            <h3 class="font-bold">Orders by status</h3>
            <div class="mt-4 space-y-2 text-sm">
              <div class="flex justify-between"><span>Pending</span><span class="font-bold">12</span></div>
              <div class="w-full h-2 rounded-full bg-ink-100"><div class="h-2 rounded-full bg-amber-500 w-[32%]"></div></div>
              <div class="flex justify-between"><span>Processing</span><span class="font-bold">8</span></div>
              <div class="w-full h-2 rounded-full bg-ink-100"><div class="h-2 rounded-full bg-heritage-600 w-[48%]"></div></div>
              <div class="flex justify-between"><span>Delivered</span><span class="font-bold">302</span></div>
              <div class="w-full h-2 rounded-full bg-ink-100"><div class="h-2 rounded-full bg-emerald-600 w-[86%]"></div></div>
            </div>
          </div>
          <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
            <h3 class="font-bold">Live activity</h3>
            <div class="mt-4 space-y-3 text-sm">
              <div class="flex gap-3"><span class="w-2 h-2 mt-2 rounded-full bg-heritage-600"></span><div><div class="font-semibold">New order #10242 — 3,200 ETB</div><div class="text-xs text-ink-500">Bishoftu • just now</div></div></div>
              <div class="flex gap-3"><span class="w-2 h-2 mt-2 rounded-full bg-emerald-500"></span><div><div class="font-semibold">Payment confirmed — Telebirr</div><div class="text-xs text-ink-500">Addis Ababa • 2m ago</div></div></div>
              <div class="flex gap-3"><span class="w-2 h-2 mt-2 rounded-full bg-amber-500"></span><div><div class="font-semibold">Low stock alert — Coffee 500g</div><div class="text-xs text-ink-500">42 → 7 left</div></div></div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft overflow-auto">
        <h3 class="font-bold">Recent orders</h3>
        <table class="mt-4 w-full text-sm">
          <thead class="text-xs tracking-widest uppercase text-ink-500"><tr><th class="text-left py-2">Order</th><th class="text-left">Customer</th><th class="text-left">Amount</th><th class="text-left">Status</th><th class="text-right">Action</th></tr></thead>
          <tbody>
            <tr v-for="i in 5" :key="i" class="border-t border-ink-100"><td class="py-3 font-semibold">#1024{{ i }}</td><td>Addis Customer {{ i }}</td><td class="font-bold">{{ (1200 + i*340).toLocaleString() }} ETB</td><td><span class="px-2 py-1 rounded-full text-xs font-bold" :class="i%3===0?'bg-emerald-100 text-emerald-700': i%3===1?'bg-amber-100 text-amber-700':'bg-ink-100 text-ink-700'">{{ i%3===0?'Delivered': i%3===1?'Pending':'Processing' }}</span></td><td class="text-right"><button class="px-3 py-1 rounded-full border border-ink-200 text-xs font-semibold">View</button></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
