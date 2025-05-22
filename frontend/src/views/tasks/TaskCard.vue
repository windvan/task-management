<template>
  <div class="px-8 py-4">
    <h1 class="font-bold text-xl text-primary mb-2">
      {{ taskData.project_name }}: {{ taskData.task_name }}
    </h1>
    <div class="flex flex-wrap gap-4 ">
      <!-- portfolio part -->
      <div
        class="border border-surface-200 p-4 rounded flex flex-col gap-2"
      >
        <div>
          <span class="font-bold mr-2">Project Status:</span>
          <Tag
            :value="taskData.project_status"
            :severity="
              getStatusSeverity('project_status', taskData.project_status)
            "
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Task Status:</span>
          <Tag
            :value="taskData.task_status"
            :severity="getStatusSeverity('task_status', taskData.task_status)"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Product Stage:</span>
          <Tag
            :severity="taskData.product_stage >= 'stage_C' ? 'success' : 'warn'"
            :value="taskData.product_stage"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Task Confirmed:</span>
          <Tag
            :value="taskData.task_confirmed ? 'Yes' : 'No'"
            :severity="taskData.task_confirmed ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Tox Gov Approved:</span>
          <Tag
            :value="taskData.tox_gov_approved ? 'Yes' : 'No'"
            :severity="taskData.tox_gov_approved ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">EcoTox Gov Approved:</span>
          <Tag
            :value="taskData.ecotox_gov_approved ? 'Yes' : 'No'"
            :severity="taskData.ecotox_gov_approved ? 'success' : 'warn'"
          ></Tag>
        </div>
      </div>
      <!-- operation part -->
      <div
        class="border border-surface-200 p-4 rounded  flex flex-col gap-2"
      >
        <div>
          <span class="font-bold mr-2">Budget Confirmed:</span>
          <Tag
            :value="taskData.budget_confirmed ? 'Yes' : 'No'"
            :severity="taskData.budget_confirmed ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">PO Placed:</span>
          <Tag
            :value="taskData.po_placed ? 'Yes' : 'No'"
            :severity="taskData.po_placed ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Contract Signed:</span>
          <Tag
            :value="taskData.contract_signed ? 'Yes' : 'No'"
            :severity="taskData.contract_signed ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Payment Status:</span>
          <Tag
            :value="taskData.payment_status"
            :severity="
              getStatusSeverity('payment_status', taskData.payment_status)
            "
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">VV Doc Uploaded:</span>
          <Tag
            :value="taskData.vv_doc_uploaded ? 'Yes' : 'No'"
            :severity="taskData.contract_signed ? 'success' : 'warn'"
          ></Tag>
        </div>
      </div>
      <!-- expert part1 -->
      <div
        class="border border-surface-200 p-4 rounded flex flex-col gap-2"
      >
        <div>
          <span class="font-bold mr-2">Expected Delivery Date:</span>
          <Tag
            :value="toLocalStr(taskData.expected_delivery_date)"
            :severity="
              getDateSeverity(
                taskData.delivery_date,
                taskData.expected_delivery_date
              )
            "
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Expected Finish:</span>
          <Tag
            :value="taskData.expected_finish"
            :severity="
              getDateSeverity(
                taskData.task_progress === 'Finished',
                taskData.expected_finish
              )
            "
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Task Progress:</span>
          <Tag :value="taskData.task_progress"></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Delivered:</span>
          <Tag
            :value="taskData.delivery_date ? 'Yes' : 'No'"
            :severity="taskData.delivery_date ? 'success' : 'warn'"
          ></Tag>
        </div>
      </div>
      <!-- expert part2 -->
      <div
        class="border border-surface-200 p-4 rounded flex flex-col gap-2"
      >
        <div>
          <span class="font-bold mr-2">Study Notified:</span>
          <Tag
            :value="taskData.study_notified ? 'Yes' : 'No'"
            :severity="taskData.study_notified ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">Test Item Data Sheet:</span>
          <Tag
            :value="taskData.test_item_data_sheet ? 'Yes' : 'No'"
            :severity="taskData.test_item_data_sheet ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">SSD Finished:</span>
          <Tag
            :value="taskData.ssd_finished ? 'Yes' : 'No'"
            :severity="taskData.ssd_finished ? 'success' : 'warn'"
          ></Tag>
        </div>
        <div>
          <span class="font-bold mr-2">SED Uploaded:</span>
          <Tag
            :value="taskData.sed_uploaded ? 'Yes' : 'No'"
            :severity="taskData.sed_uploaded ? 'success' : 'warn'"
          ></Tag>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { taskData } = defineProps({ taskData: Object });
import { getStatusSeverity } from "../../composables/fieldTools";
import{toLocalStr} from "../../composables/dateTools";

  function getDateSeverity(precondition, targetDate) {
  if (Boolean(precondition)) {
    return "success";
  } else {
    const target = new Date(targetDate);
    const now = new Date();

    if (target < now) {
      return "danger";
    } else if (target - now <= 30) {
      return "warn";
    } else {
      return "info";
    }
  }
}
</script>
