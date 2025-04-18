<script setup>
  import { provide,onMounted } from 'vue';
  import { RouterView } from 'vue-router'
  import useApi from './composables/useApi';
  onMounted(() => {
    provide('Api', useApi())
  })
</script>

<template>
  <Toast position="top-center" />
  <RouterView />
</template>
