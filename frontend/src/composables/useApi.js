// 通用错误处理，不需要将api请求放在错误捕获代码中
// 如果想使用局部错误处理，将请求放在try代码块中，并在catch块中使用error.response.data.detail获取api返回的错误信息

import axios from 'axios'
import { useErrorStore } from '../stores/errorStore'
import router from '../router'


export default function useApi() {
  const errStore = useErrorStore()

  const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL, // get base url from .env
    timeout: 5000,
    withCredentials: true,
    skipInterceptor: false
  })

  // axios request interceptor
  axiosInstance.interceptors.request.use((config) => {
    
    return config
  })
  // axios response interceptor
  axiosInstance.interceptors.response.use(
    (response) => response.data,
    (error) => {
      if (error.config.skipInterceptor) {
        return Promise.reject(error)
      }
      // 检查是否有响应，及是否跳过拦截器
      if (error.response) {
        // 请求已发出，但服务器响应的状态码不在 2xx 范围内
        switch (error.response.status) {
          case 400:
            errStore.setMessage('warn', 'Response Error', 'Bad Request')
            console.error(error)
            break;
          case 401:
            console.error(error)
            router.push('/login');
            break;
          case 403:
            errStore.setMessage('warn', 'Response Error', 'Access Forbidden')
            console.error(error);
            break;
          case 404:
            console.error(error)
            router.push('/404')
            break;
          case 408:
            errStore.setMessage('warn', 'Response Error', 'Request Timeout')
            console.error(error);
            break;
          case 500:
            errStore.setMessage('warn', 'Response Error', 'Internal Server Error')
            console.error(error);
            break;
          case 501:
            errStore.setMessage('warn', 'Response Error', 'Not Implemented')
            console.error(error);
            break;
          case 502:
            errStore.setMessage('warn', 'Response Error', 'Bad Gateway')
            console.error(error);
            break;
          case 503:
            errStore.setMessage('warn', 'Response Error', 'Service Unavailable')
            console.error(error);
            break;
          case 504:
            errStore.setMessage('warn', 'Response Error', 'Gateway Timeout')
            console.error(error);
            break;
          case 505:
            errStore.setMessage('warn', 'Response Error', 'HTTP Version Not Supported')
            console.error(error);
            break;
          default:
            errStore.setMessage('warn', 'Response Error', `Connection Error: ${error.response.statusText}`)
            console.error(error);
        }
      } else if (error.request) {
        // 请求已经成功发起，但没有收到响应
        errStore.setMessage('warn', 'Response Error', 'No Response Received')
        console.error(error);
      } else {
        // 发送请求时出了点问题
        errStore.setMessage('warn', 'Request Error', 'Something is Wrong with the Request')
        console.error(error);
      }
      return Promise.reject(error);
    }
  )

  return axiosInstance
}
