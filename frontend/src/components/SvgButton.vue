<template>
  <button class="defaultIconBtn" :style="btnStyle" @click="clickHandler">
    <svg aria-hidden="true" width="50%" height="50%" :color="color">
      <use :href="symbolId" />
    </svg>
  </button>
</template>

<script setup name="SvgButton">
  import { computed, reactive } from 'vue'

  const props = defineProps({
    prefix: {
      type: String,
      default: 'icon'
    },
    name: {
      type: String,
      required: true
    },

    size: {
      type: [Number, String],
      default: '2em'
    },
    color: {
      type: String,
      default: '#000'
    },
    fill: {
      type: String,
      default: '#FFF'
    }
  })
  const emit = defineEmits(['click-icon'])

  const symbolId = computed(() => `#${props.prefix}-${props.name}`)
  const btnStyle = reactive({ width: props.size, height: props.size, backgroundColor: props.fill })
  const clickHandler = () => {
    emit('click-icon')
  }
</script>

<style scoped>
  .defaultIconBtn {
    /* default style, can be over-writed throgh component class
           style defined by props(width,height,color background-color) can not be over-writed through component class
        */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    padding-block: 0;
    padding-inline: 0;
  }

  .defaultIconBtn:hover {
    filter: brightness(0.8);
  }
</style>
