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
  build: {
    outDir: '../backend/app/statics/frontend/dist' // 自定义输出目录，默认是 dist
  },

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
  // base: import.meta.env.VITE_API_STATIC_BASE_URL, //打包过程中的相对路径相对于此值
})
