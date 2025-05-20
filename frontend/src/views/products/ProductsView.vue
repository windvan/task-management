<template>
  <div class="flex flex-row gap-4">
    <DataTable ref="tableRef" :value="products" v-model:selection="selectedProducts" v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand" scrollable selectionMode="single" dataKey="id" paginator v-model:filters="filters"
      filterDisplay="menu" :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" :globalFilterFields="globalFilterFields"
      tableStyle="min-width: 50rem" pt:header="px-0">
      <template #header>
        <Toolbar pt:start="gap-2" pt:end="gap-4">
          <template #start>
            <Button icon="pi pi-plus" label="New" @click="handleOpenProductForm('new')" severity="secondary" />

          </template>

          <template #center>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <!-- , dt: { color: '{gray.900}', background: '{gray.100}', maxWidth: '30rem', shadow:'none'}  -->
              <InputText title="Search by Product/Trade Name, AI, Stage, A Number" placeholder="Search"
                v-model="filters['global'].value" />
            </IconField>
          </template>

          <template #end>
            <Button :icon="'pi pi-filter' + (showFloatFilter ? '-fill' : '')" rounded severity="secondary"
              @click="handleShowFilter"></Button>
            <Button severity="secondary" icon="pi pi-download" label="Export" @click="handleExport"></Button>
            <!-- <SplitButton severity=" secondary" label="Export" icon="pi pi-download" @click="handleExport"
              :model="splitBtnItems">
              </SplitButton> -->
          </template>
        </Toolbar>
      </template>


      <Column expander style="width: 3rem"></Column>
      <Column field="internal_name" header="Internal Name" class="text-nowrap px-0" frozen>
        <template #body="{ data }">
          <Button :label="data.internal_name" variant="link" class="px-0"
            @click="handleOpenProductForm('edit', data)"></Button>
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Search by Internal Name"
            class="w-full" />
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



    <!-- #region Product Form -->
    <ProductForm v-if="showProductForm" :initialFormData="initialProductFormData" @close="handleCloseProductForm"
      @refresh="handleRefreshProduct" />
    <!-- #endregion Product Form -->

    <!-- #region AI Form -->

    <AiForm v-if="showAiForm" :initialFormData="initialAiFormData" @close="handleCloseAiForm"
      @refresh="handleRefreshAi">
    </AiForm>
    <!-- #endregion AI Form -->

    <!-- #region Filter -->
    <div v-if="showFloatFilter" class="w-50">
      <form @submit="handleApplyFilters">
        <div class="flex flex-col">
          <label for="internal_name">Internal Name</label>
          <InputText name="internal_name" id="internal_name" v-model="filters.internal_name.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="lead_ai">lead_ai</label>
          <InputText name="lead_ai" id="lead_ai" v-model="filters.lead_ai.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="stage">stage</label>
          <Select name="stage" inputId="stage" :options="enums.StageEnum" v-model="filters.stage.value" />
        </div>


        <div class="flex flex-row gap-4 justify-center mt-4">
          <Button type="submit">Apply</Button>
          <Button>Cancel</Button>
          <Button>Reset</Button>
        </div>

      </form>
    </div>
    <!-- #endregion Filter -->

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
  import useApi from "@/composables/useApi";;
  const Api = inject("Api")
  const tableRef = useTemplateRef("tableRef");

  const products = ref([]);
  const selectedProducts = ref([]);
  const expandedRows = ref([]);



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

  async function handleRefreshProduct(newData) {
    const index = products.value.findIndex((product) => product.id === newData.id);
    if (index === -1) {
      // products.value.push(await Api.get(`/products/${product_id}`));
      products.value.push(newData);
    } else {
      // products.value[index] = await Api.get(`/products/${product_id}`);
      products.value.splice(index, 1, newData);
    }
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


  // region filter
  const globalFilterFields = [
    "internal_name",
    "lead_ai",
    "stage",
    "a_number",
    "product_name",
    "product_name_cn",
    "trade_name",
  ];

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    internal_name: { value: 'TYM', matchMode: FilterMatchMode.STARTS_WITH },
    lead_ai: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    stage: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    a_number: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    trade_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    product_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    product_name_cn: { value: null, matchMode: FilterMatchMode.STARTS_WITH },

  });


  const showFloatFilter = ref(false);
  function handleShowFilter() {
    showFloatFilter.value = !showFloatFilter.value;
  }
  function handleApplyFilters(event) {

    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    for (const [key, value] of formData.entries()) {
      filters.value[key].value = value;
    }
  }
  // endregion filter

</script>





<style module></style>
