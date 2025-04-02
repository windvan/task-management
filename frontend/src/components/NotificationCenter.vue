<template>

  <Popover ref="poRef" appendTo="self" class="popover">
    Notification Center Content
  </Popover>

</template>

<script setup>
  import { useTemplateRef } from "vue"

  const poRef = useTemplateRef('poRef')
  // 暴露方法给父组件
  defineExpose({
    toggle: (event) => poRef.value?.toggle(event),
  });



</script>

<style module></style>
