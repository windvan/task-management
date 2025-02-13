<template>
  <Dialog v-model:visible="visible" :style="{ width: '900px' }" :modal="true" maximizable>
    <template #header>
      <p class="font-bold text-lg">Edit Task</p>
      <div class="flex gap-4">
        <Button icon="pi pi-save" label="Save" type="submit" form="editTaskForm" />
        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form
      v-if="_initialFormData"
      :resolver
      :initialValues="_initialFormData"
      @submit="handleSave"
      pt:root:id="editTaskForm"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32"
    >
      <!-- project field:project_id -->
      <FormField v-slot="$field" name="project" class="form-field">
        <label for="project" class="required-mark">Project</label>
        <Select
          inputId="project"
          :options="selectOptions?.projectOptions"
          optionLabel="project_name"
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- task group field -->
      <FormField v-slot="$field" name="tags" class="form-field">
        <label for="tags">Tags</label>
        <InputText id="tags"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- task category field -->
      <FormField v-slot="$field" name="task_category" class="form-field">
        <label for="task_category">Task Category</label>
        <Select inputId="task_category" :options="taskCategoryOptions" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- task name field -->
      <FormField v-slot="$field" name="task_name" class="form-field">
        <label for="task_name">Task Name</label>
        <InputText id="task_name" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- task owner:task_owner_id -->
      <FormField v-slot="$field" name="task_owner" class="form-field">
        <label for="task_owner">Task Owner</label>
        <Select :options="selectOptions?.userOptions" option-label="name"></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- task status -->
      <FormField v-slot="$field" name="task_status" class="form-field">
        <label for="task_status">Task Status</label>
        <Select inputId="task_status" :options="enums?.TaskStatusEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- start_year -->
      <FormField v-slot="$field" name="start_year" class="form-field">
        <label for="start_year">Start Year</label>
        <DatePicker
          inputId="start_year"
          name="start_year"
          view="year"
          date-format="yy"
          showIcon
          iconDisplay="input"
          showButtonBar
          :min-date="new Date()"
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- expected_delivery_date -->
      <FormField v-slot="$field" name="expected_delivery_date" class="form-field">
        <label for="expected_delivery_date">Expected Delivery Date</label>
        <DatePicker
          inputId="expected_delivery_date"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
          :min-date="new Date()"
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- pi_number -->
      <FormField v-slot="$field" name="pi_number" class="form-field">
        <label for="pi_number">PI Number</label>
        <InputText id="pi_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- tk_number -->
      <FormField v-slot="$field" name="tk_number" class="form-field">
        <label for="tk_number">TK Number</label>
        <InputText id="tk_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- cost_center -->
      <FormField v-slot="$field" name="cost_center" class="form-field">
        <label for="cost_center">Cost Center</label>
        <Select inputId="cost_center" :options="enums?.CostCenterEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- tox_gov_approved -->
      <FormField v-slot="$field" name="tox_gov_approved" class="form-field">
        <label for="tox_gov_approved">Tox Gov. Approved</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="tox_gov_approved_true" :value="true" />
          <label for="tox_gov_approved_true">Yes</label>

          <RadioButton inputId="tox_gov_approved_false" :value="false" />
          <label for="tox_gov_approved_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- ecotox_gov_approved -->
      <FormField v-slot="$field" name="ecotox_gov_approved" class="form-field">
        <label for="ecotox_gov_approved">Ecotox Gov. Approved</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="ecotox_gov_approved_true" :value="true" />
          <label for="ecotox_gov_approved_true">Yes</label>
          <RadioButton inputId="ecotox_gov_approved_false" :value="false" />
          <label for="ecotox_gov_approved_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- budget_confirmed -->
      <FormField v-slot="$field" name="budget_confirmed" class="form-field">
        <label for="budget_confirmed">Budget Confirmed</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="budget_confirmed_true" :value="true" />
          <label for="budget_confirmed_true">Yes</label>
          <RadioButton inputId="budget_confirmed_false" :value="false" />
          <label for="budget_confirmed_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- doc_link -->
      <FormField v-slot="$field" name="doc_link" class="form-field">
        <label for="doc_link">Document Link</label>
        <InputText id="doc_link"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- task_confirmed -->
      <FormField v-slot="$field" name="task_confirmed" class="form-field">
        <label for="task_confirmed">Task Confirmed</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="task_confirmed_true" :value="true" />
          <label for="task_confirmed_true">Yes</label>
          <RadioButton inputId="task_confirmed_false" :value="false" />
          <label for="task_confirmed_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- po_placed -->
      <FormField v-slot="$field" name="po_placed" class="form-field">
        <label for="po_placed">PO Placed</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="po_placed_true" :value="true" />
          <label for="po_placed_true">Yes</label>
          <RadioButton inputId="po_placed_false" :value="false" />
          <label for="po_placed_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- contract_signed -->
      <FormField v-slot="$field" name="contract_signed" class="form-field">
        <label for="contract_signed">Contract Signed</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="contract_signed_true" :value="true" />
          <label for="contract_signed_true">Yes</label>
          <RadioButton inputId="contract_signed_false" :value="false" />
          <label for="contract_signed_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- payment_method -->
      <FormField v-slot="$field" name="payment_method" class="form-field">
        <label for="payment_method">Payment Method</label>
        <Select inputId="payment_method" :options="enums?.PaymentMethodEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- payment_status -->
      <FormField v-slot="$field" name="payment_status" class="form-field">
        <label for="payment_status">Payment Status</label>
        <Select inputId="payment_status" :options="enums?.PaymentStatusEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- vv_doc_uploaded -->
      <FormField v-slot="$field" name="vv_doc_uploaded" class="form-field">
        <label for="vv_doc_uploaded">VV Doc Uploaded</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="vv_doc_uploaded_true" :value="true" />
          <label for="vv_doc_uploaded_true">Yes</label>
          <RadioButton inputId="vv_doc_uploaded_false" :value="false" />
          <label for="vv_doc_uploaded_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <!-- vv_doc_number -->
      <FormField v-slot="$field" name="vv_doc_number" class="form-field">
        <label for="vv_doc_number">Veeva Document Number</label>
        <InputText id="vv_doc_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- planned_start -->
      <FormField v-slot="$field" name="planned_start" class="form-field">
        <label for="planned_start">Planned Start</label>
        <DatePicker
          inputId="planned_start"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- expected_finish -->
      <FormField v-slot="$field" name="expected_finish" class="form-field">
        <label for="expected_finish">Expected Finish</label>
        <DatePicker
          inputId="expected_finish"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- actual_start -->
      <FormField v-slot="$field" name="actual_start" class="form-field">
        <label for="actual_start">Actual Start</label>
        <DatePicker
          inputId="actual_start"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- actual_finish -->
      <FormField v-slot="$field" name="actual_finish" class="form-field">
        <label for="actual_finish">Actual Finish</label>
        <DatePicker
          inputId="actual_finish"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- delivery_date -->
      <FormField v-slot="$field" name="delivery_date" class="form-field">
        <label for="delivery_date">Delivery Date</label>
        <DatePicker
          inputId="delivery_date"
          date-format="yy-mm-dd"
          showIcon
          iconDisplay="input"
          showButtonBar
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- stuff_days -->
      <FormField v-slot="$field" name="stuff_days" class="form-field">
        <label for="stuff_days">Stuff Days</label>
        <InputNumber id="stuff_days" :min-fraction-digits="0" :max-fraction-digits="1" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- task_progress -->
      <FormField v-slot="$field" name="task_progress" class="form-field">
        <label for="task_progress">Task Progress</label>
        <Select inputId="task_progress" :options="enums?.TaskProgressEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- cro_id -->
      <FormField v-slot="$field" name="cro" class="form-field">
        <label for="cro">CRO Name</label>
        <Select :options="selectOptions?.croOptions" option-label="cro_name"></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- sample_id -->
      <FormField v-slot="$field" name="sample" class="form-field">
        <label for="sample_id">Sample Name</label>
        <Select :options="selectOptions?.sampleOptions" option-label="sample_name"></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- study_notified -->
      <FormField v-slot="$field" name="study_notified" class="form-field">
        <label for="study_notified">Study Notified</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="study_notified_true" :value="true" />
          <label for="study_notified_true">Yes</label>
          <RadioButton inputId="study_notified_false" :value="false" />
          <label for="study_notified_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- estimated_cost -->
      <FormField v-slot="$field" name="estimated_cost" class="form-field">
        <label for="estimated_cost">Estimated Cost</label>
        <InputNumber id="estimated_cost" mode="currency" currency="CNY" locale="zh-CN" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- actual_cost -->
      <FormField v-slot="$field" name="actual_cost" class="form-field">
        <label for="actual_cost">Actual Cost</label>
        <InputNumber id="actual_cost" mode="currency" currency="CNY" locale="zh-CN" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- analytes -->
      <FormField v-slot="$field" name="analytes" class="form-field">
        <label for="analytes">Analytes</label>
        <InputText id="analytes"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- key_results -->
      <FormField v-slot="$field" name="key_results" class="form-field">
        <label for="key_results">Key Results</label>
        <InputText id="key_results"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- guidelines -->
      <FormField v-slot="$field" name="guidelines" class="form-field">
        <label for="guidelines">Guidelines</label>
        <InputText id="guidelines"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- test_item_data_sheet -->
      <FormField v-slot="$field" name="test_item_data_sheet" class="form-field">
        <label for="test_item_data_sheet">Test Item Data Sheet</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="test_item_data_sheet_true" :value="true" />
          <label for="test_item_data_sheet_true">Yes</label>
          <RadioButton inputId="test_item_data_sheet_false" :value="false" />
          <label for="test_item_data_sheet_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- ssd_finished -->
      <FormField v-slot="$field" name="ssd_finished" class="form-field">
        <label for="ssd_finished">SSD Finished</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="ssd_finished_true" :value="true" />
          <label for="ssd_finished_true">Yes</label>
          <RadioButton inputId="ssd_finished_false" :value="false" />
          <label for="ssd_finished_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- sed_uploaded -->
      <FormField v-slot="$field" name="sed_uploaded" class="form-field">
        <label for="sed_uploaded">SED Uploaded</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="sed_uploaded_true" :value="true" />
          <label for="sed_uploaded_true">Yes</label>
          <RadioButton inputId="sed_uploaded_false" :value="false" />
          <label for="sed_uploaded_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- global_study_manager -->
      <FormField v-slot="$field" name="global_study_manager" class="form-field">
        <label for="global_study_manager">Global Study Manager</label>
        <InputText id="global_study_manager"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- global_study_manager_email -->
      <FormField v-slot="$field" name="global_study_manager_email" class="form-field">
        <label for="global_study_manager_email">Global Study Manager Email</label>
        <InputText id="global_study_manager_email" type="email"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- cro_study_director -->
      <FormField v-slot="$field" name="cro_study_director" class="form-field">
        <label for="cro_study_director">CRO Study Director</label>
        <InputText id="cro_study_director"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>
    </Form>
  </Dialog>
</template>

<script setup>
  import { inject, onMounted, ref } from 'vue'
  import { useToast } from 'primevue'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'
  import DatePicker from 'primevue/datepicker'


  import { dateToStr } from '@/composables/dateTools'
  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}

  const taskCategoryOptions = ref()

  const emit = defineEmits(['refresh'])

  const toast = useToast()
  const visible = defineModel('visible')
  const $axios = inject('$axios')
  let selectOptions
  const _initialFormData = ref()
  const { initialFormData } = defineProps({
    initialFormData: {
      type: Object,
      required: true
    }
  })

  onMounted(async () => {
    try {
      let response = await $axios.get('/tasks/select-options')
      selectOptions = response.data
    } catch (err) {
      console.log('get select options failed on tasks edit view', err)
    }

    taskCategoryOptions.value = [
      ...new Set(selectOptions?.taskLibrary.map((item) => item['task_category']))
    ]

    let processedFormData = { ...initialFormData }

    processedFormData.project = selectOptions?.projectOptions.find(
      (proj) => proj.id === initialFormData.project_id
    )
    processedFormData.task_owner = selectOptions?.userOptions.find(
      (user) => user.id === initialFormData.task_owner_id
    )
    processedFormData.start_year = new Date(initialFormData.start_year, 0, 1)
    processedFormData.expected_delivery_date = new Date(initialFormData.expected_delivery_date)

    _initialFormData.value = processedFormData
  })

  const resolver = yupResolver(
    yup.object().shape({
      project: yup.mixed().required(),
      tasks: yup.mixed().required(),
      tags: yup
        .string()
        .test(
          'is-tag-format',
          'Value must be one or more #string# separated by spaces, string length <20',
          (value) => {
            const pattern = /^(#\w{1,20}#\s*)+$/
            return pattern.test(value.trim())
          }
        ),
      task_category: yup.string().required(),
      task_name: yup.string().required(),
      task_status: yup.string().required(),
      start_year: yup.date().required('Start year is required in the table'),
      expected_delivery_date: yup
        .date()
        .required('Expected Delivery Date is required in the table'),
      task_owner: yup.mixed().required('Task Owner is required in the table')
    })
  )

  function handleCancel() {
    visible.value = false
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'discard changes successfully',
      life: 2000
    })
  }

  async function handleSave(e) {
    if (!e.valid) return

    console.log(e.states)
    let updatedFields = {}
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        if (state.value instanceof Date) {
          // for date fields
          updatedFields[field] =dateToStr(state.value)
            
        } else if (state.value && typeof state.value === 'object') {
          // for relational fields
          updatedFields[field + '_id'] = state.value.id
        } else {
          // for string and select field
          updatedFields[field] = state.value
        }
      }
    })
    console.log(updatedFields)
    // update task
    try {
      await $axios.patch(`/tasks/${initialFormData.id}`, updatedFields)
      toast.add({
        severity: 'success',
        summary: 'Edit task successfully',
        life: 3000
      })
      visible.value = false
      emit('refresh')
    } catch (err) {
      console.error(err)
    }
  }
</script>
