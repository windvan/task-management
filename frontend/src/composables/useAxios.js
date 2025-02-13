// 通用错误处理，不需要将api请求放在错误捕获代码中
// 如果想使用局部错误处理，将请求放在try代码块中，并在catch块中使用error.response.data.detail获取api返回的错误信息
import router from '@/router'
import axios from 'axios'
export default function useAxios() {
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
            error.customMessage=('Bad Request');
            break;
          case 401:
            error.customMessage=('Unauthorized');
            router.push('/login');
            break;
          case 403:
            error.customMessage=('Access Forbidden');
            break;
          case 404:
            error.customMessage=('Resource Not Found');
            break;
          case 408:
            error.customMessage=('Request Timeout');
            break;
          case 500:
            error.customMessage=('Internal Server Error');
            break;
          case 501:
            error.customMessage=('Not Implemented');
            break;
          case 502:
            error.customMessage=('Bad Gateway');
            break;
          case 503:
            error.customMessage=('Service Unavailable');
            break;
          case 504:
            error.customMessage=('Gateway Timeout');
            break;
          case 505:
            error.customMessage=('HTTP Version Not Supported');
            break;
          default:
            error.customMessage=(`Connection Error: ${error.response.status}`);
        }
      } else {
        error.customMessage=('Failed to connect to the server');
      }
      return Promise.reject(error);
    }
  )
  return axiosInstance
}
