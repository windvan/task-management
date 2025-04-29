<script setup>
  import { provide,onMounted } from 'vue';
  import { RouterView } from 'vue-router'
  import useApi from './composables/useApi';
import { ConfirmDialog } from 'primevue';
  
  provide('Api', useApi())
  
</script>

<template>
  <Toast position="top-center" />
  <ConfirmDialog></ConfirmDialog>
  <RouterView />
</template>
