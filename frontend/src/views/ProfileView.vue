<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-5xl mx-auto px-4 py-6 grid lg:grid-cols-[260px_1fr] gap-6">
      <aside class="rounded-[22px] bg-white border border-ink-100 p-6 h-fit shadow-soft">
        <div class="flex items-center gap-3">
          <img :src="auth.user?.profilePicture || `https://i.pravatar.cc/100?u=${auth.user?.email}`" class="w-12 h-12 rounded-full" />
          <div><div class="font-bold">{{ auth.user?.name || 'Guest' }}</div><div class="text-xs text-ink-500">{{ auth.user?.email }}</div></div>
        </div>
        <div class="mt-4 space-y-1 text-sm font-semibold">
          <div class="px-3 py-2 rounded-full bg-ink-900 text-white">Profile</div>
          <RouterLink to="/orders" class="block px-3 py-2 rounded-full hover:bg-ink-50">Orders</RouterLink>
          <RouterLink to="/wishlist" class="block px-3 py-2 rounded-full hover:bg-ink-50">Wishlist</RouterLink>
          <div class="px-3 py-2 rounded-full hover:bg-ink-50">Addresses</div>
          <div class="px-3 py-2 rounded-full hover:bg-ink-50">Security</div>
        </div>
        <button @click="auth.logout(); $router.push('/')" class="mt-6 w-full py-2.5 rounded-full border border-ink-200 font-semibold">Sign out</button>
      </aside>
      <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
        <h2 class="font-display font-bold text-xl">Profile settings</h2>
        <div class="mt-4 grid sm:grid-cols-2 gap-4">
          <div><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Full name</label><input :value="auth.user?.name" class="input mt-1" /></div>
          <div><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Email</label><input :value="auth.user?.email" class="input mt-1" disabled /></div>
          <div class="sm:col-span-2"><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Address (Delivery)</label><input :value="auth.user?.address || 'Bishoftu, Oromia, ET'" class="input mt-1" /></div>
        </div>
        <div class="mt-4 flex gap-2">
          <button class="btn-primary">Save changes</button>
          <button class="btn-ghost">Change password</button>
        </div>
        <div class="mt-6 rounded-2xl bg-amber-50 border border-amber-200 p-4 text-sm">
          <div class="font-bold">Heritage Rewards</div>
          <div class="text-ink-600">You have 1,240 points • Redeem for 120 ETB off next order.</div>
        </div>
      </div>
    </div>
  </div>
</template>
