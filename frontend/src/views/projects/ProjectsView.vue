<template>
  <div>
    <DataTable ref="outerTableRef" :value="projects" v-model:selection="selectedProject"
      v-model:expandedRows="expandedRows" @rowExpand="onRowExpand" scrollable selectionMode="single" dataKey="id"
      paginator v-model:filters="tableFilters" :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]"
      :globalFilterFields="globalTableFilterFields" tableStyle="min-width: 50rem" pt:header="px-0">
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
              <InputText placeholder="Search" v-model="tableFilters['global'].value" />
            </IconField>
          </template>

          <template #end>
            <SplitButton severity="secondary" label="Export" icon="pi pi-download" @click="handleExport"
              :model="splitBtnItems">
            </SplitButton>
          </template>
        </Toolbar>
      </template>

      <Column expander class="w-12" frozen />
      <!-- <Column selectionMode="multiple" class="w-12" frozen></Column> -->
      <Column field="project_name" header="Project Name" frozen>
        <template #body="{ data }">
          <Button :label="data.project_name" variant="link" @click="handleEdit(data)" class="px-0 text-left"></Button>
        </template>
      </Column>
      <Column field="product_internal_name" header="Product"></Column>
      <!-- product_id  -->
      <Column field="product_stage" header="Product Stage">
        <template #body="{ data }">
          <Tag :severity="data.product_stage >= 'stage_C' ? 'success' : 'warn'" :value="data.product_stage"></Tag>
        </template>
      </Column>

      <Column field="project_status" header="Project Status">
        <template #body="{ data }">
          <Tag :severity="getStatusSeverity(data.project_status)" :value="data.project_status"></Tag>
        </template>
      </Column>
      <Column field="indication" header="Indication">
        <template #body="{ data }">
          <Tag severity="info" :value="data.indication"></Tag>
        </template>
      </Column>
      <Column field="registration_type" header="Registration Type"></Column>
      <Column field="reg_entity" header="Reg Entity"></Column>
      <Column field="notification_entrance" header="Notification No."></Column>
      <Column field="portfolio_contact_name" header="Portfolio"></Column>
      <!-- portfolio_contact_id  -->
      <Column field="project_manager" header="PM"></Column>
      <Column field="reg_manager" header="RM"></Column>
      <Column field="registration_status" header="Registration Status"></Column>
      <Column field="approved_date" header="Approved Date">
        <template #body="{ data }">
          {{ data.approved_date ? data.approved_date : 'Not Approved Yet' }}
        </template>
      </Column>

      <template #expansion="{ data }">
        <div class="flex gap-4">
          <div class="w-24 flex flex-col items-center p-4">
            <Button icon="pi pi-plus" severity="info" rounded variant="outlined" />
          </div>

          <DataTable :value="data.tasks" dataKey="id" size="large" scrollable>
            <Column field="task_name" header="Task Name"></Column>
            <Column field="task_group" header="Task Group"></Column>
            <Column field="task_category" header="Task Category"></Column>
            <Column field="task_owner_name" header="Task Owner"></Column>
            <Column field="task_status" header="Task Status"></Column>
            <Column field="start_year" header="Start Year"></Column>
            <Column field="expected_delivery_date" header="Expected Delivery Date"></Column>
            <Column field="planned_start" header="Planned_Start"></Column>
            <Column field="expected_finish" header="Expected Finish"></Column>
            <Column field="actual_start" header="Actual Start"></Column>
            <Column field="actual_finish" header="Actual Finish"></Column>

            <template #empty>
              <p class="text-center text-primary">No Related Tasks Found!</p>
            </template>
          </DataTable>
        </div>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Projects Found!</p>
      </template>
    </DataTable>
    <ConfirmDialog></ConfirmDialog>

    <Dialog v-model:visible="showForm" :style="{ width: '900px' }" :modal="true" maximizable>
      <template #header>
        <p class="font-bold text-lg">
          {{ initialFormData.id ? 'Edit Project' : 'Create Project' }}
        </p>
        <div class="flex gap-4">
          <Button icon="pi pi-save" label="Save" @click="handleSave" v-show="showForm" />
          <!-- <Button icon="pi pi-replay" label="Reset" @click="handleReset" v-show="showForm" /> -->
          <Button icon="pi pi-times" label="Cancel" @click="handleCancel" v-show="showForm" />
        </div>
      </template>
      <Form v-slot="$form" :resolver="resolver" :initialValues="initialFormData" :validateOnValueUpdate="true"
        ref="formRef" class="flex flex-col gap-4 overflow-auto p-4 mb-32">
        <FormField v-slot="$field" name="product" class="form-field">
          <label for="product" class="required-mark">Product</label>
          <AutoComplete inputId="product" optionLabel="internal_name" :suggestions="filteredProductOptions"
            @complete="filterProductOptions" completeOnFocus forceSelection dropdown :delay="200"
            placeholder="Type to filter" />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="registration_type" class="form-field">
          <label for="registration_type" class="required-mark">Registration Type</label>
          <Select inputId="registration_type" :options="enums.RegistrationTypeEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="project_name" class="form-field">
          <label for="project_name" class="required-mark">Project Name</label>
          <InputGroup>
            <!-- <InputGroupAddon>{{ [$form.product?.value?.internal_name,$form.registration_type?.value].join("_") }}</InputGroupAddon> -->
            <InputText id="project_name" />
          </InputGroup>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="indication" class="form-field">
          <label for="indication" class="required-mark">Indication</label>
          <Select inputId="indication" :options="enums.IndicationEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="reg_entity" class="form-field">
          <label for="reg_entity">Reg Entity</label>
          <Select inputId="reg_entity" :options="enums.RegEntityEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="project_status" class="form-field">
          <label for="project_status" class="required-mark">Project Status</label>
          <Select inputId="project_status" :options="enums.ProjectStatusEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="portfolio_contact" class="form-field">
          <label for="portfolio_contact" class="required-mark">Portfolio Contact</label>
          <AutoComplete inputId="portfolio_contact" optionLabel="name" :suggestions="filteredUserOptions"
            @complete="filterUserOptions" completeOnFocus forceSelection dropdown :delay="200"
            placeholder="Type to filter" />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="project_manager" class="form-field">
          <label for="project_manager" class="required-mark">Project Manager</label>
          <Select inputId="project_manager" :options="enums.ProjectManagerEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="reg_manager" class="form-field">
          <label for="reg_manager" class="required-mark">Reg Manager</label>
          <AutoComplete inputId="reg_manager" :suggestions="filteredRmOptions" @complete="filterRmOptions"
            completeOnFocus forceSelection dropdown :delay="200" placeholder="Type to filter" />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="notification_entrance" class="form-field">
          <label for="notification_entrance">Notification Entrance</label>
          <InputText id="notification_entrance"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="submission_status" class="form-field">
          <label for="submission_status">Submission Status</label>
          <Select inputId="submission_status" :options="enums.SubmissionStatusEnum" showClear></Select>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="approved_date" class="form-field">
          <label for="approved_date"
            :class="{ 'required-mark': $form?.submission_status?.value === 'Approved' }">Approved
            Date</label>
          <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
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
  import { Select } from 'primevue'

  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
  const toast = useToast()
  const confirm = useConfirm()
  const $axios = inject('$axios')
  const outerTableRef = useTemplateRef('outerTableRef')
  const formRef = useTemplateRef('formRef')

  const projects = ref([])
  const expandedRows = ref([])

  // const projectNamePrefix=ref()
  let selectOptions //all select components options on this page
  const filteredProductOptions = ref([]) // form autocomplete component filter
  const filteredUserOptions = ref([]) // form autocomplete component filter
  const filteredRmOptions = ref([]) // form autocomplete component filter
  const selectedProject = ref()
  const showForm = ref(false)
  let initialFormData

  const splitBtnItems = [{ label: 'Import', icon: 'pi pi-upload', command: handleImport }]
  //yup resolver: (values,[names])=>{}->errors:obj
  const resolver = yupResolver(
    yup.object().shape({
      project_name: yup.string(),
      product: yup.object().required(),
      indication: yup.string().required(),
      portfolio_contact: yup.object().required(),
      project_manager: yup.string().required(),
      reg_manager: yup.string().required(),
      project_status: yup.string().required(),
      registration_type: yup.string().required(),
      submission_status: yup.string().nullable(),
      approved_date: yup.date().when('submission_status', ([submission_status], schema) => {
        return submission_status === 'Approved' ? schema.required() : schema.nullable()
      })
    })
  )

  const globalTableFilterFields = ['project_name', 'product_id']

  const tableFilters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
    // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
  })

  onMounted(async () => {
    try {
      const response = await $axios.get('/projects/')
      projects.value = response.data
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

  function getStatusSeverity(status) {
    switch (status) {
      case 'Idea_Stage':
        return 'secondary'
      case 'Active':
        return 'info'
      case 'Finished':
        return 'success'
      case 'Terminated':
        return 'warn'
      default:
        return 'primary' // 或者其他默认值
    }
  }

  async function onRowExpand(event) {
    // get tasks of current project
    try {
      let response = await $axios.get(`projects/${event.data.id}/tasks`)
      event.data.tasks = response.data
    } catch (err) {
      if (err.status === 401) {
        toast.add({
          severity: 'warn',
          summary: 'Warn Message',
          detail: 'Get related tasks failed!',
          life: 3000
        })
      }
    }
  }

  async function getSelectOptions() {
    try {
      let response = await $axios.get('/projects/select-options')
      selectOptions = response.data
    } catch (err) {
      console.log('get select options failed on projects view', err)
    }
  }
  // watchEffect(async () => {
  //   if (showForm.value) {
  //     try {
  //       const response = await $axios.get('/projects/select-options')
  //       selectOptions = response.data
  //     } catch (err) {
  //       console.log('get select options failed on projects view', err)
  //     }
  //   }
  // })

  // watchEffect(async () => {
  //   projectNamePrefix.value=formRef.value.status.product.value
  // })

  function filterProductOptions(event) {
    if (event.query.trim()) {
      filteredProductOptions.value = selectOptions.productOptions.filter((product) => {
        return product.internal_name.toLowerCase().includes(event.query.toLowerCase())
      })
    } else {
      filteredProductOptions.value = [...selectOptions.productOptions]
    }
  }
  function filterUserOptions(event) {
    if (event.query.trim()) {
      filteredUserOptions.value = selectOptions.userOptions.filter((user) => {
        return user.name.toLowerCase().includes(event.query.toLowerCase())
      })
    } else {
      filteredUserOptions.value = [...selectOptions.userOptions]
    }
  }
  function filterRmOptions(event) {
    if (event.query.trim()) {
      filteredRmOptions.value = enums.RegManagerEnum.filter((rm) => {
        return rm.toLowerCase().includes(event.query.toLowerCase())
      })
    } else {
      filteredRmOptions.value = [...enums.RegManagerEnum]
    }
  }
  function handleImport() {
    toast.add({
      severity: 'warn',
      summary: 'Warn Message',
      detail: 'To be implemented',
      life: 3000
    })
  }

  function handleExport() {
    outerTableRef.value.exportCSV()
  }

  function handleEdit(row) {
    initialFormData = toRaw(row)

    initialFormData.product = {
      id: initialFormData.product_id,
      internal_name: initialFormData.product_internal_name
    }
    initialFormData.portfolio_contact = {
      id: initialFormData.portfolio_contact_id,
      name: initialFormData.portfolio_contact_name
    }
    showForm.value = true
  }

  function handleNew() {
    // set default value on the form
    getSelectOptions()
    initialFormData = {
      submission_status: 'Preparation',
      portfolio_contact: selectOptions?.userOptions.find((user) => user.name === 'Hank Gao')
    }
    showForm.value = true
  }
  async function handleDelete() {
    console.log(selectedProject.value)
    if (!selectedProject.value) {
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
          response = await $axios.delete(`/products/${selectedProject.value.id}`)
          //refresh products
          response = await $axios.get('/products')
          projects.value = response.data
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: response.data.message,
            life: 3000
          })
        } catch (err) {
          toast.add({ severity: 'error', summary: 'Error', detail: err.message })
        }
        selectedProject.value = undefined
      },
      reject: () => { }
    })
  }

  async function handleSave() {
    // form filed values are matained by primevue Form, no need to bind to a ref or reactive
    const { errors } = await formRef.value.validate()
    // if validation error ,return
    if (Object.keys(errors).length !== 0) {
      return
    }
    // get and transform modified data
    let updatedFields = {}
    Object.entries(formRef.value.states).forEach(([field, states]) => {
      if (states.dirty) {
        if (typeof states.value === 'object' && states.value !== null) {
          // for autocomplete field
          updatedFields[field + '_id'] = states.value.id
        } else {
          // for string field
          updatedFields[field] = states.value
        }
      }
    })

    // distinguish add and patch through formData.id (Undefined == add)
    try {
      let response
      if (initialFormData.id) {
        // modify current porduct
        if (Object.keys(updatedFields).length === 0) {
          toast.add({
            severity: 'warn',
            summary: 'Warning',
            detail: 'No changes to current data',
            life: 3000
          })
          return
        }
        response = await $axios.patch(`/projects/${initialFormData.id}`, updatedFields)
        toast.add({ severity: 'success', summary: 'Modify project successfully', life: 3000 })
      } else {
        // add new product
        response = await $axios.post('/projects', updatedFields)
        toast.add({
          severity: 'success',
          summary: 'Add project successfully',
          life: 3000
        })
      }

      showForm.value = false
      //refresh data
      response = await $axios.get('/projects')
      projects.value = response.data
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
