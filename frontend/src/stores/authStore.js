import { ref, inject, computed } from 'vue'
import { defineStore } from 'pinia'
// import api from '../api'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const $axios = inject('$axios')
  const current_user =ref( localStorage.getItem('cached_user')
    ? JSON.parse(localStorage.getItem('cached_user'))
    : null)
  const loginErrorMessage = ref('')
  const isLogedIn = computed(()=>!!current_user.value)

  async function login(credentials) {
    try {
      const response = await $axios.post('/auth/login', credentials)
      current_user.value = response.data.current_user
      localStorage.setItem('cached_user', JSON.stringify(current_user.value))
      router.push('/')
    } catch (errMsg) {
      loginErrorMessage.value = errMsg
    }
  }

  async function logout() {
    try {
      let response = await $axios.get('/auth/logout')
      console.log(response.data)
      localStorage.removeItem('cached_user')
      current_user.value = null 
      router.push('/login')
    } catch (err) {
      console.error(err)
    }
  }

  return { current_user, login, logout, isLogedIn, loginErrorMessage }
})
