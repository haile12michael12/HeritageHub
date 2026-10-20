<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useUiStore } from '@/stores/ui'
const cart = useCartStore()
const ui = useUiStore()
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <h1 class="font-display font-extrabold text-2xl">Shopping Cart</h1>
      <div class="mt-6 grid lg:grid-cols-[1fr_360px] gap-6">
        <div class="rounded-[22px] bg-white border border-ink-100 shadow-soft p-6">
          <div v-if="!cart.items.length" class="py-16 text-center">
            <div class="w-16 h-16 rounded-3xl bg-ink-50 grid place-items-center mx-auto text-2xl">🛒</div>
            <p class="mt-4 font-semibold">Your cart is empty</p>
            <p class="text-sm text-ink-500">Discover heritage treasures in Shop.</p>
            <RouterLink to="/shop" class="btn-primary mt-4">Continue Shopping</RouterLink>
          </div>
          <div v-else class="space-y-4">
            <div v-for="item in cart.items" :key="item.id" class="flex gap-4 p-4 rounded-2xl border border-ink-100 bg-ink-50">
              <img :src="item.product_image || `https://picsum.photos/seed/${item.product_id}/200/200`" class="w-24 h-24 rounded-xl object-cover" />
              <div class="flex-1">
                <div class="font-semibold">{{ item.product_name }}</div>
                <div class="text-sm text-ink-500">Unit: {{ item.product_price }} ETB</div>
                <div class="mt-2 flex items-center gap-2">
                  <button @click="cart.decrement(item.product_id)" class="w-8 h-8 rounded-full bg-white border border-ink-200">−</button>
                  <span class="w-8 text-center font-bold">{{ item.quantity }}</span>
                  <button @click="cart.addLocal({ id: item.product_id, name: item.product_name, price: item.product_price, image_url: item.product_image })" class="w-8 h-8 rounded-full bg-white border border-ink-200">+</button>
                  <span class="ml-auto font-extrabold">{{ (Number(item.product_price)*item.quantity).toFixed(2) }} ETB</span>
                </div>
              </div>
              <button @click="cart.remove(item.product_id); cart.items=cart.items.filter((i:any)=>i.product_id!==item.product_id)" class="text-sm font-semibold text-red-600">Remove</button>
            </div>
          </div>
        </div>
        <div class="rounded-[22px] bg-white border border-ink-100 p-6 h-fit shadow-soft">
          <h3 class="font-bold text-lg">Order Summary</h3>
          <div class="mt-4 space-y-2 text-sm">
            <div class="flex justify-between"><span class="text-ink-500">Subtotal</span><span class="font-bold">{{ cart.total.toFixed(2) }} ETB</span></div>
            <div class="flex justify-between"><span class="text-ink-500">Shipping</span><span class="font-bold text-emerald-600">Free</span></div>
            <div class="flex gap-2 mt-3"><input placeholder="Coupon code" class="input flex-1" /><button @click="ui.toast('Coupon HERITAGE10 applied — 10% off','success')" class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-bold">Apply</button></div>
            <div class="h-px bg-ink-100 my-3"></div>
            <div class="flex justify-between font-extrabold text-lg"><span>Total</span><span>{{ cart.total.toFixed(2) }} ETB</span></div>
          </div>
          <RouterLink to="/checkout" class="btn-primary w-full mt-4 py-3.5">Proceed to Checkout →</RouterLink>
          <p class="text-center text-xs text-ink-400 mt-2">Tax included • Secure by Chapa & Telebirr</p>
        </div>
      </div>
    </div>
  </div>
</template>
