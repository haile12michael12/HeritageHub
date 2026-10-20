<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import CartDrawer from '@/components/CartDrawer.vue'
import { useUiStore } from '@/stores/ui'
const ui = useUiStore()
</script>

<template>
  <div class="min-h-screen flex flex-col bg-[#fffaf0]">
    <AppHeader />
    <main class="flex-1">
      <RouterView />
    </main>
    <AppFooter />
    <CartDrawer />

    <!-- Toasts -->
    <div class="fixed bottom-4 right-4 z-50 space-y-2">
      <div v-for="t in ui.toasts" :key="t.id" class="px-4 py-3 rounded-2xl shadow-lifted border text-sm font-semibold flex items-center gap-2"
        :class="t.type==='success' ? 'bg-emerald-600 text-white border-emerald-700' : t.type==='error' ? 'bg-red-600 text-white' : 'bg-ink-900 text-white'">
        <span>{{ t.message }}</span>
      </div>
    </div>

    <!-- Live notif demo -->
    <div class="fixed top-[88px] left-1/2 -translate-x-1/2 z-40 hidden md:flex items-center gap-2 px-4 py-2 rounded-full bg-ink-900 text-white text-xs font-semibold shadow-lifted">
      <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span> Live: Order #10242 shipped to Bishoftu • Tracking updated via WebSocket
    </div>
  </div>
</template>
