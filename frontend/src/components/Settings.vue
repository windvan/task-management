<template>

  <Drawer v-model:visible="visible" header="Settings" class="w-96" :position  @hide="emit('close')">
    Settings
  </Drawer>

</template>

<script setup>
  import { useTemplateRef ,ref} from "vue"
 
  const emit=defineEmits(['close'])
  const visible = ref(true)
  const position = ref("right");


</script>

<style module></style>
