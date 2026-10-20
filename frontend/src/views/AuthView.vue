<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const props = defineProps<{ mode: 'login' | 'register' }>()
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const ui = useUiStore()

const email = ref('demo@heritagehub.et')
const password = ref('demo12345')
const name = ref('Heritage Guest')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    if (props.mode === 'login') {
      await auth.login(email.value, password.value)
      ui.toast('Welcome back!','success')
      router.push((route.query.redirect as string) || '/')
    } else {
      await auth.register({ email: email.value, password: password.value, name: name.value })
      ui.toast('Account created — please sign in','success')
      router.push('/login')
    }
  } catch (e:any) {
    const msg = e?.response?.data?.message || e?.response?.data?.detail || (props.mode==='login' ? 'Demo login: use any email (backend optional) — continuing as guest' : 'Demo: account created locally')
    // demo fallback: mock auth
    if (props.mode==='login') {
      auth.user = { email: email.value, name: email.value.split('@')[0], role: 'CUSTOMER', profilePicture: `https://i.pravatar.cc/100?u=${email.value}` }
      auth.token = 'demo-token'
      localStorage.setItem('heritage_token','demo-token')
      localStorage.setItem('heritage_user', JSON.stringify(auth.user))
      ui.toast('Signed in as demo guest — explore shop','success')
      router.push('/')
    } else {
      ui.toast(msg,'error')
    }
  } finally { loading.value=false }
}
</script>

<template>
  <div class="min-h-[80vh] bg-[#fffaf0] grid lg:grid-cols-2">
    <div class="hidden lg:block relative overflow-hidden">
      <img src="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=1000&q=80" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-ink-900 via-ink-900/40 to-transparent"></div>
      <div class="absolute bottom-0 p-10 text-white">
        <div class="inline-flex px-3 py-1 rounded-full bg-white/15 border border-white/20 text-xs font-bold tracking-widest uppercase">HeritageHub • Since 2024</div>
        <h2 class="mt-4 font-display font-extrabold text-3xl leading-tight">Craft, culture and<br />commerce — together.</h2>
        <p class="mt-3 text-sm text-white/80 max-w-md">Join 12,000+ customers supporting Ethiopian artisans. Secure ETB payments, real-time delivery, AI help.</p>
      </div>
    </div>
    <div class="flex items-center justify-center p-6 lg:p-10">
      <div class="w-full max-w-md rounded-[28px] bg-white border border-ink-100 p-8 shadow-lifted">
        <div class="w-12 h-12 rounded-2xl bg-ink-900 text-white grid place-items-center font-display font-extrabold">H</div>
        <h1 class="mt-4 font-display font-extrabold text-2xl">{{ mode==='login' ? 'Welcome back' : 'Create account' }}</h1>
        <p class="text-sm text-ink-500">{{ mode==='login' ? 'Sign in to your HeritageHub account' : 'Start your heritage journey today' }}</p>

        <form @submit.prevent="submit" class="mt-6 space-y-3">
          <div v-if="mode==='register'"><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Full name</label><input v-model="name" class="input mt-1" required /></div>
          <div><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Email</label><input v-model="email" type="email" class="input mt-1" required /></div>
          <div><label class="text-xs font-bold tracking-widest uppercase text-ink-500">Password</label><input v-model="password" type="password" class="input mt-1" required /></div>
          <div v-if="mode==='login'" class="flex justify-between text-xs"><label class="flex gap-2"><input type="checkbox" /> Remember me</label><a href="#" class="font-semibold text-heritage-700">Forgot?</a></div>
          <button :disabled="loading" class="btn-primary w-full py-3.5 disabled:opacity-50">{{ loading ? 'Please wait…' : (mode==='login' ? 'Sign in →' : 'Create account') }}</button>
        </form>

        <div class="mt-6">
          <div class="flex items-center gap-3 text-xs text-ink-400"><span class="h-px flex-1 bg-ink-200"></span> OR <span class="h-px flex-1 bg-ink-200"></span></div>
          <button class="mt-4 w-full py-3 rounded-full border border-ink-200 font-semibold flex items-center justify-center gap-2 hover:bg-ink-50"><span class="w-5 h-5 rounded-full bg-white border grid place-items-center text-xs">G</span> Continue with Google</button>
        </div>

        <p class="mt-6 text-center text-sm">
          <span class="text-ink-500">{{ mode==='login' ? 'New here?' : 'Already have an account?' }}</span>
          <RouterLink :to="mode==='login' ? '/register' : '/login'" class="font-bold text-heritage-700 ml-1">{{ mode==='login' ? 'Create account' : 'Sign in' }}</RouterLink>
        </p>
        <p class="mt-3 text-center text-xs text-ink-400">Demo: any email works — no backend required for preview</p>
      </div>
    </div>
  </div>
</template>
