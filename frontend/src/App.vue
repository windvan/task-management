<script setup>
  import { RouterView } from 'vue-router'
  import { watchEffect } from 'vue';
  import { useErrorStore } from './stores/errorStore';
  import { useToast } from 'primevue';

  const { message, resetMessage } = useErrorStore()
  const toast = useToast()

  watchEffect(async () => {
    toast.add(message);// add message to toast
    resetMessage();// reset message 
  })
</script>

<template>
  <Toast position="top-center" :pt="{ summary: 'leading-4' }"></Toast>

  <RouterView />
</template>
