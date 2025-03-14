<script setup>
  // #region view
  import { ref, inject, onMounted, useTemplateRef, onBeforeMount } from 'vue';
  import { FilterMatchMode } from "@primevue/core";
  import TaskCardView from './TaskCardView.vue';
  import TaskForm from './TaskForm.vue';
  import ColumnSetting from './ColumnSetting.vue';
  import { useToast } from 'primevue';

  const layout = ref('table');
  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    task_category: { value: null, matchMode: FilterMatchMode.EQUALS },
    project_id: { value: null, matchMode: FilterMatchMode.EQUALS },
    // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
  });
  const tasks = ref()
  const Api = inject("Api");
  const toast = useToast()

  onMounted(async () => {
    tasks.value = await Api.get("/tasks/");
  });

  function handleImportTasks() {
    toast.add({
      severity: "warn",
      summary: "Warn Message",
      detail: "To be implemented",
      life: 3000,
    });
  }

  function handleExportTasks() {
    taskTableRef.value.export()
  }
  // #endregion

  // #region Task Table
  const taskTableRef = useTemplateRef('taskTableRef')
  const showTaskForm = ref(false)
  const defaultTaskColumns = {
    "project_name": "Project Name",
    "task_name": "Task Name",
    "tags": "Tags",
    "task_owner_name": "Task Owner Name",
    "task_confirmed": "Task Confirmed",
    "task_status": "Task Status",
    "start_year": "Start Year",
    "expected_delivery_date": "Expected Delivery Date",
    "pi_number": "PI Number",
    "tk_number": "TK Number",
    "tox_gov_approved": "Tox Gov Approved",
    "ecotox_gov_approved": "EcoTox Gov Approved",
  }
  const visibleTaskColumns = JSON.parse(localStorage.getItem("visibleTaskColumns")) ?? defaultTaskColumns


  let initialTaskFormData

  // onBeforeMount(async () => {
  //   allTaskColumns = await Api.get('')
  // }),
  function handleShowTaskForm(mode, data) {
    if (mode === "new") {
      initialTaskFormData = {};
    } else if (mode === "edit") {
      const project = { project_id: data.id, project_name: data.project_name }
      initialTaskFormData = { ...data, project };
    }
    showTaskForm.value = true;
  }

  function handleCloseTaskForm() {
    showTaskForm.value = false
    initialTaskFormData = null
  }

  function handleRefreshTasks(task_id, newData) {
    const index = tasks.value.findIndex((task) => task.id === task_id);
    if (index !== -1) {
      // Object.assign(projects.value[index], newData);
      tasks.value[index] = newData;
    } else {
      tasks.value.push(newData);
    }
  }

  // #endregion Task Table


</script>

<template>
  <div>
    <DataTable v-if="layout === 'table'" ref="taskTableRef" pt:header="px-0">
      <template #header>
        <Toolbar pt:start="gap-2" pt:end="gap-2">
          <template #start>
            <SplitButton severity="secondary" label="Create" icon='pi pi-plus' @click="handleShowTaskForm('new', null)"
              :model='[{ label: "Batch Create", icon: "pi pi-cart-plus", command: handleShowCreateTasks }]'>
            </SplitButton>
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
            <Button icon="pi pi-cog" rounded severity="secondary" v-tooltip.top="'Select columns'"
              @click="showColumnSetting = !showColumnSetting"></Button>

            <ColumnSetting v-if="showColumnSetting"></ColumnSetting>

            <SelectButton v-model="layout" :options="['table', 'grid']" :allowEmpty="false"
              v-tooltip.top="'Toggle display table/grid'">
              <template #option="{ option }">
                <i :class="[option === 'grid' ? 'pi pi-bars' : 'pi pi-table']" />
              </template>
            </SelectButton>
            <SplitButton severity="secondary" label="Export" icon="pi pi-download" @click="handleExportTasks"
              :model="[{ label: 'Import', icon: 'pi pi-upload', command: handleImportTasks }]">
            </SplitButton>
          </template>
        </Toolbar>
      </template>


      <!-- <Column v-if="field in visibleTaskColumns" expander class="w-12" frozen /> -->
      <Column expander />
      <!-- <Column frozen selectionMode="multiple"></Column> -->

      <Column v-if="visibleTaskColumns['task_name']" field="task_name" header="Task Name" sortable>
        <template #body="{ data, field }">
          <Button :label="data[field]" variant="link" @click="handleShowTaskForm('edit', data)"
            class="text-nowrap"></Button>
        </template>
        <!-- <template #editor="{data,field}">
          <InputText v-model="data[field]"></InputText>
        </template> -->
      </Column>

      <Column v-if="visibleTaskColumns['project_name']" field="project_name" header="Project Name" sortable>
        <template #filter="{ filterModel }">
          <InputText v-model="filterModel.value" type="text" placeholder="Search Tasks" />
        </template>
      </Column>


      <Column filter-field="" v-if="visibleTaskColumns['task_category']" field="task_category" header="Task Category"
        sortable header-class="min-w-40"></Column>
      <Column v-if="visibleTaskColumns['tags']" field="tags" header="Tags">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>

      <Column v-if="visibleTaskColumns['task_status']" field="task_status" header="Task Status">
        <template #body="{ data, field }">
          <Tag :severity="getTaskStatusSeverity(data[field])" :value="data[field]"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Select :options="enums.TaskStatusEnum" class="w-full" :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['start_year']" field="start_year" header="Start Year" :pt="{
        headerCell: ({ parent }) => ({
          class: { 'min-w-48': parent.state['d_editing'] },
        }),
      }">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar view="year" date-format="yy" :min-date="new Date()"
            :model-value="new Date(data[field], 0)" @update:model-value="
              (value) => onCellChange(data.id, field, value?.getFullYear())
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['expected_delivery_date']" field="expected_delivery_date"
        header="Expected Delivery Date">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="new Date(data[field])" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['task_owner_id']" field="task_owner_id" header="Task Owner">
        <template #body="{ data, field }">
          {{
            selectOptions?.userOptions?.find((user) => user.id === data[field])
              ?.name
          }}
        </template>
        <template #editor="{ data, field }">
          <Select :options="selectOptions?.userOptions" option-label="name" :model-value="selectOptions?.userOptions?.find(
            (user) => user.id === data[field]
          )
            " @update:model-value="
              (value) => onCellChange(data.id, field, value.id)
            "></Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['crop']" field="crop" header="Crop">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['target']" field="target" header="Target">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>

      <Column v-if="visibleTaskColumns['task_confirmed']" field="task_confirmed" header="Task Confirmed">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>

        >
      </Column>
      <Column v-if="visibleTaskColumns['budget_confirmed']" field="budget_confirmed" header="Budget Confirmed">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['cost_center']" field="cost_center" header="Cost Center">
        <template #editor="{ data, field }">
          <Select :options="enums.CostCenterEnum" class="w-full" :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['tox_gov_approved']" field="tox_gov_approved" header="Tox_Gov Approved">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['ecotox_gov_approved']" field="ecotox_gov_approved" header="EcoTox_Gov Approved">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['pi_number']" field="pi_number" header="PI NO.">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['tk_number']" field="tk_number" header="TK NO.">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <!-- gap is not necessary and mainly for scoping tasks -->
      <Column v-if="visibleTaskColumns['gap_snapshot_url']" field="gap_snapshot_url" header="GAP Sanpshot">
        <template #body="{ data, field, index }">
          <a @click.prevent="onGapViewShow(data.id, data[field], index)" class="text-primary hover:underline">{{
            data[field] ? "Show" : "Add" }}</a>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['doc_link']" field="doc_link" header="Doc Link">
        <template #body="{ data, field }">
          <a v-if="data[field]" class="text-primary hover:underline" :href="data[field]" target="_blank">Follow</a>
        </template>
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['estimated_cost']" field="estimated_cost" header="Estimated Cost">
        <template #body="{ data, field }">
          {{ data[field] ? `&yen; ${data[field]}` : null }}
        </template>
        <template #editor="{ data, field }">
          <InputNumber :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputNumber>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['actual_cost']" field="actual_cost" header="Actual Cost">
        <template #body="{ data, field }">
          {{ data[field] ? `￥${data[field]}` : null }}
        </template>
        <template #editor="{ data, field }">
          <InputNumber :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputNumber>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['po_placed']" field="po_placed" header="PO Placed">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['contract_signed']" field="contract_signed" header="Contract Signed">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['payment_method']" field="payment_method" header="Payment Method">
        <template #editor="{ data, field }">
          <Select :options="enums.PaymentMethodEnum" class="w-full" :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['payment_status']" field="payment_status" header="Payment Status">
        <template #editor="{ data, field }">
          <Select :options="enums.PaymentStatusEnum" class="w-full" :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['vv_doc_uploaded']" field="vv_doc_uploaded" header="Veeva Uploaded">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['vv_doc_number']" field="vv_doc_number" header="Veeva Doc Number">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>

      <Column v-if="visibleTaskColumns['task_progress']" field="task_progress" header="Task Progress">
        <template #editor="{ data, field }">
          <Select :options="enums.TaskProgressEnum" class="w-full" :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['planned_start']" field="planned_start" header="Planned Start">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['expected_finish']" field="expected_finish" header="Expected Finish">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['actual_start']" field="actual_start" header="Actual Start">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['actual_finish']" field="actual_finish" header="Actual Finish">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['delivery_date']" field="delivery_date" header="Delivery Date">
        <template #editor="{ data, field }">
          <DatePicker showIcon iconDisplay="input" showButtonBar date-format="yy-mm-dd" :min-date="new Date()"
            :model-value="data[field] ? new Date(data[field]) : null" @update:model-value="
              (value) => onCellChange(data.id, field, dateToStr(value))
            " />
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['stuff_days']" field="stuff_days" header="Stuff Days">
        <template #editor="{ data, field }">
          <InputNumber :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputNumber>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['cro_id']" field="cro_id" header="CRO Name">
        <template #body="{ data, field }">
          {{
            selectOptions?.croOptions?.find((cro) => cro.id === data[field])
              ?.cro_name
          }}
        </template>
        <template #editor="{ data, field }">
          <Select :options="selectOptions?.croOptions" option-label="cro_name" :model-value="selectOptions?.croOptions?.find((cro) => cro.id === data[field])
            " @update:model-value="
              (value) => onCellChange(data.id, field, value.id)
            "></Select>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['samples']" field="samples" header="Sample Status">
        <template #body="{ data, field }">
          <a @click.prevent="onSamplesViewShow(data.id)">
            <template v-if="data[field].length > 0">
              <Tag v-for="(sample, index) in data[field]" :value="sample.sample_status" :Key="index"
                class="hover:underline" />
            </template>
            <span v-else class="text-primary hover:underline">Add</span>
          </a>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['study_notified']" field="study_notified" header="Study Notified">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>
        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>

      <Column v-if="visibleTaskColumns['analytes']" field="analytes" header="Analytes">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>

      <Column v-if="visibleTaskColumns['key_results']" field="key_results" header="Key Results">
        <template #body="{ data, field, index }">
          <a @click.prevent="onKeyResultsViewShow(data.id, data[field], index)"
            class="text-primary hover:underline">Show</a>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['guidelines']" field="guidelines" header="Guidelines">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['test_item_info_sent']" field="test_item_info_sent" header="Test Item Info Sent">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['ssd_finished']" field="ssd_finished" header="SSD Finished">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['sed_uploaded']" field="sed_uploaded" header="SED Uploaded">
        <template #body="{ data, field }">
          <Tag :severity="data[field] ? 'success' : 'warn'" :value="data[field] ? 'YES' : 'NO'"></Tag>
        </template>

        <template #editor="{ data, field }">
          <Checkbox binary :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          "></Checkbox>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['global_study_manager']" field="global_study_manager"
        header="Global Study Manager">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>
      <Column v-if="visibleTaskColumns['cro_study_director']" field="cro_study_director" header="CRO Study Director">
        <template #editor="{ data, field }">
          <InputText :model-value="data[field]" @update:model-value="
            (value) => onCellChange(data.id, field, value)
          ">
          </InputText>
        </template>
      </Column>

      <Column rowEditor class="border-l border-l-gray-300 text-center p-2" frozen align-frozen="right" :pt="{
        columnHeaderContent: 'justify-center',
        pcRowEditorInit: { root: 'size-7' },
        pcRowEditorSave: { root: 'size-7' },
        pcRowEditorCancel: { root: 'size-7' },
        headerCell: ({ parent }) => ({
          class: parent.state['d_editing'] ? 'min-w-16' : 'min-w-8',
        }),
      }">
        <template #header>
          <Button icon="pi pi-pencil" v-show="!editingRows.length" rounded class="size-7" size="small"
            severity="secondary" @click="onToggleRowEditAll" />
          <Button icon="pi pi-times" v-show="editingRows.length" rounded class="size-7" size="small"
            severity="secondary" @click="onRowEditCancelAll" />
          <Button icon="pi pi-check" v-show="editingRows.length" rounded class="size-7" size="small"
            severity="secondary" @click="onRowEditSaveAll" />
        </template>
      </Column>
      <Column frozen align-frozen="right" header=" " class="text-center p-2" header-class="w-8">
        <template #body="{ data }">
          <Button severity="secondary" rounded class="size-7" size="small" icon="pi pi-comments"
            @click="showComments(data)"></Button>
        </template>
      </Column>
      <template #empty>
        <p class="text-center text-primary">No tasks Found!</p>
      </template>

    </DataTable>


    <TaskCardView v-else></TaskCardView>

    <TaskForm v-if="showTaskForm" @close="handleCloseTaskForm" @refresh="handleRefreshTasks"></TaskForm>



  </div>
</template>