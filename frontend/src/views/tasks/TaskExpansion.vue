<template>
  <div>
    <p>Task Expand</p>
    <div>{{task}}</div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  const {task}=defineProps(['task'])

</script>