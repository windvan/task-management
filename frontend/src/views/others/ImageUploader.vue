<template>
  <div class="image-uploader" @paste="onPaste" tabindex="0">
    <FileUpload
      :customUpload="true"
      @uploader="onUpload"
      :multiple="false"
      accept="image/*"
      :auto="true"
      chooseLabel="选择图片"
    >
      <template #empty>
        <p>拖放图片到此处、点击选择或粘贴图片</p>
      </template>
    </FileUpload>
    <div v-if="imageUrl" class="preview-container">
      <img :src="imageUrl" @click="showFullImage" class="preview-image" alt="Preview" />
    </div>
  </div>
</template>

<script>
  import { ref, onMounted, onUnmounted } from 'vue'
  import FileUpload from 'primevue/fileupload'

  export default {
    components: {
      FileUpload
    },
    props: {
      modelValue: String
    },
    emits: ['update:modelValue'],
    setup(props, { emit }) {
      const imageUrl = ref(props.modelValue)

      const processFile = (file) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          imageUrl.value = e.target.result
          emit('update:modelValue', e.target.result)
        }
        reader.readAsDataURL(file)
      }

      const onUpload = (event) => {
        const file = event.files[0]
        processFile(file)
      }

      const onPaste = (event) => {
        const items = (event.clipboardData || event.originalEvent.clipboardData).items
        for (let index in items) {
          const item = items[index]
          if (item.kind === 'file') {
            const blob = item.getAsFile()
            processFile(blob)
            break
          }
        }
      }

      const showFullImage = () => {
        // 实现图片放大查看的逻辑
        // 可以使用 PrimeVue 的 Dialog 组件或其他方式
      }

      // 全局粘贴事件处理
      const handleGlobalPaste = (event) => {
        if (
          document.activeElement === event.target ||
          document.activeElement.contains(event.target)
        ) {
          onPaste(event)
        }
      }

      onMounted(() => {
        document.addEventListener('paste', handleGlobalPaste)
      })

      onUnmounted(() => {
        document.removeEventListener('paste', handleGlobalPaste)
      })

      return {
        imageUrl,
        onUpload,
        onPaste,
        showFullImage
      }
    }
  }
</script>

<style scoped>
  .image-uploader {
    display: flex;
    align-items: center;
    outline: none; /* 移除 focus 时的轮廓 */
  }
  .preview-container {
    margin-left: 1rem;
  }
  .preview-image {
    width: 50px;
    height: 50px;
    object-fit: cover;
    cursor: pointer;
  }
</style>
