<template>
  <div>
    <DataTable ref="tableRef" :value="products" v-model:selection="selectedProducts" v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand" scrollable selectionMode="single" dataKey="id" paginator v-model:filters="filters"
      :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" :globalFilterFields="globalFilterFields"
      tableStyle="min-width: 50rem" pt:header="px-0">
      <template #header>
        <Toolbar pt:start="gap-2">
          <template #start>
            <Button icon="pi pi-plus" label="New" @click="handleOpenForm('new')" severity="secondary" />
            <Button icon="pi pi-trash" label="Delete" @click="handleDelete" severity="secondary" />
          </template>

          <template #center>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <!-- , dt: { color: '{gray.900}', background: '{gray.100}', maxWidth: '30rem', shadow:'none'}  -->
              <InputText v-tooltip.top="{ value: 'Search by Product/Trade Name, AI, Stage, A Number' }"
                placeholder="Search" v-model="filters['global'].value" />
            </IconField>
          </template>

          <template #end>
            <SplitButton severity="secondary" label="Export" icon="pi pi-download" @click="handleExport"
              :model="splitBtnItems">
            </SplitButton>
          </template>
        </Toolbar>
      </template>


      <Column expander style="width: 3rem"></Column>
      <Column field="internal_name" header="Internal Name" frozen>
        <template #body="{ data }">
          <Button :label="data.internal_name" variant="link" @click="handleOpenForm('edit', data)"></Button> </template>
      </Column>
      <Column field="lead_ai" header="Lead AI"></Column>
      <Column field="stage" header="Stage">
        <template #body="{ data }">
          <Tag :severity="data.stage >= 'stage_C' ? 'success' : 'warn'" :value="data.stage"></Tag>
        </template>
      </Column>
      <Column field="a_number" header="A Number"></Column>
      <Column field="product_name" header="Product Name"></Column>
      <Column field="product_name_cn" header="Product Name (CN)"></Column>
      <Column field="trade_name" header="Trade Name"></Column>
      <Column field="product_origin" header="Product Origin"></Column>
      <Column field="is_three_new" header="Three-New">
        <template #body="{ data }">
          <span :class="{ 'font-bold text-orange-500': data.is_three_new }">{{
            data.is_three_new ? "Yes" : "No"
          }}</span>
        </template>
      </Column>
      <Column header="Action">
        <template #body="{ data }">
          <Button icon="pi pi-trash" @click="handleDeleteProduct(data.id)" rounded outlined></Button>
        </template>
      </Column>
      <template #expansion="{ data, index }">
        <div>
          {{ data.ais }}
        </div>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Products Found!</p>
      </template>


    </DataTable>

    <ConfirmDialog></ConfirmDialog>

    <!-- #Region Product Form -->

    <ProductForm v-if="showProductForm" :initialFormData @close="handleCloseForm" @refresh="handleRefresh" />

    <!-- #endregion -->


  </div>
</template>

<script setup>
  import { onMounted, inject, ref, useTemplateRef, toRaw } from "vue";

  import { useToast } from "primevue/usetoast";
  import { useConfirm } from "primevue/useconfirm";
  import { FilterMatchMode } from "@primevue/core";
  import ProductForm from "./ProductForm.vue";

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  const toast = useToast();
  const confirm = useConfirm();
  const Api = inject("Api");
  const tableRef = useTemplateRef("tableRef");

  const products = ref([]);
  const selectedProducts = ref([]);
  const expandedRows = ref([]);




  const splitBtnItems = [
    { label: "Import", icon: "pi pi-upload", command: handleImport },
  ];


  const globalFilterFields = [
    "internal_name",
    "lead_ai",
    "stage",
    "a_number",
    "product_name_cn",
    "trade_name",
  ];

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
  });

  onMounted(async () => {
    products.value = await Api.get("/products/");
  });

  function handleImport() {
    toast.add({
      severity: "warn",
      summary: "Warn Message",
      detail: "To be implemented",
      life: 3000,
    });
  }

  function handleExport() {
    tableRef.value.exportCSV();
  }




  const showProductForm = ref(false);
  const initialFormData = ref();
  function handleOpenForm(mode, data = null) {
    if (mode === 'new') {
      initialFormData.value = {};
    } else if (mode === 'edit') {
      initialFormData.value = data;
    }
    showProductForm.value = true;
  }




  function handleCloseForm() {
    showProductForm.value = false;
  }


  async function handleDeleteProduct(product_id) {

    confirm.require({
      position: "top",
      message: "Are you sure you want delete?",
      header: "Confirmation",
      icon: "pi pi-exclamation-triangle",
      rejectProps: {
        label: "Cancel",
        severity: "secondary",
        outlined: true,
      },
      acceptProps: {
        label: "Confirm",
      },
      accept: async () => {

        let response;
        response = await Api.delete(`/products/${product_id}`);
        //refresh products
        products.value = await Api.get("/products");

      },
      reject: null,
    });
  }

  async function handleRefresh() {
    products.value = await Api.get("/products");
  }

  async function onRowExpand(event) {
    event.data.ais = await Api.get(`/products/${event.data.id}/ais`);
  }
</script>



<style module></style>
