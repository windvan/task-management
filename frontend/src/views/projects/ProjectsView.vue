<template>
  <div>
    <DataTable
      ref="projectTableRef"
      :value="projects"
      v-model:selection="selectedProject"
      v-model:expandedRows="expandedRows"
      @rowExpand="onRowExpand"
      scrollable
      selectionMode="single"
      dataKey="id"
      paginator
      v-model:filters="tableFilters"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      :globalFilterFields="globalTableFilterFields"
      tableStyle="min-width: 50rem"
      pt:header="px-0"
    >
      <template #header>
        <Toolbar pt:start="gap-2">
          <template #start>
            <Button
              icon="pi pi-plus"
              label="New"
              @click="handleShowProjectForm('new', null)"
              severity="secondary"
            />
          </template>

          <template #center>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <InputText
                placeholder="Search"
                v-model="tableFilters['global'].value"
              />
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

      <Column expander class="w-12" />
      <Column class="w-4 p-0 mx-auto" frozen>
        <template #body="{ data }">
          <Button severity="secondary" variant="text" rounded size="small" class="p-0" icon="pi pi-comments"
            @click="handleShowComments(data.id)"></Button>
        </template>
      </Column>
      <Column class="w-4 p-0 mx-auto" frozen>
        <template #body="{ data,index }">
          <Button severity="secondary" variant="text" rounded size="small" class="p-0" icon="pi pi-trash"
            @click="handleDeleteProject(data.id, index)"></Button>
        </template>
      </Column>
      <!-- <Column selectionMode="multiple" class="w-12" frozen></Column> -->
      <Column field="project_name" header="Project Name">
        <template #body="{ data }">
          <Button
            :label="data.project_name"
            variant="link"
            @click="handleShowProjectForm('edit', data)"
            class="px-0 text-left text-nowrap"
          ></Button>
        </template>
      </Column>
      <!-- <Column field="product_internal_name" header="Product"></Column> -->

      <Column field="product_stage" header="Product Stage">
        <template #body="{ data }">
          <Tag
            :severity="data.product_stage >= 'stage_C' ? 'success' : 'warn'"
            :value="data.product_stage"
          ></Tag>
        </template>
      </Column>

      <Column field="project_status" header="Project Status">
        <template #body="{ data, field }">
          <Tag
            :severity="getStatusSeverity(field, data.project_status)"
            :value="data.project_status"
          ></Tag>
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
      <Column field="submission_status" header="Submission Status"></Column>
      <Column field="approved_date" header="Approved Date">
        <template #body="{ data }">
          {{ data.approved_date ? data.approved_date : "Not Approved Yet" }}
        </template>
      </Column>

      <template #expansion="{ data }">
        <div class="mt-4 flex flex-col gap-4" @click="selectedProject = data">

          
          <div class="flex gap-4 items-center">
            <p class="text-xl">Related Tasks</p>

            <Button icon="pi pi-plus" rounded variant="outlined"
              @click="handleShowTaskForm('new', data, null)"></Button>
            <Button icon="pi pi-pencil" rounded variant="outlined" v-if="selectedTask?.project_id === data.id"
              @click="handleShowTaskForm('edit', data)"></Button>
            <Button icon=" pi pi-trash" rounded variant="outlined" v-if="selectedTask?.project_id === data.id"
              @click="handleDeleteTask(data)"></Button>
          </div>

          <DataTable
            :value="data.tasks"
            dataKey="id"
            scrollable
            scrollHeight="flex"
            selectionMode="single"
            v-model:selection="selectedTask"
            showGridlines
          >
            <!-- <Column selectionMode="single" class="w-8"></Column> -->
            <Column field="task_name" header="Task Name">
              <template #body="{ data }">
                <Button
                  variant="link"
                  class="px-0 text-left text-nowrap"
                  @click="handleShowTaskForm('edit', null, data)"
                >
                  {{ data.task_name }}
                </Button>
              </template>
            </Column>
            <Column field="task_group" header="Task Group"></Column>
            <Column field="task_category" header="Task Category"></Column>
            <Column field="task_owner_name" header="Task Owner"></Column>
            <Column field="task_status" header="Task Status"></Column>
            <Column field="start_year" header="Start Year"></Column>
            <Column
              field="expected_delivery_date"
              header="Expected Delivery Date"
            ></Column>
            <Column field="planned_start" header="Planned_Start"></Column>
            <Column field="expected_finish" header="Expected Finish"></Column>
            <Column field="actual_start" header="Actual Start"></Column>
            <Column field="actual_finish" header="Actual Finish"></Column>
            <Column header="Action">
              <template #body="props">
                <Button
                  icon=" pi pi-trash"
                  rounded
                  variant="outlined"
                  
                ></Button>
              </template>
            </Column>

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

    <ProjectForm
      v-if="showProjectForm"
      :initialFormData="initialProjectFormData"
      @close="handleCloseProjectForm"
      @refresh="handleRefreshProject"
    >
    </ProjectForm>
    <TaskFrom
      v-if="showTaskFomr"
      :initialFormData="initialTaskFormData"
      @close="handleCloseTaskForm"
      @refresh="handleRefreshProjectTasks"
    ></TaskFrom>

    <CommentDrawer v-if="showCommentDrawer" v-bind="commentDrawerProps" @close="handleCloseComments">
    </CommentDrawer>
  </div>
</template>

<script setup>
import { onMounted, inject, ref, useTemplateRef } from "vue";
import { getStatusSeverity } from "../../composables/fieldTools";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { FilterMatchMode } from "@primevue/core";

import ProjectForm from "./ProjectForm.vue";
import TaskFrom from "../tasks/TaskForm.vue";

const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
const toast = useToast();
const confirm = useConfirm();
const Api = inject("Api");

onMounted(async () => {
  projects.value = await Api.get("/projects");
});

const splitBtnItems = [
  { label: "Import", icon: "pi pi-upload", command: handleImport },
];
function handleImport() {
  toast.add({
    severity: "warn",
    summary: "Warn Message",
    detail: "To be implemented",
    life: 3000,
  });
}

function handleExport() {
  projectTableRef.value.exportCSV();
}

// #region Project table
const projectTableRef = useTemplateRef("projectTableRef");
const projects = ref();
const expandedRows = ref();
const selectedProject = ref();
const tableFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  // internal_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
});
const globalTableFilterFields = ["project_name", "product_id"];

async function onRowExpand(event) {
  // get tasks of current project
  console.log(event);
  event.data.tasks = await Api.get(`projects/${event.data.id}/tasks`);
}

function handleDeleteProject(project_id, index) {
  confirm.require({
    
    message: "Are you sure you want delete?",
    header: "Confirmation",
    icon: "pi pi-exclamation-triangle",
    accept: async () => {
      await Api.delete(`/projects/${project_id}`);
      //refresh products
      projects.value.splice(index, 1);
    }
  });
}

function handleRefreshProject(newData) {
  const index = projects.value.findIndex(
    (project) => project.id === newData.id
  );
  if (index !== -1) {
    // Object.assign(projects.value[index], newData);
    // projects.value[index] = newData;
    projects.value.splice(index, 1, newData);
  } else {
    projects.value.push(newData);
  }
}




// #endregion project table

// #region project form
const showProjectForm = ref(false);
const initialProjectFormData = ref();

function handleShowProjectForm(mode, data) {
  if (mode === "new") {
    initialProjectFormData.value = {};
  } else if (mode === "edit") {
    // handle relational fields on the form

    const product = {
      id: data.product_id,
      internal_name: data.product_internal_name,
    };
    const portfolio_contact = {
      id: data.portfolio_contact_id,
      name: data.portfolio_contact_name,
    };
    initialProjectFormData.value = { ...data, product, portfolio_contact };
  }
  showProjectForm.value = true;
}

function handleCloseProjectForm() {
  showProjectForm.value = false;
}

// #endregion

// #region related task table
const selectedTask = ref();
function handleDeleteProjectTask(project_id, task_id) {
  confirm.require({
    position: "top",
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
      await Api.delete(`/projects/${project_id}/tasks/${task_id}`);
      //refresh tasks
      const projectIndex = projects.value.findIndex(
        (project) => project.id === project_id
      );
      const taskIndex = projects.value[projectIndex].tasks.findIndex(
        (task) => task.id === task_id
      );
      projects.value[projectIndex].tasks.splice(taskIndex, 1);
    },
    reject: null,
  });
}
// #endregion

// #region Task Form
const showTaskFomr = ref(false);
const initialTaskFormData = ref();
function handleShowTaskForm(mode, project, data) {
  if (mode === "new") {
    initialTaskFormData.value = {
      project_id: project.id,
      project_name: project.project_name,
    };
  } else if (mode === "edit") {
    initialTaskFormData.value = data;
  }
  showTaskFomr.value = true;
}

function handleCloseTaskForm() {
  showTaskFomr.value = false;
}

function handleRefreshProjectTasks(project_id, newData) {
  const projectIndex = projects.value.findIndex(
    (project) => project.id === project_id
  );
  if (projectIndex !== -1) {
    projects.value[projectIndex].tasks.push(newData);
  }
}

// #endregion

  // #region Comment Drawer
  import CommentDrawer from "./CommentDrawer.vue";
  const showCommentDrawer = ref(false);
  const commentDrawerProps = {};
  function handleShowComments(proj_id) {
    commentDrawerProps.targetId = proj_id;
    commentDrawerProps.commentType = 'project';
    showCommentDrawer.value = true;
  }
  function handleCloseComments() {
    showCommentDrawer.value = false;
  }

  // #endregion Comment Drawer

</script>

<style module></style>
