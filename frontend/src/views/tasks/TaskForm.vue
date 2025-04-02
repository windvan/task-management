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
      <!-- task_status -->
      <FormField v-slot="$field" name="task_status" class="form-field">
        <label for="task_status">Task Status</label>
        <Select inputId="task_status" :options="enums.TaskStatusEnum" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- start_year -->
      <FormField v-slot="$field" name="start_year" class="form-field">
        <label for="start_year">Start Year</label>
        <InputText type="number" :min="new Date().getFullYear" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- expected_delivery_date -->
      <FormField v-slot="$field" name="expected_delivery_date" class="form-field">
        <label for="expected_delivery_date">Expected Delivery Date</label>
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
      <!-- task_owner -->
      <FormField v-slot="$field" name="key_results" class="form-field">
        <label for="key_results">Key Results</label>
        <Textarea id="key_results"></Textarea>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
    </Form>
  </Dialog>
</template>

<script setup>
  import { computed, inject, onMounted, ref, useTemplateRef } from "vue";
  import { InputText, useToast } from "primevue";
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  const taskLibrary = JSON.parse(localStorage.getItem("cachedTaskLibrary")) || {};
  const taskNameLibrary = taskLibrary.map(task => task.task_name)
  const toast = useToast();
  const Api = inject("Api");

  const emit = defineEmits(["close", "refresh"]);
  const visible = ref(true);
  const { initialFormData } = defineProps({ initialFormData: Object });

  const projectSuggestion = ref();
  async function filterProjectSuggestion(event) {
    projectSuggestion.value = await Api.get(
      `/projects/search?query=${event.query}`
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
  // onMounted(async () => {
  //   try {
  //     let response = await Api.get('/tasks/select-options')
  //     selectOptions = response.data
  //   } catch (err) {
  //     console.log('get select options failed on tasks edit view', err)
  //   }

  //   taskCategoryOptions.value = [
  //     ...new Set(selectOptions?.taskLibrary.map((item) => item['task_category']))
  //   ]

  //   let processedFormData = { ...initialFormData }

  //   processedFormData.project = selectOptions?.projectOptions.find(
  //     (proj) => proj.id === initialFormData.project_id
  //   )
  //   processedFormData.task_owner = selectOptions?.userOptions.find(
  //     (user) => user.id === initialFormData.task_owner_id
  //   )
  //   processedFormData.start_year = new Date(initialFormData.start_year, 0, 1)
  //   processedFormData.expected_delivery_date = new Date(initialFormData.expected_delivery_date)

  //   _initialFormData.value = processedFormData
  // })

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


  async function handleSave(e) {
    console.log(e)

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
