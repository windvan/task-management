// style
import "./assets/style.css"; /* global-css */
import "primeicons/primeicons.css"; /* primevue-icons */

// utils

import { createPinia } from "pinia";
import router from "./router";

// primevue
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import { definePreset } from "@primevue/themes";
import ConfirmationService from "primevue/confirmationservice";
import ToastService from "primevue/toastservice";
import Tooltip from "primevue/tooltip";
// vue
import App from "./App.vue";
import { createApp } from "vue";


const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: "{cyan.50}",
      100: "{cyan.100}",
      200: "{cyan.200}",
      300: "{cyan.300}",
      400: "{cyan.400}",
      500: "{cyan.500}",
      600: "{cyan.600}",
      700: "{cyan.700}",
      800: "{cyan.800}",
      900: "{cyan.900}",
      950: "{cyan.950}",
    },
    colorScheme: {
      light: {
        formField: {
          shadow: null,
          borderColor: "{gray.300}",
        },
      },
    },
  },
  
});

const app = createApp(App);

// Install PrimeVue and Toast service first
app.use(PrimeVue, {
  theme: {
    preset: MyPreset,
    ripple: true,
    options: {
      cssLayer: {
        name: "primevue",
        order: 'theme, base, primevue',
      },
    },
  }
});

app.use(ToastService);
app.use(ConfirmationService);
app.directive("tooltip", Tooltip);

app.use(createPinia());
app.use(router);

app.mount("#app");

