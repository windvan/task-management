<template>
  <div :class="label + '-view'">This is {{ label }} view
    <div class="box">
      <Button label="Primary" :pt:root:style:color="'red'"/>
      <Button label="Secondary" severity="secondary" />
      <Button label="Success" severity="success" />
      <Button label="Info" severity="info" />
      <Button label="Warn" severity="warn" />
      <Button label="Help" severity="help" />
      <Button label="Danger" severity="danger" />
      <Button label="Contrast" severity="contrast" />
    </div>
  </div>


</template>

<script setup>
  import { useRoute } from 'vue-router';
  const route = useRoute().path
  const label = route.split('/').pop()
</script>

<style scoped>
  .box {
    display: flex;
    gap: 20px;
    margin-top: 50px;
  }
</style>
