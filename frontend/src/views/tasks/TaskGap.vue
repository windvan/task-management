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
        <Button
          v-show="disabled"
          icon="pi pi-trash"
          rounded
          outlined
          @click="handleDeleteGap"
        ></Button>
        <!-- <Button
          v-show="disabled"
          icon="pi pi-pencil"
          rounded
          outlined
          @click="handleEditGap"
        ></Button> -->
        <Button
          v-show="!disabled"
          icon="pi pi-check"
          rounded
          outlined
          @click="handleSaveGap"
        ></Button>
      </div>
    </template>

    <Image
      v-if="gap_id"
      :src="staticBaseUrl + gap?.snapshot_url"
      class="h-64 w-full border border-surface-200 rounded"
      preview
      pt:toolbar="bg-surface-600"
    />

    <FileUpload
      v-else
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
      class="grid md:grid-cols-2 grid-cols-1 gap-8 border border-surface-200 rounded mt-4 p-2"
    >
      <div class="flex flex-col grow gap-4">
        <div class="flex text-nowrap items-center">
          <label for="crop_name" class="mr-2">Crop Name</label>
          <InputText
            v-model="gap_detail['crop_name']"
            id="crop_name"
            fluid
            :disabled
          />
        </div>
        <div class="flex text-nowrap items-center">
          <label for="crop_name_cn" class="mr-2">Crop Name(CN)</label>
          <InputText
            v-model="gap_detail['crop_name_cn']"
            id="crop_name_cn"
            fluid
            :disabled
          />
        </div>
        <div class="flex text-nowrap items-center">
          <label for="control_target" class="mr-2">Control Target</label>
          <InputText
            v-model="gap_detail['control_target']"
            id="control_target"
            fluid
            :disabled
          />
        </div>
        <div class="flex text-nowrap items-center">
          <label for="control_target_cn" class="mr-2">Control Target(CN)</label>
          <InputText
            v-model="gap_detail['control_target_cn']"
            id="control_target_cn"
            fluid
            :disabled
          />
        </div>

        <div class="flex text-nowrap items-center">
          <label for="phi" class="mr-2">PHI</label>
          <InputText v-model="gap_detail['phi']" id="phi" fluid :disabled />
        </div>
        <div class="flex text-nowrap items-center">
          <label for="app_time_bbch" class="mr-2">Application Time(BBCH)</label>
          <InputText
            v-model="gap_detail['app_time_bbch']"
            id="app_time_bbch"
            fluid
            :disabled
          />
        </div>
      </div>
      <div class="flex flex-col grow gap-4">
        <div class="flex text-nowrap items-center">
          <label for="app_rate" class="mr-2">Application Rate</label>
          <InputText
            v-model="gap_detail['app_rate_min']"
            id="app_rate_min"
            fluid
            :disabled
          />
          <label for="app_rate" class="mx-2">-</label>
          <InputText
            v-model="gap_detail['app_rate_max']"
            id="app_rate_max"
            fluid
            :disabled
          />
          <label for="app_rate" class="ml-2">g a.i./ha</label>
        </div>
        <div class="flex text-nowrap items-center">
          <label for="water_valumn" class="mr-2">Water Valumn</label>
          <InputText
            v-model="gap_detail['water_valumn_min']"
            id="water_valumn_min"
            fluid
            :disabled
          />
          <label for="water_valumn" class="mx-2">-</label>
          <InputText
            v-model="gap_detail['water_valumn_max']"
            id="water_valumn_max"
            fluid
            :disabled
          />
          <label for="water_valumn" class="ml-2">L/ha</label>
        </div>
        <div class="flex text-nowrap items-center">
          <label for="app_method" class="mr-2">Application Method</label>
          <InputText
            v-model="gap_detail['app_method']"
            id="app_method"
            fluid
            :disabled
          />
        </div>
        <div class="flex text-nowrap items-center">
          <label for="app_number" class="mr-2">Application Number</label>
          <InputText
            v-model="gap_detail['app_number']"
            id="app_number"
            fluid
            :disabled
          />
        </div>
        <div class="flex text-nowrap items-center">
          <label class="mr-2">Application Interval</label>
          <InputText v-model="gap_detail['app_interval_min']" fluid :disabled />
          <label for="water_valumn" class="mx-2">-</label>
          <InputText v-model="gap_detail['app_interval_max']" fluid :disabled />
          <label class="ml-2">L/ha</label>
        </div>
        <div class="flex text-nowrap items-center">
          <label for="app_time" class="mr-2">Application Time</label>
          <InputText
            v-model="gap_detail['app_time']"
            id="app_time"
            fluid
            :disabled
          />
        </div>
      </div>
      <div class="flex text-nowrap items-center col-span-2">
        <label for="additional_comments" class="mr-2"
          >Additional Comments</label
        >
        <InputText
          v-model="gap_detail['additional_comments']"
          id="additional_comments"
          fluid
          :disabled
        />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, useTemplateRef, inject, onMounted, nextTick } from "vue";
import { InputText, useToast } from "primevue";
const Api = inject("Api");
const fileUploadRef = useTemplateRef("fileUploadRef");
const toast = useToast();
const staticBaseUrl = import.meta.env.VITE_API_STATIC_BASE_URL;
const visible = ref(true);
const { task_id, gap_id } = defineProps({
  task_id: Number,
  gap_id: Number,
});
const disabled = ref(gap_id ? true : false);
const emit = defineEmits(["refresh", "close"]);

const gap = ref();

onMounted(async () => {
  // await nextTick()
  if (gap_id) {
    gap.value = await Api.get(`/gaps/${gap_id}`);
  }
});

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

  const file = fileUploadRef.value.files[0];

  const formData = new FormData();
  formData.append("file", file);

  // Add other data fields to formData as needed
  formData.append("gap_detail", JSON.stringify(gap_detail.value));

  const new_gap = await Api.post(`/gaps/?task_id=${task_id}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  emit("refresh", task_id, new_gap.id);
  emit("close");
}

async function handleDeleteGap() {
  // delete image if no related tasks othetwhise unrelate
  await Api.delete(`/gaps/${gap_id}?task_id=${task_id}`);
  emit("refresh", task_id, null);
  emit("close");
}
// async function handleEditGap() {
//   disabled.value = false;
// }
</script>
