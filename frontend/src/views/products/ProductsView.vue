<template>
  <div>
    
    <DataTable
      ref="tableRef"
      :value="products"
      v-model:selection="selectedProducts"
      scrollable
      selectionMode="single"
      dataKey="id"
      paginator
      v-model:filters="filters"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      :globalFilterFields="globalFilterFields"
      tableStyle="min-width: 50rem"
      pt:header="px-0"
    >
      <template #header>
        <Toolbar pt:start="gap-2">
          <template #start>
            <Button icon="pi pi-plus" label="New" @click="handleNew" severity="secondary" />
            <Button icon="pi pi-trash" label="Delete" @click="handleDelete" severity="secondary" />
          </template>

          <template #center>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <InputText placeholder="Search" v-model="filters['global'].value" />
            </IconField>
          </template>

          <template #end>
            <SplitButton
              severity="secondary"
              label="Export"
              icon="pi pi-download"
              @click="handleExport"
              :model="splitBtnItems"
            >
            </SplitButton>
          </template>
        </Toolbar>
      </template>

      <!-- <Column selectionMode="multiple" headerStyle="width: 3rem"></Column> -->
      <Column field="internal_name" header="Internal Name" frozen>
        <template #body="{ data }">
          <Button
            :label="data.internal_name"
            variant="link"
            @click="handleEdit(data)"
          ></Button> </template
      ></Column>
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
            data.is_three_new ? 'Yes' : 'No'
          }}</span>
        </template>
      </Column>

      <template #empty>
        <p class="text-center text-primary">No Products Found!</p>
      </template>
    </DataTable>
    <ConfirmDialog></ConfirmDialog>

    <Dialog v-model:visible="showForm" :style="{ width: '900px' }" :modal="true" maximizable>
      <template #header>
        <p class="font-bold text-lg">{{initialFormData.id?"Edit Product":"Create Product"}}</p>
        <div class="flex gap-4">
          <Button icon="pi pi-save" label="Save" @click="handleSave" v-show="showForm" />
          <!-- <Button icon="pi pi-replay" label="Reset" @click="handleReset" v-show="showForm" /> -->
          <Button icon="pi pi-times" label="Cancel" @click="handleCancel" v-show="showForm" />
        </div>
      </template>
      <Form
        :resolver="resolver"
        :initialValues="initialFormData"
        :validateOnValueUpdate="true"
        ref="formRef"
        class="flex flex-col gap-4 overflow-auto p-4 mb-32"
      >
        <FormField v-slot="$field" name="internal_name" class="form-field">
          <label for="internal_name" class="required-mark">Internal Name</label>
          <InputText id="internal_name"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="lead_ai" class="form-field">
          <label for="lead_ai" class="required-mark">Lead AI</label>
          <InputText id="lead_ai"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="stage" class="form-field">
          <label for="stage" class="required-mark">Stage</label>
          <Select inputId="stage" :options="enums.StageEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="a_number" class="form-field">
          <label for="a_number">A Number</label>
          <InputText id="a_number"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="product_name" class="form-field">
          <label for="product_name">Product Name</label>
          <InputText id="product_name"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="product_name_cn" class="form-field">
          <label for="product_name_cn">Product Name (CN)</label>
          <InputText id="product_name_cn"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="trade_name" class="form-field">
          <label for="trade_name">Trade Name</label>
          <InputText id="trade_name"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="product_origin" class="form-field">
          <label for="product_origin">Product Origin</label>
          <InputText id="product_origin"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="is_three_new" class="form-field">
          <label for="is_three_new">Three-New</label>
          <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
            <RadioButton inputId="is_three_new_true" :value="true" />
            <label for="is_three_new_true">Yes</label>

            <RadioButton inputId="is_three_new_false" :value="false" />
            <label for="is_three_new_false">No</label>
          </RadioButtonGroup>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
      </Form>
    </Dialog>
  </div>
</template>

<script setup>
  import { onMounted, inject, ref, useTemplateRef, toRaw } from 'vue'
  import { Form, FormField } from '@primevue/forms'
  import { useToast } from 'primevue/usetoast'
  import { useConfirm } from 'primevue/useconfirm'
  import { FilterMatchMode } from '@primevue/core'

  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'

  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
  const toast = useToast()
  const confirm = useConfirm()
  const $axios = inject('$axios')
  const tableRef = useTemplateRef('tableRef')
  const formRef = useTemplateRef('formRef')

  const products = ref([])
  const selectedProducts = ref([])
  const showForm = ref(false)
  let initialFormData = {}

  const splitBtnItems = [{ label: 'Import', icon: 'pi pi-upload', command: handleImport }]
  //yup resolver: (values,[names])=>{}->errors:obj
  const resolver = yupResolver(
    yup.object().shape({
      internal_name: yup.string().required(),
      lead_ai: yup.string().required(),
      stage: yup.string().required()
    })
  )

  const globalFilterFields = ['internal_name','lead_ai', 'stage', 'a_number', 'product_name_cn','trade_name']

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
    // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
  })

  onMounted(async () => {
    try {
      const response = await $axios.get('/products')
      products.value = response.data
    } catch (err) {
      console.error(err)
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Faild to get all products',
        life: 3000
      })
    }
  })

  function handleImport() {
    toast.add({
      severity: 'warn',
      summary: 'Warn Message',
      detail: 'To be implemented',
      life: 3000
    })
  }

  function handleExport() {
    tableRef.value.exportCSV()
  }

  function handleEdit(row) {
    initialFormData = toRaw(row)
    showForm.value = true
  }

  function handleNew() {
    //save data to database
    initialFormData = {}
    showForm.value = true
  }
  async function handleDelete() {
    if (selectedProducts.value.length === 0) {
      toast.add({
        severity: 'warn',
        summary: 'Warning!',
        detail: 'Please select rows first!',
        life: 2000
      })
      return
    }
    confirm.require({
      position: 'top',
      message: 'Are you sure you want delete?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      rejectProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true
      },
      acceptProps: {
        label: 'Confirm'
      },
      accept: async () => {
        try {
          let response
          response = await $axios.delete('/products', {
            data: selectedProducts.value.map((obj) => obj.id) //for mutiple selection
          })
          //refresh products
          response = await $axios.get('/products')
          products.value = response.data
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: response.data.message,
            life: 3000
          })
        } catch (err) {
          toast.add({ severity: 'error', summary: 'Error', detail: err.message })
        }
        selectedProducts.value = []
      },
      reject: () => {}
    })
  }

  async function handleSave() {
    //form filed values are matained by primevue Form, no need to bind to a ref or reactive

    const { values, errors } = await formRef.value.validate()

    if (Object.keys(errors).length !== 0) {
      return
    }

    // distinguish add and patch through formData.id (Undefined == add)
    try {
      let response
      if (initialFormData.id) {
        // modify current porduct
        let dirty_data = {}
        Object.entries(formRef.value.states).forEach(([key, value]) => {
          if (value.dirty) {
            dirty_data[key] = value.value
          }
        })

        if (Object.keys(dirty_data).length === 0) {
          toast.add({
          severity: 'warn',
          summary: 'Warning',
          detail: "No changes to current data",
          life: 3000
        })
          return
        }
        response = await $axios.patch(`/products/${ initialFormData.id}`, dirty_data)
        
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: response.data.message,
          life: 3000
        })
      } else {
        // add new product

        response = await $axios.post('/products', values)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: response.data.message,
          life: 3000
        })
      }

      showForm.value = false

      //refresh data
      response = await $axios.get('/products')
      products.value = response.data
    } catch (err) {
      console.log(err)
      toast.add({ severity: 'error', summary: 'Error', detail: 'Add product failed!' })
    }
  }

  // async function handleReset() {
  //   await formRef.value.reset() // reset validation status
  // }
  function handleCancel() {
    showForm.value = false
  }
</script>

<style module></style>
