import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
// import api from '../api'

export const useEnumsStore = defineStore('enums', () => {
  

  async function getEnums() {
    Api
      .get('/enums')
      .then((response) => {
        enums.value = response.data
        localStorage.setItem('cachedEnums', JSON.stringify(enums.value))
      })
      .catch((err) => {
        console.log(err.customMessage)
      })
  }

  return { enums, getEnums }
})
