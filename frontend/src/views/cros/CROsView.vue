<template>
  <div>
    <Toolbar class="min-w-100 mb-3">
      <template #start>
        <Button
          icon="pi pi-plus"
          label="New"
          severity="primary"
          size="small"
          @click="openNew"
        />
      </template>
      <template #end>
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText placeholder="Search" size="small" />
        </IconField>
      </template>
    </Toolbar>

    <DataTable
      :value="cro_list"
      v-model:selection="selectedCro"
      v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand"
      scrollable
      selectionMode="single"
      dataKey="id"
      resizableColumns
      showGridlines
      tableStyle="min-width: 50rem"
      size="small"
    >
      <Column expander class="w-12" frozen />
      <Column field="certification_number" header="Cert Number"></Column>
      <Column field="cro_name" header="CRO Name"></Column>
      <Column
        field="certification_expiration_date"
        header="Expiration"
      ></Column>
      <Column field="certification_scope" header="Scope"></Column>
      <Column field="fw_contract_start" header="Fw Contract Start"></Column>
      <Column field="fw_contract_end" header="Fw Contract End"></Column>
      <Column field="fw_contract_detail" header="Fw Contract Detail"></Column>
      <Column field="address" header="Address"></Column>

      <template #expansion="{ data }">
        <DataTable :value="data.contacts" dataKey="id" size="large" scrollable>
          <Column field="contact_name" header="Contact Name"></Column>
          <Column field="discipline" header="Discipline"></Column>
          <Column field="phone_number" header="Phone Number"></Column>
          <Column field="email" header="Email"></Column>
          <Column field="remarks" header="Remarks"></Column>
          <template #empty>
            <p class="text-center text-primary">No Related Tasks Found!</p>
          </template>
        </DataTable>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Cros Found!</p>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { onMounted, ref, inject } from "vue";
const $axios = inject("$axios");

const cro_list = ref([]);
const selectedCro = ref();

onMounted(async () => {
  try {
    const response = await $axios.get("/cros/");
    // 处理成功响应
    cro_list.value = response.data;

    console.log(response.data);
  } catch (error) {
    // 处理错误
    console.error("An error occurred:", error);
  }
});
async function onRowExpand(event) {
  // get tasks of current project
  try {
    let response = await $axios.get(`cros/${event.data.id}/contacts`);
    event.data.contacts = response.data;
  } catch (err) {
    if (err.status === 401) {
      toast.add({
        severity: "warn",
        summary: "Warn Message",
        detail: "Get related tasks failed!",
        life: 3000,
      });
    }
  }
}
</script>

<style module></style>
