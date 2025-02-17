import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useErrorStore } from './errorStore'

export const useAuthStore = defineStore('auth', () => {

  const errorStore = useErrorStore()

  const current_user = ref(null)
  const isLoggedIn = ref(false) //computed(() => !!current_user.value)

  async function login(credentials, router, axios) {
    try {
      let data = await axios.post('/auth/login', credentials)

      current_user.value = data.current_user
      isLoggedIn.value = data.isAuthenticated

    } catch (error) {
      console.error(error)
      errorStore.$patch({ loginErrMsg: error.response?.data?.detail || 'Login failed' })
    }

    router.push('/')
  }

  async function logout(router, axios) {
    await axios.get('/auth/logout')
    current_user.value = null
    isLoggedIn.value = false
    router.push('/login')
  }

  async function checkAuthStatus() {

    try {
      const data = await axios.get('/auth/status')
      isLoggedIn.value = data.isAuthenticated
      current_user.value = data.current_user

    } catch (error) {
      console.error('Failed to check auth status', error)
      isLoggedIn.value = false
      current_user.value = null
      return false
    }
  }

  return { current_user, login, logout, isLoggedIn }
})