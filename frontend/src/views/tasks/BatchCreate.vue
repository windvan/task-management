<template>
  <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
    <template #header>
      <p class="font-bold text-lg">Create Tasks</p>
      <div class="flex gap-4">
        <Button type="submit" form="batchCreateForm" icon="pi pi-save" label="Save" @click="handleSave" />

        <Button icon="pi pi-times" label="Cancel" @click="emit('close')" />
      </div>
    </template>
    <Form pt:root:id="batchCreateForm" :resolver="resolver" @submit="handleSave"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32">
      <!-- project -->
      <FormField v-slot="$field" name="project" class="form-field">
        <label for="project" class="required-mark">Project</label>
        <AutoComplete inputId="project" optionLabel="project_name" :suggestions="projectSuggestion"
          @complete="filterProjectSuggestion" forceSelection placeholder="Search" dropdown fluid
          :disabled="Boolean(initialFormData?.project)" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>


      <!-- task selector:task_category, task_name, default_task_owner, -->
      <FormField v-slot="$field" name="tasks" class="form-field">
        <label for="task_category" class="required-mark">Tasks</label>
        <TreeSelect v-model="selectedTasks" :options="taskOptions" filter filterMode="strict" selectionMode="checkbox"
          display="chip" showClear :maxSelectedLabels="3">
          <!-- <template #value="value">
            <Chip v-if="!(value?.children)">{{ value.label }}</Chip>
          </template> -->
        </TreeSelect>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
        <Message v-if="tableError" size="small" variant="simple" severity="error">{{
          tableError
        }}</Message>
      </FormField>

      <DataTable :value="newTasks" dataKey="id" scrollable scrollHeight="flex" v-model:editingRows="newTasks"
        editMode="row" v-model:expandedRowGroups="expandedRowGroups" expandableRowGroups rowGroupMode="subheader"
        groupRowsBy="task_category">
        <template #groupheader="{ data }">
          <Tag severity="info" :value="data['task_category']" class="mx-2"></Tag>
          <span class="text-primary font-bold">{{
            'Total:' +
            newTasks.filter((task) => task.task_category === data.task_category).length
          }}</span>
        </template>

        <Column header="No." header-class="w-8">
          <template #body="{ index }">
            {{ index + 1 }}
          </template>
        </Column>

        <Column field="task_category" header="Task Category*"></Column>
        <!-- <Column rowEditor></Column> -->
        <Column field="task_name" header="Task Name" class="min-w-60"></Column>
        <Column field="task_status" header="Task Status*" header-class="min-w-40">
          <template #editor="{ field, data }">
            <Select v-model="data[field]" :options="enums.TaskStatusEnum"></Select>
          </template>
        </Column>
        <Column field="start_year" header="Start Year*" header-class="min-w-48">
          <template #editor="{ data, field }">
            <InputText v-model="data[field]" type="number" />
          </template>

        </Column>
        <Column field="expected_delivery_date" header="Expected Delivery Date*" header-class="min-w-56">
          <template #editor="{ data, field }">
            <DatePicker v-model="data[field]" showIcon iconDisplay="input" showButtonBar :min-date="new Date()" />
          </template>
        </Column>

        <Column field="task_owner" header="Task Owner*" header-class="min-w-48">
          <template #body="{ data, field }">
            {{ data[field].name }}
          </template>
          <template #editor="{ data, field }">
            <AutoComplete inputId="task_owner" optionLabel="name" :suggestions="taskOwnerSuggestion"
              v-model="data[field]" @complete="filterTaskOwnerSuggestion" forceSelection placeholder="Search" dropdown
              fluid dataKey="id" />
          </template>
        </Column>
      </DataTable>

    </Form>
  </Dialog>
</template>

<script setup>
  import { inject, onMounted, ref, computed } from 'vue'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'


  const visible = ref(true)
  const emit = defineEmits(['close', 'refresh'])
  const { initialFormData } = defineProps({ initialFormData: { type: Object, required: false } })

  const Api = inject('Api')
  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}

  const resolver = yupResolver(
    yup.object().shape({
      project: yup.mixed().required(),
      tasks: yup.mixed().required()
    })
  )


  // function onDataPickerHide() {
  //   // a compromise for datepicker in datatable cell-edit-mode
  //   document.body.click()
  // }



  const projectSuggestion = ref()
  async function filterProjectSuggestion(event) {
    projectSuggestion.value = await Api.get(
      `/projects/search?query=${event.query}`
    )
  }

  const taskLibrary = JSON.parse(localStorage.getItem('cachedTaskLibrary')) || {}
  let taskOptions = taskLibrary.reduce((groups, item) => {
    const group = groups.find(g => g.key === item.task_category);
    if (group) {
      group.children.push({
        key: item.id,
        label: item.task_name
      });
    } else {
      groups.push({
        key: item.task_category,
        label: item.task_category,
        children: [{
          key: item.id,
          label: item.task_name
        }]
      });
    }
    return groups;
  }, []);


  const selectedTasks = ref()
  const newTasks = computed(() => {

    if (!selectedTasks.value) {
      return
    }
    return Object.keys(selectedTasks.value)
      .filter((nodeKey) => !isNaN(nodeKey))
      .map((nodeKey) => {

        let libraryItem = taskLibrary.find((item) => item.id === Number(nodeKey))
        return {
          task_category: libraryItem.task_category,
          task_name: libraryItem?.task_name,
          task_status: 'Idle',
          start_year: new Date().getFullYear(),
          expected_delivery_date: null,
          task_owner: libraryItem.default_task_owner_id ? {
            id: libraryItem.default_task_owner_id,
            name: libraryItem.default_task_owner_name
          } : undefined,
          task_owner_id: libraryItem.default_task_owner_id

        }
      })
  })

  const expandedRowGroups = ref(['Tox_Study', 'Eco_Tox_Study', 'Risk_Assessment', 'Residue_Study', 'Processing_Residue_Study', 'Unplanned',]
  )
  const taskOwnerSuggestion = ref()
  async function filterTaskOwnerSuggestion(event) {
    taskOwnerSuggestion.value = await Api.get(
      `/users/search?query=${event.query}`
    )
  }

  const tableError = ref('')



  async function handleSave(e) {
    if (e.valid) {
      console.log('e', e)
      //validate table value
      tableError.value = ''
      const rowSchema = yup.object().shape({
        task_name: yup.string().required(),
        task_status: yup.string().required(),
        start_year: yup.number().min(new Date().getFullYear()).max(9999).required('Start year is required in the table'),
        expected_delivery_date: yup
          .date()
          .required('Expected Delivery Date is required in the table'),
        task_owner: yup.mixed().required('Task Owner is required in the table'),

      })

      let valid_tasks = []
      console.log('newtasks', newTasks.value)

      for (let i = 0; i < newTasks.value?.length; i++) {
        try {
          let newTask = await rowSchema.validate(newTasks.value[i])
          newTask.project_id = e.states?.project.value.id
          newTask.task_owner_id = newTask.task_owner.id
          delete newTask.task_category
          delete newTask.task_owner
          valid_tasks.push(newTask)
        } catch (error) {
          // console.log(error)
          tableError.value = `${error} at row ${i + 1}`;
          return;
        }
      }

      console.log('valid_tasks', valid_tasks)

      // post new tasks to database

      const newData = await Api.post('/tasks/', valid_tasks)
      emit('close')
      emit('refresh', newData)


    }
  }
  // post new tasks to database
  // const task_create = []
  // for (let i = 0; i < newTasks.value?.length; i++) {
  //   let _edd = newTasks.value[i].expected_delivery_date
  //   task_create.push({
  //     project_id: e.states?.project.value.id,
  //     tags: e.states?.tags.value,
  //     task_category: newTasks.value[i].task_category,
  //     task_name: newTasks.value[i].task_name,
  //     task_owner_id: newTasks.value[i].task_owner.id,
  //     task_status: newTasks.value[i].task_status,
  //     expected_delivery_date: _edd,
  //     start_year: newTasks.value[i].start_year.getFullYear(),
  //     crop: newTasks.value[i].crop,
  //     target: newTasks.value[i].target
  //   })
  // }



  // try {
  //   await Api.post('/tasks', task_create)
  //   // const response = await Api.get('/tasks/')
  //   // tasks.value = response.data
  //   visible.value = false
  //   emit('refresh')
  // } catch (err) {
  //   console.error(err)
  // }
  //   }
  // }

</script>
