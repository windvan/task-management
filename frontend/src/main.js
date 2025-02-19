// style
import './assets/style.css' /* global-css */
import 'primeicons/primeicons.css' /* primevue-icons */

// utils
import useAxios from './composables/useApi'
import { createPinia } from 'pinia'
import router from './router'

// primevue
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
// vue
import App from './App.vue'
import { createApp } from 'vue'
import useApi from './composables/useApi'

const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{cyan.50}',
      100: '{cyan.100}',
      200: '{cyan.200}',
      300: '{cyan.300}',
      400: '{cyan.400}',
      500: '{cyan.500}',
      600: '{cyan.600}',
      700: '{cyan.700}',
      800: '{cyan.800}',
      900: '{cyan.900}',
      950: '{cyan.950}'
    }
  }
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.provide('Api', useApi())
app.directive('tooltip', Tooltip)

// prime vue plugin

app.use(PrimeVue, {
  theme: {
    preset: MyPreset,
    ripple: true,
    options: {
      cssLayer: {
        name: 'primevue',
        order: 'base,primevue,components,utilities'
      }
    }
  }
})

app.use(ConfirmationService)
app.use(ToastService)

app.mount('#app')
