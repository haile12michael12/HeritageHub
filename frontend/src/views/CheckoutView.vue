<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import api from '@/services/api'
const cart = useCartStore()
const auth = useAuthStore()
const ui = useUiStore()
const step = ref(1)
const address = ref(auth.user?.address || 'Bishoftu, Oromia, ET — Kebele 09')
const coupon = ref('HERITAGE10')
const discount = ref(0)
const validating = ref(false)

async function validateCoupon() {
  validating.value = true
  try {
    const res = await api.post('/coupons/validate', { code: coupon.value, orderAmount: cart.total })
    const data = res.data?.data || res.data
    if (data?.valid) { discount.value = Number(data.discount); ui.toast(data.message || 'Coupon applied','success') }
    else ui.toast(data?.message || 'Invalid coupon','error')
  } catch {
    // demo: 10% demo
    if (coupon.value.toUpperCase()==='HERITAGE10') { discount.value = cart.total*0.1; ui.toast('Coupon HERITAGE10 applied — 10% off (demo)','success') }
    else ui.toast('Invalid coupon','error')
  } finally { validating.value=false }
}

async function placeOrder() {
  try {
    const res = await api.post('/orders/checkout')
    const data = res.data?.data || res.data
    if (data?.checkoutUrl) window.location.href = data.checkoutUrl
    else ui.toast('Order placed! Redirecting to payment…','success')
  } catch (e:any) {
    // demo success
    ui.toast('Demo: Order #10241 placed — Payment link sent to email','success')
    step.value = 3
  }
}
const total = () => Math.max(0, cart.total - discount.value)
</script>

<template>
  <div class="bg-[#fffaf0] min-h-screen">
    <div class="max-w-5xl mx-auto px-4 py-6">
      <h1 class="font-display font-extrabold text-2xl">Checkout</h1>
      <div class="mt-4 flex items-center gap-2 text-xs font-bold">
        <span class="px-3 py-1 rounded-full" :class="step>=1?'bg-ink-900 text-white':'bg-white border border-ink-200'">1 Address</span>
        <span class="w-6 h-px bg-ink-200"></span>
        <span class="px-3 py-1 rounded-full" :class="step>=2?'bg-ink-900 text-white':'bg-white border border-ink-200'">2 Payment</span>
        <span class="w-6 h-px bg-ink-200"></span>
        <span class="px-3 py-1 rounded-full" :class="step>=3?'bg-ink-900 text-white':'bg-white border border-ink-200'">3 Confirmation</span>
      </div>

      <div class="mt-6 grid lg:grid-cols-[1fr_360px] gap-6">
        <div class="rounded-[22px] bg-white border border-ink-100 p-6 shadow-soft">
          <div v-if="step===1">
            <h3 class="font-bold">Shipping address</h3>
            <p class="text-sm text-ink-500 mt-1">Ethiopian address structure: Region → City → Sub-City → Woreda</p>
            <div class="mt-4 grid gap-3">
              <input v-model="address" class="input" placeholder="Full address" />
              <div class="grid grid-cols-2 gap-3">
                <input placeholder="City (e.g. Bishoftu)" class="input" value="Bishoftu" />
                <input placeholder="Phone" class="input" value="+251 911 000 000" />
              </div>
              <label class="flex gap-2 text-sm"><input type="checkbox" checked /> Save for next time</label>
            </div>
            <button @click="step=2" class="btn-primary w-full mt-4">Continue to payment →</button>
          </div>

          <div v-if="step===2">
            <h3 class="font-bold">Payment method</h3>
            <div class="mt-4 grid gap-3">
              <label class="flex items-center gap-3 p-4 rounded-2xl border-2 border-heritage-500 bg-heritage-50"><input type="radio" checked name="pay" /> <span class="font-semibold">Telebirr / Chapa (Recommended)</span><span class="ml-auto text-xs font-bold bg-white px-2 py-1 rounded-full border">ETB</span></label>
              <label class="flex items-center gap-3 p-4 rounded-2xl border border-ink-200"><input type="radio" name="pay" /> <span class="font-semibold">Card (Stripe)</span><span class="ml-auto text-xs">Visa • MC</span></label>
              <label class="flex items-center gap-3 p-4 rounded-2xl border border-ink-200"><input type="radio" name="pay" /> <span class="font-semibold">Cash on Delivery</span><span class="ml-auto text-xs">Pay to rider</span></label>
            </div>
            <button @click="placeOrder" class="btn-primary w-full mt-4 py-3.5">Pay {{ total().toFixed(2) }} ETB Securely</button>
            <p class="text-center text-xs text-ink-400 mt-2">By placing order you agree to Terms • 14-day returns</p>
          </div>

          <div v-if="step===3" class="text-center py-10">
            <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-700 grid place-items-center mx-auto text-2xl">✓</div>
            <h3 class="mt-4 font-display font-bold text-xl">Order confirmed!</h3>
            <p class="text-sm text-ink-500">Order #10241 • Track in real-time</p>
            <div class="mt-4 p-4 rounded-2xl bg-ink-50 border border-ink-100 text-left text-sm">
              <div>📦 Packed → Shipped → Out for delivery → Delivered</div>
              <div class="mt-2 h-2 rounded-full bg-ink-200 overflow-hidden"><div class="h-2 bg-heritage-600 w-[40%]"></div></div>
            </div>
            <RouterLink to="/orders" class="btn-primary mt-6">Track order</RouterLink>
          </div>
        </div>

        <div class="rounded-[22px] bg-white border border-ink-100 p-6 h-fit shadow-soft">
          <h3 class="font-bold">Order Summary</h3>
          <div class="mt-4 space-y-2">
            <div v-for="item in cart.items" :key="item.id" class="flex gap-3 text-sm">
              <img :src="item.product_image || `https://picsum.photos/seed/${item.product_id}/200/200`" class="w-12 h-12 rounded-xl object-cover" />
              <div class="flex-1"><div class="font-semibold line-clamp-1">{{ item.product_name }}</div><div class="text-ink-500">× {{ item.quantity }}</div></div>
              <div class="font-bold">{{ (Number(item.product_price)*item.quantity).toFixed(0) }} ETB</div>
            </div>
          </div>
          <div class="mt-4 flex gap-2"><input v-model="coupon" placeholder="HERITAGE10" class="input flex-1" /><button @click="validateCoupon" :disabled="validating" class="px-4 py-2 rounded-full bg-ink-900 text-white text-sm font-bold disabled:opacity-50">{{ validating ? '...' : 'Apply' }}</button></div>
          <div class="mt-4 space-y-1 text-sm">
            <div class="flex justify-between"><span class="text-ink-500">Subtotal</span><span class="font-bold">{{ cart.total.toFixed(2) }} ETB</span></div>
            <div class="flex justify-between"><span class="text-ink-500">Discount</span><span class="font-bold text-emerald-600">-{{ discount.toFixed(2) }} ETB</span></div>
            <div class="flex justify-between"><span class="text-ink-500">Shipping</span><span class="font-bold text-emerald-600">Free</span></div>
            <div class="h-px bg-ink-100 my-2"></div>
            <div class="flex justify-between font-extrabold text-lg"><span>Total</span><span>{{ total().toFixed(2) }} ETB</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
