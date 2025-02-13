import { ref, inject, computed } from 'vue'
import { defineStore } from 'pinia'
// import api from '../api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const $axios = inject('$axios')
  const cached_user = localStorage.getItem('cached_user')
  const current_user=ref(JSON.parse(cached_user).current_user)
  const loginErrorMessage = ref('')

  const isLogedIn = computed(() => !!current_user.value)

  async function login(credentials) {
    try {
      current_user.value = await $axios.post('/auth/login', credentials)
      localStorage.setItem('cached_user', JSON.stringify(current_user.value))
      router.push('/')
    } catch (error) {
      console.log(error)
      loginErrorMessage.value = error.response.data.detail
    }
  }

  async function logout() {
    await $axios.get('/auth/logout')
    try {
      localStorage.removeItem('cached_users')
      current_user.value = null
      router.push('/login')
    } catch (error) {
      console.log(error)
      
    }
  }

  return { current_user, login, logout, isLogedIn, loginErrorMessage}
})
