<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()
const ui = useUiStore()
const search = ref('')
function onSearch() {
  if (!search.value.trim()) return
  router.push({ name: 'shop', query: { q: search.value } })
}
</script>

<template>
  <header class="sticky top-0 z-40 bg-white/90 backdrop-blur-xl border-b border-ink-100">
    <!-- Top bar -->
    <div class="bg-ink-900 text-ink-100 text-xs">
      <div class="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <span class="hidden sm:inline-flex items-center gap-2"><span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span> Free delivery on orders over 2,000 ETB</span>
          <span class="hidden md:inline">🇪🇹 Made for Ethiopia — ETB • USD • EUR</span>
        </div>
        <div class="flex items-center gap-3">
          <span class="hidden sm:inline">Need help? +251 911 000 000</span>
          <span class="w-px h-3 bg-white/20 hidden sm:block"></span>
          <a href="#" class="hover:text-white">Track Order</a>
        </div>
      </div>
    </div>

    <!-- Main nav -->
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center gap-6 py-3.5">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-3 shrink-0">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-heritage-600 to-heritage-800 grid place-items-center text-white font-display font-extrabold text-lg shadow-glow">H</div>
          <div class="leading-none">
            <div class="font-display font-extrabold text-[18px] tracking-tight text-ink-900">HeritageHub</div>
            <div class="text-[11px] tracking-[0.14em] font-semibold text-heritage-600 uppercase -mt-0.5">Commerce • ET</div>
          </div>
        </RouterLink>

        <!-- Categories (desktop) -->
        <div class="hidden lg:flex items-center gap-1 ml-2">
          <RouterLink to="/shop" class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-semibold hover:bg-ink-800">Shop All →</RouterLink>
          <RouterLink to="/shop?category=1" class="px-3.5 py-2 rounded-full hover:bg-ink-50 text-sm font-medium">Artisan</RouterLink>
          <RouterLink to="/shop?category=2" class="px-3.5 py-2 rounded-full hover:bg-ink-50 text-sm font-medium">Textiles</RouterLink>
          <RouterLink to="/shop?category=3" class="px-3.5 py-2 rounded-full hover:bg-ink-50 text-sm font-medium">Ceramics</RouterLink>
          <RouterLink to="/shop?category=4" class="hidden xl:inline px-3.5 py-2 rounded-full hover:bg-ink-50 text-sm font-medium">Jewelry</RouterLink>
        </div>

        <!-- Search -->
        <div class="flex-1 max-w-xl hidden md:block">
          <div class="relative">
            <input v-model="search" @keydown.enter="onSearch" placeholder="Search for coffee, baskets, scarves… (AI suggests)" class="w-full h-11 pl-11 pr-12 rounded-full bg-ink-50 border border-ink-200 focus:bg-white focus:border-heritage-500 focus:ring-2 focus:ring-heritage-500/20 outline-none transition text-sm" />
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            <button @click="onSearch" class="absolute right-1.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-heritage-600 text-white grid place-items-center hover:bg-heritage-700 transition">→</button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-1 ml-auto">
          <RouterLink to="/wishlist" class="relative w-10 h-10 grid place-items-center rounded-full hover:bg-ink-50 transition">
            <svg class="w-5 h-5 text-ink-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
          </RouterLink>

          <button @click="ui.cartOpen = true" class="relative w-10 h-10 grid place-items-center rounded-full hover:bg-ink-50 transition">
            <svg class="w-5 h-5 text-ink-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            <span v-if="cart.count" class="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-heritage-600 text-white text-[11px] font-bold grid place-items-center">{{ cart.count }}</span>
          </button>

          <div class="hidden sm:flex items-center gap-2 ml-2 pl-3 border-l border-ink-200">
            <template v-if="auth.isAuthenticated">
              <RouterLink to="/profile" class="hidden md:inline-flex items-center gap-2 pl-1 pr-3 py-1 rounded-full bg-ink-50 border border-ink-200 hover:bg-white transition">
                <img :src="auth.user?.profilePicture || `https://i.pravatar.cc/100?u=${auth.user?.email}`" class="w-7 h-7 rounded-full object-cover" />
                <span class="text-sm font-semibold max-w-[110px] truncate">{{ auth.user?.name || 'Account' }}</span>
              </RouterLink>
              <RouterLink v-if="auth.isAdmin" to="/admin" class="px-3 py-1.5 rounded-full bg-ink-900 text-white text-xs font-bold">ADMIN</RouterLink>
            </template>
            <template v-else>
              <RouterLink to="/login" class="px-5 py-2.5 rounded-full bg-ink-900 text-white text-sm font-semibold hover:bg-ink-800">Sign in</RouterLink>
              <RouterLink to="/register" class="hidden md:inline px-5 py-2.5 rounded-full border border-ink-200 text-sm font-semibold hover:bg-ink-50">Join</RouterLink>
            </template>
          </div>

          <button @click="ui.mobileMenu = !ui.mobileMenu" class="lg:hidden w-10 h-10 grid place-items-center rounded-full border border-ink-200">≡</button>
        </div>
      </div>

      <!-- Mobile search -->
      <div class="md:hidden pb-3">
        <div class="relative">
          <input v-model="search" @keydown.enter="onSearch" placeholder="Search HeritageHub…" class="w-full h-11 pl-11 pr-12 rounded-full bg-ink-50 border border-ink-200 focus:bg-white focus:border-heritage-500 outline-none text-sm" />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-ink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <button @click="onSearch" class="absolute right-1.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-heritage-600 text-white grid place-items-center">→</button>
        </div>
      </div>
    </div>
  </header>
</template>
