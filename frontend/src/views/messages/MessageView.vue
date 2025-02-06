<template>
  <div>
    <h1>Event Messages</h1>
    <ul>
      <li v-for="(message, index) in messages" :key="index">
        {{ message }}
      </li>
    </ul>
  </div>
</template>

<script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'

  const eventSource = ref(null)
  const messages = ref([])
  const reconnectInterval = ref(5000) // 5秒后重连
  const maxReconnectAttempts = ref(5)
  const reconnectAttempts = ref(0)

  const createEventSource = () => {
    eventSource.value = new EventSource('http://127.0.0.1:8000/sse')

    eventSource.value.onmessage = (event) => {
      // const data = JSON.parse(event.data)
      messages.value.push(event.data)
      reconnectAttempts.value = 0 // 重置重连尝试次数
    }

    eventSource.value.onerror = (error) => {
      console.error('EventSource failed:', error)
      closeEventSource()
      reconnect()
    }
  }

  const closeEventSource = () => {
    if (eventSource.value) {
      eventSource.value.close()
      eventSource.value = null
    }
  }

  const reconnect = () => {
    if (reconnectAttempts.value < maxReconnectAttempts.value) {
      reconnectAttempts.value++
      console.log(
        `Attempting to reconnect (${reconnectAttempts.value}/${maxReconnectAttempts.value})`
      )
      setTimeout(() => {
        createEventSource()
      }, reconnectInterval.value)
    } else {
      console.error('Max reconnect attempts reached')
    }
  }

  onMounted(() => {
    createEventSource()
  })

  onBeforeUnmount(() => {
    closeEventSource()
  })
</script>
