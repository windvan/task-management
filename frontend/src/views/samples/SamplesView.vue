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
      <Column field="product_name" header="Product Name"></Column>
      <Column field="sample_name" header="Sample Name">
        <template #body="{ data, field }">
          <Button
            :label="data[field]"
            variant="link"
            @click="handleShowSampleForm('edit', data)"
            class="px-0 text-left"></Button>
        </template>
      </Column>
      <Column field="batch_number" header="Batch Number"></Column>
      <Column
        field="sealing_number"
        header="Sealing Number"
        class="w-20"></Column>
      <Column field="production_date" header="Production Date"></Column>
      <Column field="expiration_date" header="Expiration Date"></Column>
      <Column field="estimated_quantity" header="Estimated Quantity">
        <template #body="{ data }">
          {{ data.estimated_quantity }} {{ data.estimated_quantity_unit }}
        </template>
      </Column>
      <Column field="received_quantity" header="Received Quantity">
        <template #body="{ data }">
          {{ data.received_quantity }} {{ data.received_quantity_unit }}
        </template>
      </Column>
      <Column field="shipped_quantity" header="Shipped Quantity"></Column>
      <Column
        field="receiver_information"
        header="Receiver Information"></Column>

      <template #expansion="{ data }">
        <div
          class="mt-4 flex flex-col gap-4 rounded"
          @click="selectedSample = data">
          <div class="flex gap-4 items-center">
            <p class="text-xl">Contacts</p>
            <Button
              icon="pi pi-plus"
              rounded
              variant="outlined"
              @click="handleExtendTask()"></Button>

            <Button
              icon=" pi pi-trash"
              rounded
              variant="outlined"
              @click="handleDeleteContact(data)"></Button>
          </div>

          <DataTable
            :value="data.tasks"
            dataKey="id"
            scrollable
            scrollHeight="flex"
            selectionMode="single"
            v-model:selection="selectedContact"
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
              <p class="text-center text-primary">No Contacts Found!</p>
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
      :headerText="sampleFormHeaderText"
      :initialFormData="initialSample"
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
  let sampleFormHeaderText = "";
  let initialSample = null;

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
      sampleFormHeaderText = "Create Sample";
    } else if (mode === "edit") {
      sampleFormHeaderText = "Edit Sample";
    }
    initialSample = data;
    showSampleForm.value = true;
  }

  async function handleDeleteSample(data) {
    await Api.delete(`cros/contacts/${selectedContact.value.id}`);
    data.contacts = await Api.get(`cros/${data.id}/contacts`);
    selectedContact.value = null;
  }

  async function handleRefreshSample() {
    sample_list.value = await Api.get("/samples/");
  }

  async function onRowExpand(event) {
    event.data.tasks = await Api.get(`samples/${event.data.id}/tasks`);
  }
</script>

<style module></style>
