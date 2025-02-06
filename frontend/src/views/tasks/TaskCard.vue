<template>
  <Card>
    <template #title>
      Task Details: {{ task.task_name }}
    </template>
    <template #content>
      <!-- Task Overview -->
      <DataView :value="[task]">
        <template #header>
          <h3>Task Overview</h3>
        </template>
        <template #list="slotProps">
          <div class="grid">
            <div class="col-12 md:col-3">
              <b>Project ID:</b> {{ slotProps.data?.project_id }}
            </div>
            <div class="col-12 md:col-3">
              <b>Task Group:</b> {{ slotProps.data?.task_group }}
            </div>
            <div class="col-12 md:col-3">
              <b>Category:</b> {{ slotProps.data?.task_category }}
            </div>
            <div class="col-12 md:col-3">
              <b>Status:</b> {{ slotProps.data?.task_status }}
            </div>
          </div>
        </template>
      </DataView>

      <!-- Timeline -->
      <Timeline :value="timelineEvents" class="mt-4">
        <template #content="slotProps">
          <small class="text-secondary">{{ slotProps.item.date }}</small>
          <h5>{{ slotProps.item.status }}</h5>
          <p>{{ slotProps.item.description }}</p>
        </template>
      </Timeline>

      <!-- Detailed Information Table -->
      <DataTable :value="taskDetails" responsiveLayout="scroll" class="mt-4">
        <Column field="key" header="Property"></Column>
        <Column field="value" header="Value"></Column>
      </DataTable>

      <!-- Status Indicators -->
      <div class="flex justify-content-between mt-4">
        <Tag :severity="getToxGovSeverity" :value="getToxGovStatus"></Tag>
        <Tag :severity="getEcoToxGovSeverity" :value="getEcoToxGovStatus"></Tag>
        <Tag :severity="getBudgetSeverity" :value="getBudgetStatus"></Tag>
      </div>

      <!-- Progress Indicator -->
      <div class="mt-4">
        <ProgressBar :value="getTaskProgressValue" :showValue="false" />
        <small>{{ task.task_progress }}</small>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { ref, computed } from 'vue';

// 假设任务数据通过 props 传入
const props = defineProps({
  taskData: {
    type: Object,
    required: true
  }
});

const task = ref(props.taskData);

// Timeline events
const timelineEvents = computed(() => [
  {
    status: 'Expected Start',
    date: task.value.planned_start || 'Not set',
    description: 'Planned start date for the task'
  },
  {
    status: 'Expected Finish',
    date: task.value.expected_finish || 'Not set',
    description: 'Expected completion date'
  },
  {
    status: 'Actual Start',
    date: task.value.actual_start || 'Not started',
    description: 'Actual start date of the task'
  },
  {
    status: 'Actual Finish',
    date: task.value.actual_finish || 'Not completed',
    description: 'Actual completion date'
  },
  {
    status: 'Delivery Date',
    date: task.value.delivery_date || 'Not delivered',
    description: 'Date when the task was delivered'
  }
]);

// Task details for DataTable
const taskDetails = computed(() => [
  { key: 'Task Owner ID', value: task.value.task_owner_id },
  { key: 'Expected Delivery Date', value: task.value.expected_delivery_date },
  { key: 'Start Year', value: task.value.start_year },
  { key: 'PI Number', value: task.value.pi_number || 'N/A' },
  { key: 'TK Number', value: task.value.tk_number || 'N/A' },
  { key: 'GAP ID', value: task.value.gap_id || 'N/A' },
  { key: 'Cost Center', value: task.value.cost_center || 'N/A' },
  { key: 'Estimated Cost', value: task.value.estimated_cost || 'N/A' },
  { key: 'Actual Cost', value: task.value.actual_cost || 'N/A' },
  { key: 'Payment Method', value: task.value.payment_method },
  { key: 'Payment Status', value: task.value.payment_status },
  { key: 'CRO ID', value: task.value.cro_id || 'N/A' },
  { key: 'Sample ID', value: task.value.sample_id || 'N/A' },
  { key: 'Global Study Manager', value: task.value.global_study_manager || 'N/A' },
  { key: 'CRO Study Director', value: task.value.cro_study_director || 'N/A' }
]);

// Status computations
const getToxGovStatus = computed(() => task.value.tox_gov_approved ? 'Tox Gov Approved' : 'Tox Gov Not Approved');
const getToxGovSeverity = computed(() => task.value.tox_gov_approved ? 'success' : 'danger');

const getEcoToxGovStatus = computed(() => task.value.ecotox_gov_approved ? 'EcoTox Gov Approved' : 'EcoTox Gov Not Approved');
const getEcoToxGovSeverity = computed(() => task.value.ecotox_gov_approved ? 'success' : 'danger');

const getBudgetStatus = computed(() => task.value.budget_confirmed ? 'Budget Confirmed' : 'Budget Not Confirmed');
const getBudgetSeverity = computed(() => task.value.budget_confirmed ? 'success' : 'warning');

// Task progress computation
const getTaskProgressValue = computed(() => {
  switch (task.value.task_progress) {
    case 'Not_Start': return 0;
    case 'In_Progress': return 50;
    case 'Completed': return 100;
    default: return 0;
  }
});
</script>

<style scoped>
/* 可以在这里添加任何组件特定的样式 */
</style>