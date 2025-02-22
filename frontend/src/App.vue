<script setup>
  import { RouterView } from 'vue-router'
  import { watch } from 'vue';
  import { useErrorStore } from './stores/errorStore';
  import { useToast } from 'primevue';

  const errorStore = useErrorStore()
  const toast = useToast()

  watch(
    () => errorStore.message,
    (newMessage) => {
      if (newMessage) {
        toast.add(newMessage)
        errorStore.resetMessage()
      }
    }
  )
  
</script>

<template>
  <Toast position="top-center" :pt="{ summary: 'leading-4' }"></Toast>

  <RouterView />
</template>
