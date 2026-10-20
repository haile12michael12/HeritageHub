import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(JSON.parse(localStorage.getItem('heritage_user') || 'null'))
  const token = ref<string | null>(localStorage.getItem('heritage_token'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  async function login(email: string, password: string) {
    const res = await api.post('/auth/login', { email, password })
    const data = res.data?.data || res.data
    token.value = data.token
    user.value = data.user
    localStorage.setItem('heritage_token', data.token)
    localStorage.setItem('heritage_user', JSON.stringify(data.user))
    return data
  }
  async function register(payload: any) {
    const res = await api.post('/auth/register', payload)
    return res.data
  }
  async function fetchProfile() {
    try {
      const res = await api.get('/users/me')
      user.value = res.data?.data || res.data
      localStorage.setItem('heritage_user', JSON.stringify(user.value))
    } catch {}
  }
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('heritage_token')
    localStorage.removeItem('heritage_user')
  }
  return { user, token, isAuthenticated, isAdmin, login, register, logout, fetchProfile }
})
