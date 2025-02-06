import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
// import api from '../api'

export const useEnumsStore = defineStore('enums', () => {
  const $axios = inject('$axios')
  const enums = ref(JSON.parse(localStorage.getItem('cachedEnums')))

  async function getEnums() {
    $axios
      .get('/enums')
      .then((response) => {
        enums.value = response.data
        localStorage.setItem('cachedEnums', JSON.stringify(enums.value))
      })
      .catch((err) => {
        console.log(err.message)
      })
  }

  return { enums, getEnums }
})
