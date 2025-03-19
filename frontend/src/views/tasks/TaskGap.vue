<template>
  <Dialog
    v-model:visible="visible"
    modal
    maximizable
    header="Gap Snapshots"
    @hide="emit('close')"
    :style="{ width: '80%' }"
  >
    <div v-if="gap_snapshot_url">
      <Image
        :src="gap_snapshot_url"
        class="h-64 w-full"
        preview
        @contextmenu="onImageRightClick"
      />
      <ContextMenu ref="menu" :model="menuItems"> </ContextMenu>
    </div>

    <FileUpload
      v-else
      name="gap_snapshot"
      :multiple="false"
      mode="advanced"
      customUpload
      @uploader="handleUploadGap"
      accept="image/*"
      :maxFileSize="1048576"
    >
      <template #empty>
        <span>Drag and drop image to here to upload.</span>
      </template>
    </FileUpload>
  </Dialog>
</template>

<script setup>
import { ContextMenu } from "primevue";
import { ref, useTemplateRef } from "vue";
import { useToast } from "primevue";
const toast = useToast();
const staticBaseUrl = import.meta.env.VITE_API_STATIC_BASE_URL;
const visible = ref(true);
const { task_id, gap_id, gap_snapshot_url } = defineProps({
  task_id: Number,
  gap_id: Number,
  gap_snapshot_url: String,
});

const emit = defineEmits(["refresh", "close"]);
const menu = useTemplateRef("menu");
const menuItems = ref([
  { label: "Delete", icon: "pi pi-trash", command: handleDeleteGap },
]);
function onImageRightClick(event) {
  menu.value.show(event);
}

function handleDeleteGap() {
  // delete image if no related tasks othetwhise unrelate
  toast.add({
    severity: "warn",
    summary: "Warn Message",
    detail: "To be implemented",
    life: 3000,
  });
}

async function handleUploadGap(event) {
  const formData = new FormData();

  event.files.forEach((file) => {
    formData.append("files", file);
  });

  try {
    let response = await Api.post(
      `/tasks/gaps/${currentTaskGaps.value.task_id}`,
      formData
    );
    currentTaskGaps.value.gapURLs = response.data.gap_snapshot.split(",");
    tasks.value[currentTaskGaps.value.index].gap_snapshot =
      response.data.gap_snapshot;
  } catch (error) {
    console.log(error);
  }
}
</script>
