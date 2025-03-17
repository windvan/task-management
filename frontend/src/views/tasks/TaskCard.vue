<template>
  <div class="border rounded-xl">
    <div>
      <span class="font-bold mr-2">Product Stage:</span>
      <Tag
        :severity="taskData.product_stage >= 'stage_C' ? 'success' : 'warn'"
        :value="taskData.product_stage"
      ></Tag>
    </div>

    <div>
      <span class="font-bold mr-2">Project Status:</span>
      <Tag
        :severity="getStatusSeverity(taskData.project_status)"
        :value="taskData.project_status"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Tox Gov Approved:</span>
      <Tag
        :value="taskData.tox_gov_approved"
        :severity="taskData.tox_gov_approved ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">EcoTox Gov Approved:</span>
      <Tag
        :value="taskData.ecotox_gov_approved"
        :severity="taskData.ecotox_gov_approved ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Budget Confirmed:</span>
      <Tag
        :value="taskData.budget_confirmed"
        :severity="taskData.budget_confirmed ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">PO Placed:</span>
      <Tag
        :value="taskData.po_placed"
        :severity="taskData.po_placed ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Contract Signed:</span>
      <Tag
        :value="taskData.contract_signed"
        :severity="taskData.contract_signed ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Task Confirmed:</span>
      <Tag
        :value="taskData.task_confirmed"
        :severity="taskData.task_confirmed ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Expected Delivery Date:</span>
      <Tag :value="taskData.expected_delivery_date"></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Task Status:</span>
      <Tag :value="taskData.task_status"></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Task Progress:</span>
      <Tag :value="taskData.task_progress"></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Expected Finish:</span>
      <Tag :value="taskData.expected_finish"></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Test Item Data Sheet:</span>
      <Tag
        :value="taskData.test_item_data_sheet"
        :severity="taskData.test_item_data_sheet ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">SSD Finished:</span>
      <Tag
        :value="taskData.ssd_finished"
        :severity="taskData.ssd_finished ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">SED Uploaded:</span>
      <Tag
        :value="taskData.sed_uploaded"
        :severity="taskData.sed_uploaded ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Study Notified:</span>
      <Tag
        :value="taskData.study_notified"
        :severity="taskData.study_notified ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Delivered:</span>
      <Tag
        :value="taskData.delivery_date ? 'Yes' : 'No'"
        :severity="taskData.delivery_date ? 'success' : 'warn'"
      ></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">Payment Status:</span>
      <Tag :value="taskData.payment_status"></Tag>
    </div>
    <div>
      <span class="font-bold mr-2">VV Doc Uploaded:</span>
      <Tag
        :value="taskData.vv_doc_uploaded"
        :severity="taskData.contract_signed ? 'success' : 'warn'"
      ></Tag>
    </div>
  </div>
</template>

<script setup>
const { taskData } = defineProps({ taskData: Object });
function getStatusSeverity(status) {
  switch (status) {
    case "Idea_Stage":
      return "secondary";
    case "Active":
      return "info";
    case "Finished":
      return "success";
    case "Terminated":
      return "warn";
    default:
      return "primary"; // 或者其他默认值
  }
}
</script>
