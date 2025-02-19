<template>
  <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable>
    <template #header>
      <p class="font-bold text-lg">Create Tasks</p>
      <div class="flex gap-4">
        <Button
          type="submit"
          form="createTasksForm"
          icon="pi pi-save"
          label="Save"
          @click="handleSave"
        />

        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form
      pt:root:id="createTasksForm"
      :resolver="resolver"
      @submit="handleSave"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32"
    >
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

      <FormField v-slot="$field" name="tags" class="form-field">
        <label for="tags">Tags</label>
        <InputText id="tags" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <!-- task selector:task_category, task_name, default_task_owner, -->
      <FormField v-slot="$field" name="tasks" class="form-field">
        <label for="task_category" class="required-mark">Tasks</label>
        <TreeSelect
          v-model="selectedNodes"
          :options="selectOptions?.taskTree"
          filter
          filterMode="strict"
          selectionMode="checkbox"
          display="chip"
          showClear
        />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
          $field.error?.message
        }}</Message>
      </FormField>

      <DataTable
        :value="newTasks"
        dataKey="id"
        scrollable
        scrollHeight="flex"
        v-model:editing-rows="editingRows"
        edit-mode="row"
        v-model:expandedRowGroups="expandedRowGroups"
        expandableRowGroups
        rowGroupMode="subheader"
        groupRowsBy="task_category"
      >
        <template #groupheader="{ data }">
          <Tag severity="info" :value="data.task_category"></Tag>
          <span class="text-[--p-tag-info-color] font-bold">{{
            '&nbsp;&nbsp;&nbsp;&nbsp;Total:' +
            newTasks.filter((task) => task.task_category === data.task_category).length
          }}</span>
        </template>

        <Column header="No." header-class="w-8">
          <template #body="{ index }">
            {{ index }}
          </template></Column
        >
        <Column field="task_category" header="Task Category*"></Column>
        <Column field="task_name" header="Task Name" header-class="min-w-60"></Column>
        <Column field="task_status" header="Task Status*" header-class="min-w-40">
          <template #body="{ field, index }">
            <Select
              v-model="newTasks[index][field]"
              :options="enums.TaskStatusEnum"
              class="w-full"
            ></Select>
          </template>
        </Column>
        <Column field="start_year" header="Start Year*" header-class="min-w-48">
          <template #body="{ index, field }">
            <DatePicker
              @hide="onDataPickerHide"
              showIcon
              iconDisplay="input"
              showButtonBar
              v-model="newTasks[index][field]"
              view="year"
              date-format="yy"
              :min-date="new Date()"
            />
          </template>
        </Column>
        <Column
          field="expected_delivery_date"
          header="Expected Delivery Date*"
          header-class="min-w-56"
        >
          <template #body="{ index, field }">
            <DatePicker
              @hide="onDataPickerHide"
              showIcon
              iconDisplay="input"
              showButtonBar
              v-model="newTasks[index][field]"
              :min-date="new Date()"
            />
          </template>
        </Column>

        <Column field="crop" header="Crop" header-class="min-w-48">
          <template #body="{ index, field }">
            <InputText v-model="newTasks[index][field]"></InputText>
          </template>
        </Column>
        <Column field="target" header="Target" header-class="min-w-48">
          <template #body="{ index, field }">
            <InputText v-model="newTasks[index][field]"></InputText>
          </template>
        </Column>

        <Column field="task_owner" header="Task Owner*" header-class="min-w-48">
          <template #body="{ index, field }">
            <Select
              v-model="newTasks[index][field]"
              :options="selectOptions.userOptions"
              option-label="name"
            ></Select>
          </template>
        </Column>
      </DataTable>
      <Message v-if="tableError" size="small" variant="simple" severity="error">{{
        tableError
      }}</Message>
    </Form>
  </Dialog>
</template>

<script setup>
  import { inject, onMounted, ref, computed } from 'vue'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'
  import { dateToStr } from '@/composables/dateTools'

  const visible = defineModel('visible')
  const emit = defineEmits(['refresh'])

  let selectOptions //all select components options on this page
  const Api = inject('Api')
  const expandedRowGroups = ref(null)
  const tableError = ref('')
  const selectedNodes = ref(null)
  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
  const resolver = yupResolver(
    yup.object().shape({
      project: yup.mixed().required(),
      tags: yup
        .string()
        .test(
          'is-tag-format',
          'Value must be one or more #string# separated by spaces, string length <20',
          (value) => {
            const pattern = /^(#\w{1,20}#\s*)+$/
            return pattern.test(value?.trim())
          }
        ),
      tasks: yup.mixed().required(),
      expected_delivery_date: yup.date().required()
    })
  )

  const editingRows = ref()

  function onDataPickerHide() {
    // a compromise for datepicker in datatable cell-edit-mode
    document.body.click()
  }

  async function getSelectOptions() {
    try {
      let response = await Api.get('/tasks/select-options')
      selectOptions = response.data
    } catch (err) {
      console.log('get select options failed on tasks view', err)
    }
  }

  onMounted(async () => {
    await getSelectOptions()
    selectedNodes.value = null
    expandedRowGroups.value = selectOptions.taskTree.map((group) => group.key)
    tableError.value = ''
  })

  const newTasks = computed(() => {
    if (!selectedNodes.value) {
      return
    }
    return Object.keys(selectedNodes.value)
      .filter((nodeKey) => !isNaN(nodeKey))
      .map((nodeKey) => {
        let libraryItem = selectOptions?.taskLibrary.find((item) => item.id === Number(nodeKey))
        return {
          task_category: libraryItem.task_category,
          task_name: libraryItem?.task_name_prefix,
          task_status: 'Idle',
          start_year: null,
          expected_delivery_date: null,
          task_owner: selectOptions?.userOptions.find(
            (user) => user.id === libraryItem.default_task_owner_id
          )
        }
      })
  })

  async function handleSave(e) {
    if (e.valid) {
      //validate table value

      tableError.value = ''
      const rowSchema = yup.object().shape({
        task_category: yup.string().required(),
        task_name: yup.string().required(),
        task_status: yup.string().required(),
        start_year: yup.date().required('Start year is required in the table'),
        expected_delivery_date: yup
          .date()
          .required('Expected Delivery Date is required in the table'),
        task_owner: yup.mixed().required('Task Owner is required in the table')
      })

      for (let i = 0; i < newTasks.value?.length; i++) {
        try {
          await rowSchema.validate(newTasks.value[i])
        } catch (err) {
          tableError.value = `Row ${i} : ${err.message}`
          break
        }
      }

      // post new tasks to database
      const task_create = []
      for (let i = 0; i < newTasks.value?.length; i++) {
        let _edd = newTasks.value[i].expected_delivery_date
        task_create.push({
          project_id: e.states?.project.value.id,
          tags: e.states?.tags.value,
          task_category: newTasks.value[i].task_category,
          task_name: newTasks.value[i].task_name,
          task_owner_id: newTasks.value[i].task_owner.id,
          task_status: newTasks.value[i].task_status,
          expected_delivery_date: dateToStr(_edd),
          start_year: newTasks.value[i].start_year.getFullYear(),
          crop: newTasks.value[i].crop,
          target: newTasks.value[i].target
        })
      }

      console.log(task_create)

      try {
        await Api.post('/tasks', task_create)
        // const response = await Api.get('/tasks/')
        // tasks.value = response.data
        visible.value = false
        emit('refresh')
      } catch (err) {
        console.error(err)
      }
    }
  }

  function handleCancel() {
    visible.value = false
  }
</script>
