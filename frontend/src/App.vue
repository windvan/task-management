<script setup>
  import { RouterView } from 'vue-router'
</script>

<template>
  <Toast position="top-center" :pt="{summary:'leading-4'}"></Toast>
  <RouterView />
</template>
