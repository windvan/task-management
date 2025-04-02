<template>
  <Drawer v-model:visible="visible" :position :style="{ width: '40rem' }" @hide="emit('close')">

    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Key Results</span>
        <div>
          <!-- <Button v-if="!results" severity="secondary" label="Add" variant="text" :icon="'pi pi-plus'
            " @click="handleShowEditBox('new')"></Button> -->
          <Button v-if="!showEditBox" severity="secondary" label="Edit" variant="text" :icon="'pi pi-pencil'
            " @click="handleShowEditBox('eidt')"></Button>
          <Button v-if="showEditBox" severity="secondary" label="Save" variant="text" :icon="'pi pi-save'
            " @click="handleSave"></Button>
          <Button v-if="showEditBox" severity="secondary" label="Cancel" variant="text" :icon="'pi pi-save'
            " @click="handleCancel"></Button>
        </div>

        <Button severity="secondary" variant="text" :icon="'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          " @click="togglePosition"></Button>
      </div>
    </template>
    <Textarea v-if="showEditBox" v-model="results" autoResize fluid class="min-h-48"></Textarea>
    <div v-else class="border border-surface-200 rounded-sm min-h-48 p-4 whitespace-pre-wrap">
      <pre>{{ results }}</pre>
    </div>

  </Drawer>

</template>

<script setup>
  import { ref, inject } from 'vue';
  const Api = inject('Api')
  const visible = ref(true)
  const emit = defineEmits(["close", "refresh"]);
  const { content, taskId } = defineProps({ content: String, taskId: Number })
  const results = ref(content)
  const position = ref("right");
  function togglePosition() {
    position.value = position.value === "full" ? "right" : "full";
  }


  const showEditBox = ref(!Boolean(content))
  function handleShowEditBox(mode) {
    showEditBox.value = true
  }
  async function handleSave() {
    const updatedTask = await Api.patch(`/tasks/${taskId}`, { key_results: results.value })
    emit('refresh', updatedTask)
    showEditBox.value = false
  }

  function handleCancel() {
    results.value = content
    showEditBox.value = false

  }
</script>