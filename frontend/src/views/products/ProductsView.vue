<template>
  <div class="flex flex-row gap-4">
    <DataTable ref="tableRef" :value="products" v-model:selection="selectedProducts" v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand" scrollable scrollHeight="400px" selectionMode="single" dataKey="id" paginator
      v-model:filters="filters" filterDisplay="menu" :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]"
      :globalFilterFields="globalFilterFields" class="min-w-[50rem] w-full" pt:header="px-0">
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
            <Button :icon="'pi pi-filter-fill'" rounded outlined :severity="btnSeverity"
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
          <InputText v-model="filterModel.value" @input="filterCallback()" fluid />
        </template>

      </Column>
      <Column field="lead_ai" header="Lead AI">
        <template #filter="{ filterModel, filterCallback }">
          <InputText v-model="filterModel.value" @input="filterCallback()" fluid />
        </template>
      </Column>
      <Column field="stage" header="Stage">
        <template #body="{ data }">
          <Tag :severity="data.stage >= 'stage_C' ? 'success' : 'warn'" :value="data.stage"></Tag>
        </template>

        <template #filter="{ filterModel, filterCallback }">
          <MultiSelect inputId="stage" :options="enums.StageEnum" v-model="filterModel.value" showClear display="chip"
            pt:header="hidden" @change="filterCallback()" />
        </template>

      </Column>
      <Column field="a_number" header="A Number"></Column>
      <Column field="product_name" header="Product Name"></Column>
      <Column field="product_name_cn" header="Product Name (CN)"></Column>
      <Column field="trade_name" header="Trade Name"></Column>
      <Column field="product_origin" header="Product Origin"></Column>
      
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
    <div v-if="showFloatFilter"
      class="w-80 py-4 pl-4 border border-surface-200 rounded bg-surface-100 flex flex-col h-full">
      <div class="flex justify-between pr-4">
        <span class="font-bold text-xl mb-4">Filters</span>
        <Button icon="pi pi-times" class="p-button-rounded p-button-secondary" @click="handleShowFilter"></Button>
      </div>
      <div class="flex-1 overflow-y-auto flex flex-col gap-4 mb-4 pr-4">
        <div class="flex flex-col">
          <label for="internal_name">Internal Name</label>
          <InputText name="internal_name" id="internal_name" v-model="filters.internal_name.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="trade_name">Trade Name</label>
          <InputText name="trade_name" id="trade_name" v-model="filters.trade_name.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="lead_ai">Lead AI</label>
          <InputText name="lead_ai" id="lead_ai" v-model="filters.lead_ai.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="stage">Stage</label>
          <MultiSelect name="stage" inputId="stage" :options="enums.StageEnum" v-model="filters.stage.value" showClear
            display="chip" pt:header="hidden" />

        </div>
        <div class="flex flex-col">
          <label for="a_number">A number</label>
          <InputText name="a_number" id="a_number" v-model="filters.a_number.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="product_name">Product Name</label>
          <InputText name="product_name" id="product_name" v-model="filters.product_name.value"></InputText>
        </div>
        <div class="flex flex-col">
          <label for="product_name_cn">Product Name (CN)</label>
          <InputText name="product_name_cn" id="product_name_cn" v-model="filters.product_name_cn.value"></InputText>
        </div>
      </div>
    </div>
    <!-- #endregion Filter -->

  </div>
</template>

<script setup>
  import { onMounted, inject, ref, useTemplateRef, toRaw, computed } from "vue";

  import { useToast } from "primevue/usetoast";
  import { useConfirm } from "primevue/useconfirm";
  import { FilterMatchMode } from "@primevue/core";
  import ProductForm from "./ProductForm.vue";
  import AiForm from "./AiForm.vue";

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  const toast = useToast();
  const confirm = useConfirm();
  import useApi from "@/composables/useApi"; import { MultiSelect } from "primevue";
  ;
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
    internal_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    lead_ai: { value: null, matchMode: FilterMatchMode.CONTAINS },
    stage: { value: null, matchMode: FilterMatchMode.IN },
    a_number: { value: null, matchMode: FilterMatchMode.CONTAINS },
    trade_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    product_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    product_name_cn: { value: null, matchMode: FilterMatchMode.CONTAINS },
    
  });


  const showFloatFilter = ref(true);
  function handleShowFilter() {
    showFloatFilter.value = !showFloatFilter.value;
  }

  const btnSeverity = computed(() => {
    let hasFilter=Object.values(filters.value).some((filter) => {
      if (filter.value && (Array.isArray(filter.value) ? filter.value.length > 0 : filter.value.toString().trim())) {
        return true;
      }
    });
    return hasFilter ? "primary" : "secondary";
  });
  // endregion filter

</script>





<style module></style>
