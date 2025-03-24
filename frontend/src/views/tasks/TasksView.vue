<script setup>
// #region view
import { ref, inject, onMounted, useTemplateRef, nextTick } from "vue";
import { FilterMatchMode } from "@primevue/core";
import { useToast } from "primevue/usetoast";

import TaskForm from "./TaskForm.vue";
import ColumnSetting from "./ColumnSetting.vue";
import TaskExpansion from "./TaskExpansion.vue";
import TaskCard from "./TaskCard.vue";

const layout = ref("table"); // table, grid
const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  task_name: { value: null, matchMode: FilterMatchMode.EQUALS },
  project_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
  start_year: { value: null, matchMode: FilterMatchMode.EQUALS },
});
const globalFilterFields = [
  "task_name",
  "project_name",
  "pi_number",
  "tk_number",
  "cro_name",
  "crop",
  "tags",
];

const tasks = ref();
const Api = inject("Api");
const toast = useToast();

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
  taskTableRef.value.exportCSV();
}

//#region Task Table
const taskTableRef = useTemplateRef("taskTableRef");
const showTaskForm = ref(false);
const defaultTaskColumns = {
  project_name: "Project Name",
  task_name: "Task Name",
  tags: "Tags",
  task_owner_name: "Task Owner Name",
  task_confirmed: "Task Confirmed",
  task_status: "Task Status",
  start_year: "Start Year",
  expected_delivery_date: "Expected Delivery Date",
  pi_number: "PI Number",
  tk_number: "TK Number",
  tox_gov_approved: "Tox Gov Approved",
  ecotox_gov_approved: "EcoTox Gov Approved",
};
const visibleTaskColumns = ref(
  JSON.parse(localStorage.getItem("visibleTaskColumns")) ?? defaultTaskColumns
);
const selectedTasks = ref([]);
const expandedRows = ref([]);
const editingRows = ref([]);

let initialTaskFormData;

const userSuggestion = ref();
async function filterUserSuggestion(event) {
  userSuggestion.value = await Api.get(`/users/search?query=${event.query}`);
}
const croSuggestion = ref();
async function filterCroSuggestion(event) {
  console.log("filterCroSuggestion", event);
  croSuggestion.value = await Api.get(`/cros/search?query=${event.query}`);
}

function handleShowTaskForm(mode, data) {
  if (mode === "new") {
    initialTaskFormData = {};
  } else if (mode === "edit") {
    const project = { project_id: data.id, project_name: data.project_name };
    initialTaskFormData = { ...data, project };
  }
  showTaskForm.value = true;
}

function handleCloseTaskForm() {
  showTaskForm.value = false;
  initialTaskFormData = null;
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

function handleShowCreateTasks() {
  toast.add({
    severity: "warn",
    summary: "Warn Message",
    detail: "To be implemented",
    life: 3000,
  });
}

import { getStatusSeverity } from "../../composables/fieldTools.js";
// function getStatusSeverity(status) {
//   switch (status) {
//     case "Idle":
//       return "secondary";
//     case "Go":
//       return "info";
//     case "Finished":
//       return "success";
//     case "Pending":
//       return "danger";
//     case "Terminated":
//       return "danger";
//     default:
//       return "primary"; // 或者其他默认值
//   }
// }

function onRowExpand(event) {
  console.log("onRowExpand", event);
}

import { getChangedFields } from "../../composables/fieldTools.js";

async function onRowEditSave(event) {
  const { data, newData, index } = event;
  const updatedFields = getChangedFields(data, newData);
  if (updatedFields.length !== 0) {
    tasks.value[index] = await Api.patch(`/tasks/${data.id}`, updatedFields);
    // tasks.value.splice(index, 1, response)
  }
}

// #endregion

// #region Column Setting
const showColumnSetting = ref(false);
const columnSettingRef = useTemplateRef("columnSettingRef");

async function handleToggleColumnSetting(event) {
  if (showColumnSetting.value) {
    showColumnSetting.value = false;
  } else {
    showColumnSetting.value = true;
    await nextTick();
    columnSettingRef.value.toggle(event);
  }
}
function handleApplyColumnSelection(selectedColumns) {
  // selectedColumns is an array of column names

  visibleTaskColumns.value = selectedColumns;
  showColumnSetting.value = false;
  localStorage.setItem("visibleTaskColumns", JSON.stringify(selectedColumns));
}

// #endregion

// #region Comment Drawer
import CommentDrawer from "./CommentDrawer.vue";
const showCommentDrawer = ref(false);
const commentDrawerProps = {};
function handleShowComments(data) {
  commentDrawerProps.project_id = data.project_id;
  commentDrawerProps.task_id = data.id;
  showCommentDrawer.value = true;
}
function handleCloseComments() {
  showCommentDrawer.value = false;
}

// #endregion Comment Drawer

// #region Task GAP
import TaskGap from "./TaskGap.vue";
const showTaskGap = ref(false);
const taskGapProps = {};

function handleShowGap(task) {
  taskGapProps.task_id = task.id;
  taskGapProps.gap_id = task.gap_id;

  showTaskGap.value = true;
}
function handleCloseGap() {
  showTaskGap.value = false;
}
function handleRefreshGap(task_id, gap_id) {
  const index = tasks.value.findIndex((task) => task.id === task_id);
  tasks.value[index].gap_id = gap_id;
}
// #endregion Task GAP
</script>

<template>
  <div>
    <Toolbar pt:start="gap-2" pt:end="gap-2" class="min-w-200">
      <template #start>
        <SplitButton
          severity="secondary"
          label="Create"
          icon="pi pi-plus"
          @click="handleShowTaskForm('new', null)"
          :model="[
            {
              label: 'Batch Create',
              icon: 'pi pi-cart-plus',
              command: handleShowCreateTasks,
            },
          ]"
        >
        </SplitButton>
      </template>

      <template #center>
        <IconField v-tooltip.top="'Search by ' + globalFilterFields.join(',')">
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText placeholder="Search" v-model="filters['global'].value" />
        </IconField>
      </template>

      <template #end>
        <Button
          icon="pi pi-cog"
          rounded
          severity="secondary"
          v-tooltip.top="'Select columns'"
          @click="handleToggleColumnSetting"
        ></Button>

        <SelectButton
          v-model="layout"
          :options="['table', 'grid']"
          :allowEmpty="false"
          v-tooltip.top="'Toggle display table/grid'"
        >
          <template #option="{ option }">
            <i :class="[option === 'grid' ? 'pi pi-bars' : 'pi pi-table']" />
          </template>
        </SelectButton>
        <SplitButton
          severity="secondary"
          label="Export"
          icon="pi pi-download"
          @click="handleExportTasks"
          :model="[
            {
              label: 'Import',
              icon: 'pi pi-upload',
              command: handleImportTasks,
            },
          ]"
        >
        </SplitButton>
      </template>
    </Toolbar>

    <DataTable
      v-if="layout === 'table'"
      ref="taskTableRef"
      :value="tasks"
      dataKey="id"
      scrollable
      scroll-height="flex"
      resizable-columns
      column-resize-mode="expand"
      v-model:selection="selectedTasks"
      selectionMode="single"
      v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand"
      v-model:editingRows="editingRows"
      editMode="row"
      @rowEditSave="onRowEditSave"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="globalFilterFields"
      sortMode="multiple"
      removableSort
      pt:header="px-0"
    >
      <Column expander class="w-4 p-0" frozen />

      <Column class="w-4 p-0 mx-auto" frozen>
        <template #body="{ data }">
          <Button
            severity="secondary"
            variant="text"
            rounded
            size="small"
            class="p-0"
            icon="pi pi-comments"
            @click="handleShowComments(data)"
          ></Button>
        </template>
      </Column>
      <Column rowEditor class="w-4 p-0" frozen />

      <!-- MARK: Task Name -->

      <Column
        v-if="visibleTaskColumns['task_name']"
        field="task_name"
        :header="visibleTaskColumns['task_name']"
        sortable
        frozen
      >
        <template #body="{ data, field }">
          <Button
            :label="data[field]"
            variant="link"
            @click="handleShowTaskForm('edit', data)"
            class="text-nowrap px-0"
          ></Button>
        </template>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]"></InputText>
        </template>
        <template #filter="{ filterModel }">
          <InputText
            v-model="filterModel.value"
            type="text"
            placeholder="Search"
          />
        </template>
      </Column>
      <!-- MARK: Project Name -->
      <Column
        v-if="visibleTaskColumns['project_name']"
        field="project_name"
        :header="visibleTaskColumns['project_name']"
        sortable
      >
        <template #filter="{ filterModel }">
          <InputText v-model="filterModel.value" type="text" />
        </template>
      </Column>
      <!-- MARK: Product Stage -->
      <Column
        v-if="visibleTaskColumns['product_stage']"
        field="product_stage"
        :header="visibleTaskColumns['product_stage']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="getStatusSeverity('product_stage', data[field])"
            :value="data[field]"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: Task Category -->
      <Column
        v-if="visibleTaskColumns['task_category']"
        field="task_category"
        :header="visibleTaskColumns['task_category']"
        sortable
      >
      </Column>
      <!-- MARK: Task Status -->
      <Column
        v-if="visibleTaskColumns['task_status']"
        field="task_status"
        :header="visibleTaskColumns['task_status']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="getStatusSeverity('task_status', data[field])"
            :value="data[field]"
          ></Tag>
        </template>
        <template #editor="{ data, field }">
          <Select
            :options="enums.TaskStatusEnum"
            v-model="data[field]"
            class="w-full"
          />
        </template>
      </Column>
      <!-- MARK Start Year-->
      <Column
        v-if="visibleTaskColumns['start_year']"
        field="start_year"
        :header="visibleTaskColumns['start_year']"
        sortable
      >
      </Column>
      <!-- MARK: Expected Delivery Date -->
      <Column
        v-if="visibleTaskColumns['expected_delivery_date']"
        field="expected_delivery_date"
        :header="visibleTaskColumns['expected_delivery_date']"
        sortable
      >
      </Column>
      <!-- MARK: Task Owner Name -->
      <Column
        v-if="visibleTaskColumns['task_owner_name']"
        field="task_owner_name"
        :header="visibleTaskColumns['task_owner_name']"
      >
        <template #editor="{ data, field }">
          <AutoComplete
            optionLabel="name"
            v-model="data[field]"
            :suggestions="userSuggestion"
            @complete="filterUserSuggestion"
            @update:modelValue="(value) => (data['task_owner_id'] = value.id)"
            forceSelection
            dropdown
          />
        </template>
      </Column>
      <!-- MARK: Crop -->
      <Column
        v-if="visibleTaskColumns['crop']"
        field="crop"
        :header="visibleTaskColumns['crop']"
      >
      </Column>
      <!-- MARK: Target -->
      <Column
        v-if="visibleTaskColumns['target']"
        field="target"
        :header="visibleTaskColumns['target']"
      >
      </Column>
      <!-- MARK: Task Confirmed -->
      <Column
        v-if="visibleTaskColumns['task_confirmed']"
        field="task_confirmed"
        :header="visibleTaskColumns['task_confirmed']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>

      <!-- MARK: Budget Confirmed -->
      <Column
        v-if="visibleTaskColumns['budget_confirmed']"
        field="budget_confirmed"
        :header="visibleTaskColumns['budget_confirmed']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>

      <!-- MARK: Cost Center -->
      <Column
        v-if="visibleTaskColumns['cost_center']"
        field="cost_center"
        :header="visibleTaskColumns['cost_center']"
      >
      </Column>
      <!-- MARK: tox_gov_approved -->
      <Column
        v-if="visibleTaskColumns['tox_gov_approved']"
        field="tox_gov_approved"
        :header="visibleTaskColumns['tox_gov_approved']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: ecotox_gov_approved -->
      <Column
        v-if="visibleTaskColumns['ecotox_gov_approved']"
        field="ecotox_gov_approved"
        :header="visibleTaskColumns['ecotox_gov_approved']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: pi_number -->
      <Column
        v-if="visibleTaskColumns['pi_number']"
        field="pi_number"
        :header="visibleTaskColumns['pi_number']"
      >
      </Column>
      <!-- MARK: tk_number -->
      <Column
        v-if="visibleTaskColumns['tk_number']"
        field="tk_number"
        :header="visibleTaskColumns['tk_number']"
      >
      </Column>

      <!-- MARK: gap -->
      <Column
        v-if="visibleTaskColumns['gap_id']"
        field="gap_id"
        :header="visibleTaskColumns['gap_id']"
      >
        <template #body="{ data }">
          <i
            :class="data.gap_id ? 'pi pi-image' : 'pi pi-cloud-upload'"
            style="font-size: 1.5rem; color: var(--p-primary-color)"
            @click="handleShowGap(data)"
          ></i>
        </template>
      </Column>
      <!-- MARK: doc_link -->
      <Column
        v-if="visibleTaskColumns['doc_link']"
        field="doc_link"
        :header="visibleTaskColumns['doc_link']"
      >
        <template #body="{ data, field }">
          <a
            :href="data[field]"
            v-if="data[field]"
            target="_blank"
            class="text-primary font-bold hover:underline"
            ><i class="pi pi-link"></i
          ></a>
        </template>
      </Column>
      <!-- MARK: estimated_cost -->
      <Column
        v-if="visibleTaskColumns['estimated_cost']"
        field="estimated_cost"
        :header="visibleTaskColumns['estimated_cost']"
      >
      </Column>
      <!-- MARK: actual_cost -->
      <Column
        v-if="visibleTaskColumns['actual_cost']"
        field="actual_cost"
        :header="visibleTaskColumns['actual_cost']"
      >
      </Column>
      <!-- MARK: po_placed -->
      <Column
        v-if="visibleTaskColumns['po_placed']"
        field="po_placed"
        :header="visibleTaskColumns['po_placed']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: contract_signed -->
      <Column
        v-if="visibleTaskColumns['contract_signed']"
        field="contract_signed"
        :header="visibleTaskColumns['contract_signed']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: payment_method -->
      <Column
        v-if="visibleTaskColumns['payment_method']"
        field="payment_method"
        :header="visibleTaskColumns['payment_method']"
      >
      </Column>
      <!-- MARK: payment_status -->
      <Column
        v-if="visibleTaskColumns['payment_status']"
        field="payment_status"
        :header="visibleTaskColumns['payment_status']"
      >
      </Column>
      <!-- vv_doc_uploaded -->
      <Column
        v-if="visibleTaskColumns['vv_doc_uploaded']"
        field="vv_doc_uploaded"
        :header="visibleTaskColumns['vv_doc_uploaded']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: vv_doc_number -->
      <Column
        v-if="visibleTaskColumns['vv_doc_number']"
        field="vv_doc_number"
        :header="visibleTaskColumns['vv_doc_number']"
      >
      </Column>
      <!-- MARK: task_progress -->
      <Column
        v-if="visibleTaskColumns['task_progress']"
        field="task_progress"
        :header="visibleTaskColumns['task_progress']"
      >
      </Column>
      <!-- MARK: planned_start -->
      <Column
        v-if="visibleTaskColumns['planned_start']"
        field="planned_start"
        :header="visibleTaskColumns['planned_start']"
      >
      </Column>
      <!-- MARK: expected_finish -->
      <Column
        v-if="visibleTaskColumns['expected_finish']"
        field="expected_finish"
        :header="visibleTaskColumns['expected_finish']"
      >
      </Column>
      <!-- MARK: actual_start -->
      <Column
        v-if="visibleTaskColumns['actual_start']"
        field="actual_start"
        :header="visibleTaskColumns['actual_start']"
      >
      </Column>
      <!-- MARK: actual_finish -->
      <Column
        v-if="visibleTaskColumns['actual_finish']"
        field="actual_finish"
        :header="visibleTaskColumns['actual_finish']"
      >
      </Column>
      <!-- MARK: delivery_date -->
      <Column
        v-if="visibleTaskColumns['delivery_date']"
        field="delivery_date"
        :header="visibleTaskColumns['delivery_date']"
      >
      </Column>
      <!-- MARK: stuff_days -->
      <Column
        v-if="visibleTaskColumns['stuff_days']"
        field="stuff_days"
        :header="visibleTaskColumns['stuff_days']"
      >
      </Column>
      <!-- MARK: cro_name-->
      <Column
        v-if="visibleTaskColumns['cro_name']"
        field="cro_name"
        :header="visibleTaskColumns['cro_name']"
      >
        <template #editor="{ data, field }">
          <AutoComplete
            optionLabel="cro_name"
            v-model="data[field]"
            :suggestions="croSuggestion"
            @complete="filterCroSuggestion"
            @update:modelValue="(value) => (data['cro_id'] = value.id)"
            forceSelection
            dropdown
          />
        </template>
      </Column>
      <!-- MARK: sample_status -->
      <Column
        v-if="visibleTaskColumns['sample_status']"
        field="sample_status"
        :header="visibleTaskColumns['sample_status']"
      >
        <template #body="{ data, field }">
          <router-link
            v-if="data['sample_id']"
            :to="{ path: '/samples', query: { id: data['sample_id'] } }"
            class="text-primary font-bold hover:underline"
            >{{ data[field] }}</router-link
          >
        </template>
      </Column>
      <!-- MARK: study_notified -->
      <Column
        v-if="visibleTaskColumns['study_notified']"
        field="study_notified"
        :header="visibleTaskColumns['study_notified']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: analytes -->
      <Column
        v-if="visibleTaskColumns['analytes']"
        field="analytes"
        :header="visibleTaskColumns['analytes']"
      >
      </Column>
      <!-- MARK: key_results -->
      <Column
        v-if="visibleTaskColumns['key_results']"
        field="key_results"
        :header="visibleTaskColumns['key_results']"
      >
      </Column>
      <!-- MARK: guidelines -->
      <Column
        v-if="visibleTaskColumns['guidelines']"
        field="guidelines"
        :header="visibleTaskColumns['guidelines']"
      >
      </Column>
      <!-- MARK: test_item_data_sheet -->
      <Column
        v-if="visibleTaskColumns['test_item_data_sheet']"
        field="test_item_data_sheet"
        :header="visibleTaskColumns['test_item_data_sheet']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: ssd_finished -->
      <Column
        v-if="visibleTaskColumns['ssd_finished']"
        field="ssd_finished"
        :header="visibleTaskColumns['ssd_finished']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: sed_uploaded -->
      <Column
        v-if="visibleTaskColumns['sed_uploaded']"
        field="sed_uploaded"
        :header="visibleTaskColumns['sed_uploaded']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: global_study_manager -->
      <Column
        v-if="visibleTaskColumns['global_study_manager']"
        field="global_study_manager"
        :header="visibleTaskColumns['global_study_manager']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>
      <!-- MARK: cro_study_director -->
      <Column
        v-if="visibleTaskColumns['cro_study_director']"
        field="cro_study_director"
        :header="visibleTaskColumns['cro_study_director']"
      >
        <template #body="{ data, field }">
          <Tag
            :severity="data[field] ? 'success' : 'warn'"
            :value="data[field] ? 'YES' : 'NO'"
          ></Tag>
        </template>
      </Column>

      <template #expansion="{ data, index }">
        <TaskExpansion :task="data" />
      </template>

      <template #empty>
        <p class="text-center text-primary">No tasks Found!</p>
      </template>
    </DataTable>

    <DataView v-else :value="tasks">
      <template #list="{ items }">
        <div class="flex flex-col gap-4">
          <TaskCard
            v-for="(task, index) in items"
            :key="index"
            :taskData="task"
            :class="{
              'border-t border-surface-200 dark:border-surface-700':
                index !== 0,
            }"
          ></TaskCard>
        </div>
      </template>
    </DataView>

    <ColumnSetting
      v-if="showColumnSetting"
      ref="columnSettingRef"
      :visibleTaskColumns
      :defaultTaskColumns
      @apply="handleApplyColumnSelection"
      @cancel="showColumnSetting = false"
    >
    </ColumnSetting>

    <CommentDrawer
      v-if="showCommentDrawer"
      v-bind="commentDrawerProps"
      @close="handleCloseComments"
    >
    </CommentDrawer>

    <TaskGap
      v-if="showTaskGap"
      v-bind="taskGapProps"
      @close="handleCloseGap"
      @refresh="handleRefreshGap"
    >
    </TaskGap>

    <TaskForm
      v-if="showTaskForm"
      @close="handleCloseTaskForm"
      @refresh="handleRefreshTasks"
    ></TaskForm>
  </div>
</template>

<style>
/* resolve inline edit control display over frozen column when scroll */
.p-datatable-thead {
  z-index: 2;
}

.p-datatable-frozen-column {
  z-index: 1;
}
</style>
