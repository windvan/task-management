<template>
  <div :class="label + '-view'">This is {{ label }} view</div>
</template>

<script setup>
  import { useRoute } from 'vue-router';
  const route = useRoute().path
  const label = route.split('/').pop()
</script>

<style scoped></style>
