import router from '@/router'
import axios from 'axios'

// import router from '../router'

export default function useAxios() {
  const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL, // get base url from .env
    timeout: 3000,
    //for oauth2 authorization,Authorization must be pre-set as
    // headers: { Authorization: 'Bearer' },
    withCredentials: true
  })

  // axios 请求拦截器
  // axiosInstance.interceptors.request.use(
  //   // 检查access_token cookie是否存在
  //   (config) => {

  //     return config
  //   }
  // )
  // axios respoonse interceptor
  axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      let errorMessage = 'An error occurred'

      if (error.response) {
        // 服务器响应了，但状态码不在 2xx 范围内
        switch (error.response.status) {
          case 400:
            errorMessage = 'Bad request'
            break
          case 401:
            errorMessage = `Unauthorized: ${error.response.data.message}`
            router.push('/login')
            break
          case 403:
            errorMessage = 'Forbidden'
            break
          case 404:
            errorMessage = 'Not found'
            break
          case 500:
            errorMessage = 'Internal server error'
            break
          default:
            errorMessage = `Error: ${error.response.status}-${error.message}`
        }
      } else if (error.request) {
        // 请求已经发出，但没有收到响应
        errorMessage = 'No response from server'
      } else {
        // 在设置请求时发生了错误
        errorMessage = error.message
      }

      return Promise.reject(errorMessage)
    }
  )
  return axiosInstance
}
