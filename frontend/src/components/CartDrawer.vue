<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { useUiStore } from '@/stores/ui'
import { useRouter } from 'vue-router'
const cart = useCartStore()
const ui = useUiStore()
const router = useRouter()
</script>

<template>
  <div v-if="ui.cartOpen" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-ink-900/40 backdrop-blur-sm" @click="ui.cartOpen=false"></div>
    <div class="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-2xl flex flex-col animate-slide-up">
      <div class="p-6 border-b border-ink-100 flex items-center justify-between">
        <div>
          <h3 class="font-display font-bold text-xl">Your Cart</h3>
          <p class="text-sm text-ink-500">{{ cart.count }} items • Free shipping over 2,000 ETB</p>
        </div>
        <button @click="ui.cartOpen=false" class="w-9 h-9 rounded-full bg-ink-50 grid place-items-center">✕</button>
      </div>

      <div class="flex-1 overflow-auto p-6 space-y-4">
        <div v-if="!cart.items.length" class="py-16 text-center">
          <div class="w-16 h-16 rounded-3xl bg-ink-50 grid place-items-center mx-auto text-2xl">🛒</div>
          <p class="mt-4 font-semibold">Your cart is empty</p>
          <p class="text-sm text-ink-500">Add some heritage treasures to get started.</p>
          <button @click="ui.cartOpen=false; router.push('/shop')" class="btn-primary mt-4">Continue Shopping</button>
        </div>

        <div v-for="item in cart.items" :key="item.id" class="flex gap-3 p-3 rounded-2xl bg-ink-50 border border-ink-100">
          <img :src="item.product_image || `https://picsum.photos/seed/${item.product_id}/200/200`" class="w-20 h-20 rounded-xl object-cover" />
          <div class="flex-1 min-w-0">
            <div class="font-semibold text-sm leading-tight line-clamp-1">{{ item.product_name }}</div>
            <div class="text-sm font-bold text-ink-900">{{ item.product_price }} ETB × {{ item.quantity }}</div>
            <div class="text-xs text-ink-500">Subtotal: {{ (Number(item.product_price) * item.quantity).toFixed(2) }} ETB</div>
            <div class="mt-2 flex gap-1">
              <button @click="cart.decrement(item.product_id); cart.items.find((i:any)=>i.product_id===item.product_id) && (cart.items.find((i:any)=>i.product_id===item.product_id).quantity=Math.max(1, cart.items.find((i:any)=>i.product_id===item.product_id).quantity-1))" class="w-7 h-7 rounded-full bg-white border border-ink-200 grid place-items-center">−</button>
              <span class="w-8 text-center text-sm font-semibold">{{ item.quantity }}</span>
              <button @click="cart.addLocal({ id: item.product_id, name: item.product_name, price: item.product_price, image_url: item.product_image })" class="w-7 h-7 rounded-full bg-white border border-ink-200 grid place-items-center">+</button>
              <button @click="cart.remove(item.product_id); cart.items = cart.items.filter((i:any)=>i.product_id!==item.product_id)" class="ml-auto text-xs font-semibold text-red-600">Remove</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="cart.items.length" class="p-6 border-t border-ink-100 bg-white">
        <div class="flex justify-between text-sm"><span class="text-ink-500">Subtotal</span><span class="font-bold">{{ cart.total.toFixed(2) }} ETB</span></div>
        <div class="flex justify-between text-sm mt-1"><span class="text-ink-500">Shipping</span><span class="font-bold text-emerald-600">Free</span></div>
        <div class="h-px bg-ink-100 my-3"></div>
        <div class="flex justify-between font-display font-extrabold text-lg"><span>Total</span><span>{{ cart.total.toFixed(2) }} ETB</span></div>
        <button @click="ui.cartOpen=false; router.push('/checkout')" class="btn-primary w-full mt-4 py-3.5">Checkout Securely →</button>
        <p class="text-center text-xs text-ink-400 mt-2">Protected by 256-bit SSL • Cash on Delivery available</p>
      </div>
    </div>
  </div>
</template>
