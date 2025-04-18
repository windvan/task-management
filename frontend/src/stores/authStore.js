import { ref } from 'vue'
import { defineStore } from 'pinia'
import router from '../router'
import useApi from '../composables/useApi'

export const useAuthStore = defineStore('auth', () => {


  const Api = useApi()
  const current_user = ref(null)
  const isLoggedIn = ref(false)


  async function login(credentials) {

    try {
      let data = await Api.post('/auth/login', credentials)
      console.log(data)
      current_user.value = data.current_user
      isLoggedIn.value = data.isAuthenticated

      // 获取当前路由中的 redirect 参数
      const redirect = router.currentRoute.value.query.redirect
      // 如果存在 redirect，跳转到该页面；否则跳转到首页
      if (redirect) {
        router.push(redirect)
      } else {
        router.push('/')
      }

    } catch (error) {
      // console.log(error)
      // use response message if responed otherwise use axios error message
      // if (error.response) {
      //   loginErrorMessage.value = error.response?.data?.detail
      // } else {
      //   loginErrorMessage.value = error.message
      // }
      console.log("Login Error: ",error)
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

  return { login, isLoggedIn, checkAuthStatus, current_user, logout }
})