<template>
  <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
    <template #header>
      <p class="font-bold text-lg">
        {{ initialFormData.id ? "Edit Task" : "Create Task" }}
      </p>
      <div class="flex gap-4">
        <Button icon="pi pi-save" label="Save" type="submit" form="taskForm" />
        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form v-slot="$form" :resolver :initialValues="initialFormData" @submit="handleSave" id="taskForm"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32">
      <!-- project -->
      <FormField v-slot="$field" name="project" class="form-field">
        <label for="project" class="required-mark">Project</label>
        <AutoComplete inputId="project" optionLabel="project_name" :suggestions="projectSuggestion"
          @complete="filterProjectSuggestion" forceSelection placeholder="Search" dropdown fluid
          :disabled="Boolean(initialFormData?.id)" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- task_name -->
      <FormField v-slot="$field" name="task_name" class="form-field">
        <label for="task_name" class="required-mark">Task Name</label>
        <AutoComplete inputId="task_name" :suggestions="taskNameSuggestion" forceSelection dropdown placeholder="Search"
          @complete="filterTaskNameSugestoin" fluid :disabled="Boolean(initialFormData?.id)">
        </AutoComplete>

        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- tags -->
      <FormField v-slot="$field" name="tags" class="form-field">
        <label for="tags">Tags</label>
        <InputText id="tags" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- task_status -->
      <FormField v-slot="$field" name="task_status" class="form-field">
        <label for="task_status" class="required-mark">Task Status</label>
        <Select inputId="task_status" :options="enums.TaskStatusEnum" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- start_year -->
      <FormField v-slot="$field" name="start_year" class="form-field">
        <label for="start_year" class="required-mark">Start Year</label>
        <InputText id="start_year" type="number" :min="new Date().getFullYear" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- expected_delivery_date -->
      <FormField v-slot="$field" name="expected_delivery_date" class="form-field">
        <label for="expected_delivery_date" class="required-mark">Expected Delivery Date</label>
        <DatePicker inputId="expected_delivery_date" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar
          :min-date="new Date()" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- task_owner -->
      <FormField v-slot="$field" name="task_owner" class="form-field">
        <label for="task_owner" class="required-mark">Task Owner</label>
        <AutoComplete inputId="task_owner" optionLabel="name" :suggestions="taskOwnerSuggestion"
          @complete="filterTaskOwnerSuggestion" forceSelection placeholder="Search" dropdown fluid dataKey="id" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- pi_number -->
      <FormField v-slot="$field" name="pi_number" class="form-field">
        <label for="pi_number">PI Number</label>
        <InputText id="pi_number" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- tk_number -->
      <FormField v-slot="$field" name="tk_number" class="form-field">
        <label for="tk_number">PI Number</label>
        <InputText id="tk_number" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- cost_center -->
      <FormField v-slot="$field" name="cost_center" class="form-field">
        <label for="cost_center">Cost Center</label>
        <Select inputId="cost_center" :options="enums.CostCenterEnum" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>



      <!-- doc_link -->
      <FormField v-slot="$field" name="doc_link" class="form-field">
        <label for="doc_link">Document Link</label>
        <InputText id="doc_link" />

        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>




      <!-- boolean fields -->
      <div class="border rounded border-surface-200 grid grid-cols-2 p-4 gap-y-3">
        <div class="flex items-center gap-2">
          <CheckBox inputId="tox_gov_approved" name="tox_gov_approved" v-model="booleanFields.tox_gov_approved"
            :binary="true" />
          <label for="tox_gov_approved">Tox Gov. Approved</label>
        </div>

        <div class="flex items-center gap-2">
          <CheckBox inputId="ecotox_gov_approved" name="ecotox_gov_approved" v-model="booleanFields.ecotox_gov_approved"
            :binary="true" />
          <label for="ecotox_gov_approved">Eco-Tox Gov. Approved</label>
        </div>

        <div class="flex items-center gap-2">
          <CheckBox inputId="budget_confirmed" name="budget_confirmed" v-model="booleanFields.budget_confirmed"
            :binary="true" />
          <label for="budget_confirmed">Budget Confirmed</label>
        </div>

        <div class="flex items-center gap-2">
          <CheckBox inputId="po_placed" name="po_placed" v-model="booleanFields.po_placed" :binary="true" />
          <label for="po_placed">po_placed</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="contract_signed" name="contract_signed" v-model="booleanFields.contract_signed"
            :binary="true" />
          <label for="contract_signed">contract_signed</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="vv_doc_uploaded" name="vv_doc_uploaded" v-model="booleanFields.vv_doc_uploaded"
            :binary="true" />
          <label for="vv_doc_uploaded">vv_doc_uploaded</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="task_confirmed" name="task_confirmed" v-model="booleanFields.task_confirmed"
            :binary="true" />
          <label for="task_confirmed">task_confirmed</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="study_notified" name="study_notified" v-model="booleanFields.study_notified"
            :binary="true" />
          <label for="study_notified">study_notified</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="test_item_data_sheet" name="test_item_data_sheet"
            v-model="booleanFields.test_item_data_sheet" :binary="true" />
          <label for="test_item_data_sheet">test_item_data_sheet</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="ssd_finished" name="ssd_finished" v-model="booleanFields.ssd_finished" :binary="true" />
          <label for="ssd_finished">ssd_finished</label>
        </div>
        <div class="flex items-center gap-2">
          <CheckBox inputId="sed_uploaded" name="sed_uploaded" v-model="booleanFields.sed_uploaded" :binary="true" />
          <label for="sed_uploaded">sed_uploaded</label>
        </div>


      </div>



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
      <!-- vv_doc_number -->
      <FormField v-slot="$field" name="vv_doc_number" class="form-field">
        <label for="vv_doc_number">Veeva Document Number</label>
        <InputText id="vv_doc_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>


      <!-- date fields -->

      <div class="grid grid-cols-2 border border-surface-300 rounded p-4">
        <!-- planned_start -->
        <FormField v-slot="$field" name="planned_start">
          <label for="planned_start">Planned Start</label>
          <DatePicker inputId="planned_start" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <!-- expected_finish -->
        <FormField v-slot="$field" name="expected_finish">
          <label for="expected_finish">Expected Finish</label>
          <DatePicker inputId="expected_finish" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <!-- actual_start -->
        <FormField v-slot="$field" name="actual_start">
          <label for="actual_start">Actual Start</label>
          <DatePicker inputId="actual_start" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <!-- actual_finish -->
        <FormField v-slot="$field" name="actual_finish">
          <label for="actual_finish">Actual Finish</label>
          <DatePicker inputId="actual_finish" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <!-- delivery_date -->
        <FormField v-slot="$field" name="delivery_date" class="form-field">
          <label for="delivery_date">Delivery Date</label>
          <DatePicker inputId="delivery_date" date-format="yy-mm-dd" showIcon iconDisplay="input" showButtonBar />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

      </div>


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

      <!-- cro -->
      <FormField v-slot="$field" name="cro" class="form-field">
        <label for="cro">CRO</label>
        <AutoComplete inputId="cro" optionLabel="cro_name" :suggestions="croSuggestion" @complete="filterCroSuggestion"
          forceSelection placeholder="Search" dropdown fluid />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- sample -->
      <FormField v-slot="$field" name="sample" class="form-field">
        <label for="sample">Sample</label>
        <AutoComplete inputId="sample" optionLabel="sample_name" :suggestions="sampleSuggestion"
          @complete="filterSampleSuggestion" forceSelection placeholder="Search" dropdown fluid />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
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
        <Textarea id="key_results"></Textarea>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- guidelines -->
      <FormField v-slot="$field" name="guidelines" class="form-field">
        <label for="guidelines">Guidelines</label>
        <InputText id="guidelines"></InputText>
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
  import { computed, inject, onMounted, ref, useTemplateRef } from "vue";
  import { InputText, useToast } from "primevue";
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";
  import useApi from "@/composables/useApi"; import { FormField } from "@primevue/forms";
  ;
  const Api = inject("Api")

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  const taskLibrary = JSON.parse(localStorage.getItem("cachedTaskLibrary")) || {};
  const taskNameLibrary = taskLibrary.map(task => task.task_name)


  const emit = defineEmits(["close", "refresh"]);
  const visible = ref(true);
  const { initialFormData } = defineProps({ initialFormData: Object });

  const projectSuggestion = ref();
  async function filterProjectSuggestion(event) {
    projectSuggestion.value = await Api.get(
      `/projects/search?query=${event.query}`
    );
  }
  const croSuggestion = ref();
  async function filterCroSuggestion(event) {
    croSuggestion.value = await Api.get(
      `/cros/search?query=${event.query}`
    );
  }
  const sampleSuggestion = ref();
  async function filterSampleSuggestion(event) {
    sampleSuggestion.value = await Api.get(
      `/samples/search?query=${event.query}`
    );
  }

  const taskNameSuggestion = ref();
  async function filterTaskNameSugestoin(event) {
    if (!event.query.trim().length) {
      taskNameSuggestion.value = taskNameLibrary;
    } else {
      const regexp = new RegExp(event.query, "i");
      taskNameSuggestion.value = taskNameLibrary.filter((name) => {
        return regexp.test(name);
      });
    }
  }

  const taskOwnerSuggestion = ref();
  async function filterTaskOwnerSuggestion(event) {
    taskOwnerSuggestion.value = await Api.get(
      `/users/search?query=${event.query}`
    );
  }


  const resolver = yupResolver(
    yup.object().shape({
      project: yup.mixed().required(),
      task_name: yup.string().required('Task name is required').matches(/\S/, 'Task name cannot be only spaces'),
      task_status: yup.string().required(),
      start_year: yup.number('Start year must be a number').required("Start year is required"),
      expected_delivery_date: yup
        .date().min(new Date(), 'Expected Delivery Date must be greater than today')
        .required("Expected Delivery Date is required"),
      task_owner: yup.mixed().test('isObject', 'Please select a value from the suggestion list', value => {
        return typeof value === 'object' && value !== '';
      }),
    })
  );

  function handleCancel() {
    visible.value = false;

  }

  const booleanFields = ref({
    "tox_gov_approved": false,
    "ecotox_gov_approved": false,
    "budget_confirmed": false,
    "po_placed": false,
    "contract_signed": false,
    "vv_doc_uploaded": false,
    "task_confirmed": false,
    "study_notified": false,
    "test_item_data_sheet": false,
    "ssd_finished": false,
    "sed_uploaded": false,
  })
  async function handleSave(e) {


    if (!e.valid) return;

    let updatedFields = {};
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        if (field === "project") {
          updatedFields["project_id"] = state.value.id;
        } else if (field === "task_name") {
          updatedFields["task_name"] = state.value.task_name;

        } else if (field === "start_year") {
          updatedFields["start_year"] = parseInt(state.value, 10); //check if this is needed
        } else if (field === "task_owner") {
          updatedFields["task_owner_id"] = state.value.id;
        } else {
          // for other fields
          updatedFields[field] = state.value;
        }
      }
    });



    let newData;
    if (initialFormData.id) {
      // edit task
      newData = await Api.patch(`/tasks/${initialFormData.id}`, updatedFields);
    } else {
      // new task
      newData = await Api.post("/tasks/", updatedFields);
    }

    emit("refresh", newData);
    emit("close");
  }
</script>
