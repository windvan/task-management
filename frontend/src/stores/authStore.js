import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
import router from '../router'
import useApi from '../composables/useApi'

export const useAuthStore = defineStore('auth', () => {


  const Api = useApi()
  const current_user = ref(null)
  const isLoggedIn = ref(false)
  const loginErrorMessage = ref(null)

  async function login(credentials) {

    try {
      let data = await Api.post('/auth/login', credentials, { skipInterceptor: true })
      current_user.value = data.current_user
      isLoggedIn.value = data.isAuthenticated
      router.push('/')

    } catch (error) {
      // console.log(error)
      // use response message if responed otherwise use axios error message
      if (error.response) {
        loginErrorMessage.value = error.response?.data?.detail
      } else {
        loginErrorMessage.value = error.message
      }
    }

  }

  async function logout() {
    await Api.get('/auth/logout')
    current_user.value = null
    isLoggedIn.value = false
    router.push('/login')
  }

  async function checkAuthStatus() {

    try {
      const data = await Api.get('/auth/status')
      isLoggedIn.value = data.isAuthenticated
      current_user.value = data.current_user

    } catch (error) {
      console.error('Failed to check auth status', error)
      isLoggedIn.value = false
      current_user.value = null
      return false
    }
  }

  return { login, isLoggedIn, checkAuthStatus, current_user, logout, loginErrorMessage }
})