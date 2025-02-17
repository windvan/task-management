
import { defineStore } from 'pinia'


export const useErrorStore = defineStore('error', () => {
    const axiosErrMsg = ref(null)
    const loginErrMsg = ref(null)

    return { axiosErrMsg, loginErrMsg }
})