<template>
  <div class="icons-view">
    <h1>Icons List</h1>
    <div class="icons-container">
      <div v-for="(clsName, index) in clsList" :key="index" class="icon">
        <i :class="clsName"></i>
        <p>{{ clsName }}</p>
      </div>
    </div>
    <h1>Components List</h1>
    <div class="componnet-container"></div>
  </div>
</template>

<script setup>
  import { PrimeIcons } from '@primevue/core/api';
  import { computed } from 'vue'


  const clsList = computed(() => {
    return Object.values(PrimeIcons)
  })


</script>

<style scoped>
  .icon {
    display: inline-flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    width: 120px;

    border: none;
    margin: 10px;
    padding: 10px;
    box-shadow: 0 0 5px red;
  }

  .icon>p {
    font-size: 12px;
  }

  .icons-container,
  .components-container {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    margin: 20px;
  }
</style>
