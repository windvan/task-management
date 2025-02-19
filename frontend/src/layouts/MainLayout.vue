<template>
  <div class="flex flex-col h-screen">
    <TheHeader @toggle="isSidebarOpen = !isSidebarOpen"></TheHeader>
    <main class="flex flex-1 overflow-hidden pt-3 gap-3">
      <TheNavigation v-show="isSidebarOpen"></TheNavigation>
      <RouterView class="bg-white rounded-md p-4 overflow-auto w-full flex flex-col gap-4"></RouterView>
    </main>
  </div>
</template>

<script setup>
  import TheHeader from '@/components/TheHeader.vue'
  import TheNavigation from '@/components/TheNavigation.vue'

  import { ref, inject } from 'vue'
  import { onMounted } from 'vue';
  import { useToast } from 'primevue';

  const Api = inject('Api')
  const toast = useToast()
  const isSidebarOpen = ref(true)
  const enums = ref(null)
  // refresh enums once refresh the page
  onMounted(async () => { await getEnums() })

  async function getEnums() {

    enums.value = await Api.get('/enums')  // error will be handled globally
    try {
      localStorage.setItem('cachedEnums', JSON.stringify(enums.value))
    } catch (err) {
      console.log(err)
      toast.add({ severity: 'error', summary: 'Error Message', detail: err.customMessage })
    }
  }


</script>

<style module></style>
