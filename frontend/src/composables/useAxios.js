
// 通用错误处理，不需要将api请求放在错误捕获代码中
// 如果想使用局部错误处理，将请求放在try代码块中，并在catch块中使用error.response.data.detail获取api返回的错误信息
import router from '@/router'
import axios from 'axios'
import { useErrorStore } from '../stores/errorStore'

const errStore=useErrorStore()

function useAxios() {
  const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL, // get base url from .env
    timeout: 3000,
    withCredentials: true
  })

  // axios request interceptor
  // axiosInstance.interceptors.request.use((config) => {return config})
  // axios response interceptor
  axiosInstance.interceptors.response.use(
    (response) => response.data,
    (error) => {
      if (error.response) {
        // console.log(error)
        switch (error.response.status) {
          case 400:
            axiosErrMsg = ('Bad Request');
            break;
          case 401:
            axiosErrMsg = ('Unauthorized');
            router.push('/login');
            break;
          case 403:
            axiosErrMsg = ('Access Forbidden');
            break;
          case 404:
            axiosErrMsg = ('Resource Not Found');
            break;
          case 408:
            axiosErrMsg = ('Request Timeout');
            break;
          case 500:
            axiosErrMsg = ('Internal Server Error');
            break;
          case 501:
            axiosErrMsg = ('Not Implemented');
            break;
          case 502:
            axiosErrMsg = ('Bad Gateway');
            break;
          case 503:
            axiosErrMsg = ('Service Unavailable');
            break;
          case 504:
            axiosErrMsg = ('Gateway Timeout');
            break;
          case 505:
            axiosErrMsg = ('HTTP Version Not Supported');
            break;
          default:
            axiosErrMsg = (`Connection Error: ${error.response.status}`);
        }
      } else {
        axiosErrMsg = ('Failed to connect to the server');
      }
      return Promise.reject(error);
    }
  )
  // update errorStore state
  errStore.$patch({ axiosErrMsg: axiosErrMsg })
  
  return axiosInstance
}
export { axiosErrMsg,useAxios}