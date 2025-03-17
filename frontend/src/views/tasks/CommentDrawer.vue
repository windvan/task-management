<template>
  <Drawer
    v-model:visible="visible"
    @hide="emit('close')"
    :position="position"
    class="w-[40rem]"
  >
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <Button
          severity="secondary"
          variant="text"
          :icon="
            'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          "
          @click="togglePosition"
        ></Button>
      </div>
    </template>

    project_id:{{ project_id }}
    <template #footer>
      <div class="flex items-center gap-2">
        <Button
          label="Add Comment"
          icon="pi pi-plus"
          class="flex-auto"
          outlined
        ></Button>
      </div>
    </template>
  </Drawer>
</template>

<script setup>
import { ref } from "vue";

const { project_id, task_id } = defineProps(["project_id", "task_id"]);
const emit = defineEmits(["close"]);
const visible = ref(true);
const position = ref("right");
function togglePosition() {
  position.value = position.value === "full" ? "right" : "full";
}
</script>
