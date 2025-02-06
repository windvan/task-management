import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import vueDevTools from 'vite-plugin-vue-devtools'
import Components from 'unplugin-vue-components/vite';
import { PrimeVueResolver } from '@primevue/auto-import-resolver';


export default defineConfig({
  // server: {
  //   https: {
  //     key: fs.readFileSync('../key.key'),
  //     cert: fs.readFileSync('../crt.crt')
  //   }
  // },

  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(),
    Components({
      resolvers: [PrimeVueResolver()] //primevue tree shaking
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  base: './' //打包结果中的文件引入使用相对路径
})
