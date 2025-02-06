<template>
  <svg aria-hidden="true" :width="size" :height="size" :color="color">
    <use :href="symbolId" />
  </svg>
</template>

<script setup name="SvgIcon">
  import { computed } from 'vue'

  const props = defineProps({
    prefix: {
      type: String,
      default: 'icon'
    },
    name: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: '#000'
    },
    size: {
      type: [Number, String],
      default: '1em'
    }
  })

  const symbolId = computed(() => `#${props.prefix}-${props.name}`)
</script>
