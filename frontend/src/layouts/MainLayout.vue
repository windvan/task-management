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
  import { ref } from 'vue'

  import { onMounted } from 'vue';
  import { useEnumsStore } from '../stores/enumsStore'

  onMounted(async () => {
    await useEnumsStore().getEnums()

  })


  const isSidebarOpen = ref(true)

</script>

<style module>

</style>
