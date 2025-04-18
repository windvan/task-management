<template>
  <div>
    <Toolbar class="min-w-100 mb-3">
      <template #start>
        <Button icon="pi pi-plus" label="New" severity="primary" size="small" @click="handleShowSampleForm('new')" />
      </template>
      <template #end>
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText v-model="filters['global'].value" placeholder="Search Sample" v-tooltip="'Search by Product Name, Sample Name, Batch Number, Sealing Number'
            " size="small" type="search" />
        </IconField>
      </template>
    </Toolbar>

    <DataTable :value="sample_list" v-model:selection="selectedSample" v-model:expandedRows="expandedRows"
      v-model:filters="filters" :globalFilterFields="globalFilterFields" @rowExpand="onRowExpand" scrollable
      selectionMode="single" dataKey="id" resizableColumns columnResizeMode="expand" showGridlines
      tableStyle="min-width: 50rem" size="small">
      <Column expander class="w-12" frozen />
      <Column field="product_internal_name" header="Product Name"></Column>
      <Column field="sample_name" header="Sample Name">
        <template #body="{ data, field }">
          <Button :label="data[field]" variant="link" @click="handleShowSampleForm('edit', data)"
            class="px-0 text-left"></Button>
        </template>
      </Column>
      <Column field="sample_status" header="Sample Status"></Column>
      <Column field="sample_quantity" header="Sample Quantity"></Column>
      <Column field="batch_number" header="Batch Number"></Column>
      <Column field="sealing_number" header="Sealing Number" class="w-20"></Column>
      <Column field="production_date" header="Production Date"><template #body="{ data, field }">
          {{ toLocalStr(data[field]) }}</template></Column>
      <Column field="expiration_date" header="Expiration Date"><template #body="{ data, field }">
          {{ toLocalStr(data[field]) }}</template></Column>

      <Column field="shipped_quantity" header="Shipped Quantity"></Column>
      <Column field="receiver_information" header="Receiver Information"></Column>
      <Column header="Action">
        <template #body="{ data }">
          <Button icon=" pi pi-trash" rounded variant="outlined" @click="handleDeleteSample(data.id)"></Button>
        </template>
      </Column>
      <template #expansion="{ data }">
        <div class="mt-4 flex flex-col gap-4 rounded" @click="selectedSample = data">
          <div class="flex gap-4 items-center">
            <p class="text-xl">Tasks</p>
          </div>

          <DataTable :value="data.tasks" dataKey="id" scrollable scrollHeight="flex" selectionMode="single"
            v-model:selection="selectedTask" showGridlines resizableColumns columnResizeMode="expand">
            <Column selectionMode="single" class="w-8"></Column>
            <Column field="project_name" header="Project Name"></Column>
            <Column field="task_name" header="Task Name"></Column>
            <Column field="task_status" header="Task Status"></Column>
            <Column field="task_progress" header="Task Progress"></Column>
            <Column field="task_owner" header="Task Owner"></Column>
            <Column header="Action">
              <template #body="props">
                <Button icon=" pi pi-trash" rounded variant="outlined"
                  @click="handleDeleteSampleTask(data.id, props.data.id)"></Button>
              </template>
            </Column>

            <template #empty>
              <p class="text-center text-primary">No Task Found!</p>
            </template>
          </DataTable>
          <Button icon="pi pi-plus" label="Add" variant="outlined" @click="handleAddSampleTask(data.id)"></Button>
        </div>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Sample Found!</p>
      </template>
    </DataTable>
    <SampleForm v-if="showSampleForm" v-bind="sampleFormData" @close="showSampleForm = false"
      @refresh="handleRefreshSample">
    </SampleForm>
    <AddSampleTask v-if="showAddSampleTask" v-bind="addSampleTaskProps" @close="showAddSampleTask = false"
      @refresh="handleRefreshSampleTasks">
    </AddSampleTask>
  </div>
</template>

<script setup>
  import SampleForm from "./SampleForm.vue";
  import { useRoute } from "vue-router";
  import { onMounted, ref, inject } from "vue";
  import { FilterMatchMode } from "@primevue/core/api";
  import AddSampleTask from "./AddSampleTask.vue";
  import { toLocalStr } from "../../composables/dateTools";
  // import { useErrorStore } from "../../stores/errorStore";
  const route = useRoute();

  const Api = inject("Api")
  const sample_list = ref([]);
  const expandedRows = ref([]);

  // cro form use
  const selectedSample = ref();
  const showSampleForm = ref(false);
  let sampleFormData = { header: "", initialFormData: null };

  const showAddSampleTask = ref(false);
  const selectedTask = ref();
  const addSampleTaskProps = ref({ sample_id: null });

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });
  const globalFilterFields = [
    "sample_name",
    "product_name",
    "batch_number",
    "sealing_number",
  ];

  onMounted(async () => {

    sample_list.value = await Api.get("/samples/");
    filters.value.global.value = sample_list.value.find(
      (sample) => sample.id == route.query.id
    )?.sample_name;
  });

  async function handleShowSampleForm(mode, data = null) {
    if (mode === "new") {
      sampleFormData.header = "Create Sample";
      sampleFormData.initialFormData = null;
    } else if (mode === "edit") {
      sampleFormData.header = "Edit Sample";
      const product = {
        id: data.product_id,
        internal_name: data.product_internal_name,
      };
      sampleFormData.initialFormData = { ...data, product: product };
    }
    // transform data here

    showSampleForm.value = true;
  }
  function handleAddSampleTask(sample_id) {
    addSampleTaskProps.value.sample_id = sample_id;
    showAddSampleTask.value = true;
  }

  async function handleDeleteSample(sample_id) {
    await Api.delete(`samples/${sample_id}`);
    sample_list.value = await Api.get("/samples/");
    selectedSample.value = null;
  }

  async function handleDeleteSampleTask(sample_id, task_id) {
    await Api.delete(`samples/${sample_id}/tasks/${task_id}`);
    const index = sample_list.value.findIndex(
      (sample) => sample.id === sample_id
    );
    if (index !== -1) {
      sample_list.value[index].tasks = await Api.get(
        `samples/${sample_id}/tasks`
      );
    }

    selectedSample.value = null;
  }

  async function handleRefreshSample() {
    sample_list.value = await Api.get("/samples/");
  }

  async function onRowExpand(event) {
    event.data.tasks = await Api.get(`samples/${event.data.id}/tasks`);
  }

  async function handleRefreshSampleTasks(Sample_id) {
    const index = sample_list.value.findIndex(
      (sample) => sample.id === Sample_id
    );
    if (index !== -1) {
      sample_list.value[index].tasks = await Api.get(
        `samples/${Sample_id}/tasks`
      );
    }
  }
</script>

<style module></style>
