<template>
  <div>
    <DataTable ref="tableRef" :value="products" v-model:selection="selectedProducts" v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand" scrollable selectionMode="single" dataKey="id" paginator v-model:filters="filters"
      :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" :globalFilterFields="globalFilterFields"
      tableStyle="min-width: 50rem" pt:header="px-0">
      <template #header>
        <Toolbar pt:start="gap-2">
          <template #start>
            <Button icon="pi pi-plus" label="New" @click="handleOpenProductForm('new')" severity="secondary" />

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
      <Column field="internal_name" header="Internal Name" class="text-nowrap px-0" frozen>
        <template #body="{ data }">
          <Button :label="data.internal_name" variant="link" class="px-0"
            @click="handleOpenProductForm('edit', data)"></Button>
        </template>
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
        <div class="mt-4 flex flex-col gap-4" @click="selectedSample = data">
          <div class="flex gap-4 items-center">
            <p class="text-xl">Product Ais</p>
            <Button icon="pi pi-plus" label="Add" size="small" outlined @click="handleOpenAiForm('new', data)"></Button>
          </div>

          <DataTable :value="data.ais" dataKey="id" scrollable scrollHeight="flex" selectionMode="single"
            v-model:selection="selectedAi" showGridlines resizableColumns columnResizeMode="expand">
            <Column selectionMode="single" class="w-8"></Column>
            <Column field="abbreviation" header="Abbreviation">
              <template #body="props">
                <Button :label="props.data.abbreviation" variant="link"
                  @click="handleOpenAiForm('edit', data, props.data)"></Button>
              </template>
            </Column>
            <Column field="common_name" header="Common Name"></Column>
            <Column field="common_name_cn" header="Common Name(CN)"></Column>
            <Column field="design_code" header="Design Code"></Column>

            <Column header="Action">
              <template #body="props">
                <Button icon=" pi pi-trash" rounded variant="outlined"
                  @click="handleDeletePorductAi(data.id, props.data.id)"></Button>
              </template>
            </Column>

            <template #empty>
              <p class="text-center text-primary">No Related Ai Found!</p>
            </template>
          </DataTable>


        </div>

      </template>

      <template #empty>
        <p class="text-center text-primary">No Products Found!</p>
      </template>


    </DataTable>

    <ConfirmDialog></ConfirmDialog>

    <!-- #region Product Form -->
    <ProductForm v-if="showProductForm" :initialFormData="initialProductFormData" @close="handleCloseProductForm"
      @refresh="handleRefreshProduct" />
    <!-- #endregion Product Form -->

    <!-- #region AI Form -->
    <AiForm v-if="showAiForm" :initialFormData="initialAiFormData" @close="handleCloseAiForm"
      @refresh="handleRefreshAi">
    </AiForm>
    <!-- #endregion AI Form -->


  </div>
</template>

<script setup>
  import { onMounted, inject, ref, useTemplateRef, toRaw } from "vue";

  import { useToast } from "primevue/usetoast";
  import { useConfirm } from "primevue/useconfirm";
  import { FilterMatchMode } from "@primevue/core";
  import ProductForm from "./ProductForm.vue";
  import AiForm from "./AiForm.vue";

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


  // #region Product Form

  const showProductForm = ref(false);
  const initialProductFormData = ref();
  function handleOpenProductForm(mode, data = null) {
    if (mode === 'new') {
      initialProductFormData.value = {};
    } else if (mode === 'edit') {
      initialProductFormData.value = data;
    }
    showProductForm.value = true;
  }


  function handleCloseProductForm() {
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

  async function handleRefreshProduct(product_id, newData) {
    const index = products.value.findIndex((product) => product.id === product_id);
    if (index === -1) {
      products.value.push(await Api.get(`/products/${product_id}`));
    } else {
      products.value[index] = await Api.get(`/products/${product_id}`);
    }
    products.value[index] = await Api.get(`/products/${product_id}`);


  }

  async function onRowExpand(event) {
    event.data.ais = await Api.get(`/products/${event.data.id}/ais`);
  }


  // #endregion

  const initialAiFormData = ref();
  const showAiForm = ref(false);
  const selectedAi = ref();

  function handleOpenAiForm(mode, product, data = null) {
    if (mode === 'new') {
      initialAiFormData.value = { product_id: product.id, product_internal_name: product.internal_name };
    } else if (mode === 'edit') {

      initialAiFormData.value = data;
      initialAiFormData.value.product_internal_name = product.internal_name;
    }
    showAiForm.value = true;
  }

  function handleCloseAiForm() {
    showAiForm.value = false;
  }

  async function handleRefreshAi(product_id, newData) {

    const p_index = products.value.findIndex((product) => product.id === product_id);
    const ai_index = products.value[p_index].ais?.findIndex((ai) => ai.id === newData.id);

    if (ai_index === undefined) {
      products.value[p_index].ais = [newData];
    } else if (ai_index === -1) {
      products.value[p_index].ais.push(newData);
    } else {
      products.value[p_index].ais[ai_index] = newData;
    }
  }


  function handleDeletePorductAi(product_id, ai_id) {
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

        await Api.delete(`/products/${product_id}/ais/${ai_id}`);
        //refresh ais
        const p_index = products.value.findIndex((product) => product.id === product_id);
        const ai_index = products.value[p_index].ais.findIndex((ai) => ai.id === ai_id);
        products.value[p_index].ais.splice(ai_index, 1);

      },
      reject: null,
    });
  }
</script>





<style module></style>
