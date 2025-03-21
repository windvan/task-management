<template>
  <Dialog
    v-model:visible="visible"
    modal
    maximizable
    @hide="emit('close')"
    :style="{ width: '80%' }"
  >
    <template #header>
      <span class="text-xl font-bold">Gap Details</span>
      <div class="flex gap-8">
        <Button icon="pi pi-trash" rounded outlined></Button>
        <Button icon="pi pi-pencil" rounded outlined></Button>
        <Button
          icon="pi pi-check"
          rounded
          outlined
          @click="handleSaveGap"
        ></Button>
      </div>
    </template>
    <div v-if="gap_id">
      <Image
        :src="staticBaseUrl + gap?.snapshot_url"
        class="h-64 w-full"
        preview
        pt:toolbar="bg-surface-600"
      />

      <pre>{{ gap }}</pre>
    </div>
    <div v-else>
      <FileUpload
        ref="fileUploadRef"
        name="gap_snapshot"
        :fileLimit="1"
        mode="advanced"
        accept="image/*"
        :maxFileSize="1048576"
      >
        <template #header="{ files, chooseCallback }">
          <Button
            icon="pi pi-plus"
            label="Choose"
            size="small"
            @click="chooseCallback"
            v-show="files.length === 0"
          ></Button>
        </template>
        <template #empty>
          <span>Drag and drop image to here to upload.</span>
        </template>
      </FileUpload>

      <div
        class="flex flex-col border border-surface-200 rounded mt-2 p-4 gap-2"
      >
        <div v-for="(value, key) in gap_detail" :key="key" class="flex">
          <label :for="key">{{ key }}</label>
          <input
            :id="key"
            type="text"
            v-model="gap_detail[key]"
            class="border border-surface-400 rounded ml-2 focus:border-primary focus:border"
          />
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, useTemplateRef, inject, onMounted, nextTick } from "vue";
import { useToast } from "primevue";
const Api = inject("Api");
const fileUploadRef = useTemplateRef("fileUploadRef");
const toast = useToast();
const staticBaseUrl = import.meta.env.VITE_API_STATIC_BASE_URL;
const visible = ref(true);
const { task_id, gap_id } = defineProps({
  task_id: Number,
  gap_id: Number,
});

const emit = defineEmits(["refresh", "close"]);

const gap = ref();

onMounted(async () => {
  // await nextTick()
  if (gap_id) {
    gap.value = await Api.get(`/gaps/${gap_id}`);
  }
});

function handleDeleteGap() {
  // delete image if no related tasks othetwhise unrelate

  toast.add({
    severity: "warn",
    summary: "Warn Message",
    detail: "To be implemented",
    life: 3000,
  });
}

const gap_detail = ref({
  crop_name: "",
  crop_name_cn: "",
  control_target: "",
  control_target_cn: "",
  app_rate_min: null,
  app_rate_max: null,
  water_volumn_min: null,
  water_volumn_max: null,
  app_method: null,
  app_number: null,
  app_interval_min: null,
  app_time: null,
  app_time_bbch: null,
  phi: null,
  additional_comments: null,
  app_rate_unit: "g a.i./ha",
  water_volumn_unit: "L/ha",
});

async function handleSaveGap() {
  // save gap data and update related task.gap_id
  console.log(fileUploadRef.value)
  const file = fileUploadRef.value.files[0];

  const formData = new FormData();
  formData.append("file", file);

  // Add other data fields to formData as needed
  formData.append("gap_detail", JSON.stringify(gap_detail.value));

  const response = await Api.post(`/gaps?task_id=${task_id}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

// emit('refresh');
</script>
