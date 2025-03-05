<template>
  <div>
    <Toolbar class="min-w-100 mb-3">
      <template #start>
        <Button
          icon="pi pi-plus"
          label="New"
          severity="primary"
          size="small"
          @click="handleShowSampleForm('new', null)" />
      </template>
      <template #end>
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText
            v-model="filters['global'].value"
            placeholder="Search Sample"
            v-tooltip="
              'Search by Product Name, Sample Name, Batch Number, Sealing Number'
            "
            size="small" />
        </IconField>
      </template>
    </Toolbar>

    <DataTable
      :value="sample_list"
      v-model:selection="selectedSample"
      v-model:expandedRows="expandedRows"
      v-model:filters="filters"
      :globalFilterFields="globalFilterFields"
      @rowExpand="onRowExpand"
      scrollable
      selectionMode="single"
      dataKey="id"
      resizableColumns
      columnResizeMode="expand"
      showGridlines
      tableStyle="min-width: 50rem"
      size="small">
      <Column expander class="w-12" frozen />
      <Column field="product_internal_name" header="Product Name"></Column>
      <Column field="sample_name" header="Sample Name">
        <template #body="{ data, field }">
          <Button
            :label="data[field]"
            variant="link"
            @click="handleShowSampleForm('edit', data)"
            class="px-0 text-left"></Button>
        </template>
      </Column>
      <Column field="sample_status" header="Sample Status"></Column>
      <Column field="sample_quantity" header="Sample Quantity"></Column>
      <Column field="batch_number" header="Batch Number"></Column>
      <Column
        field="sealing_number"
        header="Sealing Number"
        class="w-20"></Column>
      <Column field="production_date" header="Production Date"></Column>
      <Column field="expiration_date" header="Expiration Date"></Column>

      <Column field="shipped_quantity" header="Shipped Quantity"></Column>
      <Column
        field="receiver_information"
        header="Receiver Information"></Column>

      <template #expansion="{ data }">
        <div
          class="mt-4 flex flex-col gap-4 rounded"
          @click="selectedSample = data">
          <div class="flex gap-4 items-center">
            <p class="text-xl">Tasks</p>
            <Button
              icon="pi pi-plus"
              rounded
              variant="outlined"
              @click="handleExtendTask()"></Button>

            <Button
              icon=" pi pi-trash"
              rounded
              variant="outlined"
              @click="handleDeleteSample(data)"></Button>
          </div>

          <DataTable
            :value="data.tasks"
            dataKey="id"
            scrollable
            scrollHeight="flex"
            selectionMode="single"
            v-model:selection="selectedTask"
            showGridlines
            resizableColumns
            columnResizeMode="expand">
            <Column selectionMode="single" class="w-8"></Column>
            <Column field="project_name" header="Project Name"></Column>
            <Column field="task_name" header="Task Name"></Column>
            <Column field="task_status" header="Task Status"></Column>
            <Column field="task_progress" header="Task Progress"></Column>
            <Column field="task_owner" header="Task Owner"></Column>

            <template #empty>
              <p class="text-center text-primary">No Sample Found!</p>
            </template>
          </DataTable>
        </div>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Samples Found!</p>
      </template>
    </DataTable>
    <SampleForm
      v-if="showSampleForm"
      v-bind="sampleFormData"
      @close="showSampleForm = false"
      @refresh="handleRefreshSample">
    </SampleForm>
  </div>
</template>

<script setup>
  import SampleForm from "./SampleForm.vue";

  import { onMounted, ref, inject } from "vue";
  import { FilterMatchMode } from "@primevue/core/api";
  // import { useErrorStore } from "../../stores/errorStore";

  const Api = inject("Api");
  const sample_list = ref([]);
  const expandedRows = ref([]);

  // cro form use
  const selectedSample = ref();
  const showSampleForm = ref(false);
  let sampleFormData = { header: "", initialFormData: null };
  // let sampleFormHeaderText = "";
  // let initialSample = null;

  const selectedTask = ref();

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
  });

  async function handleShowSampleForm(mode, data) {
    if (mode === "new") {
      sampleFormData.header = "Create Sample";
    } else if (mode === "edit") {
      sampleFormData.header = "Edit Sample";
    }
    // transform data here
    const product = {
      id: data.product_id,
      internal_name: data.product_internal_name,
    };
    sampleFormData.initialFormData = { ...data, product: product };
    showSampleForm.value = true;
  }

  async function handleDeleteSample(data) {
    await Api.delete(`samples/${selectedSample.value.id}`);
    // data.contacts = await Api.get(`cros/${data.id}/contacts`);
    selectedSample.value = null;
  }

  async function handleRefreshSample() {
    sample_list.value = await Api.get("/samples/");
  }

  async function onRowExpand(event) {
    event.data.tasks = await Api.get(`samples/${event.data.id}/tasks`);
  }
</script>

<style module></style>
