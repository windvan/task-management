// 通用错误处理，不需要将api请求放在错误捕获代码中
// 如果想使用局部错误处理，将请求放在try代码块中，并在catch块中使用error.response.data.detail获取api返回的错误信息

import axios from 'axios'
import { useToastService } from './useToastService';
import router from '../router'


export default function useApi() {
 const { showError, showWarning } = useToastService();

  const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL, // get base url from .env
    timeout: 5000,
    withCredentials: true
    
  })

  // axios response interceptor
  axiosInstance.interceptors.response.use(
    response => response.data,
    error => {

      if (error.response) {
        const { status, data } = error.response;
        const errorMessage = data?.detail || error.message;

        switch (status) {
          case 401:
            router.push('/login');
            showWarning(errorMessage,'Unauthorized');
            break;
          case 403:
            showError('You do not have permission to perform this action');
            break;
          case 404:
             showError(errorMessage, 'Not found Error');
            break;
          case 400:
          case 422:
            showError(errorMessage, 'Validation Error');
            break;
          case 500:
            showError('An unexpected error occurred. Please try again later.','Server Error');
            break;
          default:
            showError(`Request failed: ${errorMessage}`);
        }
      } else if (error.request) {
        showError('No response received from server');
      } else {
        showError('Failed to send request');
      }

      return Promise.reject(error);
    }
  )

  return axiosInstance
}
