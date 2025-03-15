<template>
  <Popover ref="poRef" pt:content="flex flex-col gap-4" @hide="handleHide">
    <div class="flex gap-8 justify-start items-center  mx-4">
      <Button
        label="Apply"
        icon="pi pi-check"
        variant="outlined"
        size="small"
        @click="onApply"></Button>

      <Button
        label="Default"
        icon="pi pi-undo"
        severity="secondary"
        size="small"
        @click="onDefault"></Button>

      <Button
        label="All"
        icon="pi pi-angle-double-right"
        severity="secondary"
        size="small"
        @click="onSelectAll"></Button>

      <p class="ml-auto text-primary">
        {{ selectedColumns.length }}/{{ columnFieldMap.size }} selected
      </p>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 h-96 overflow-auto">
      <div
        v-for="[col, field] in columnFieldMap.entries()"
        :key="field"
        class="flex items-center gap-2 bg-gray-100 rounded-md p-2">
        <Checkbox v-model="selectedColumns" :inputId="field" :value="col" />
        <label :for="field" class="flex-1">{{ col }}</label>
      </div>
    </div>
  </Popover>
</template>

<script setup>
  import {
    inject,
    onMounted,
    useTemplateRef,
    ref,
    onBeforeMount,
    computed,
  } from "vue";

  const poRef = useTemplateRef("poRef");
  const Api = inject("Api");

  const { visibleTaskColumns, defaultTaskColumns } = defineProps({
    visibleTaskColumns: Object,
    defaultTaskColumns: Object,
  });
  const emit = defineEmits(["cancel", "apply"]);

  // selectedColumns is an array of column names
  const selectedColumns = ref(Object.values(visibleTaskColumns ?? {}));

  const columnFieldMap = new Map([
    ["Project Name", "project_name"],
    ["Task Name", "task_name"],
    ["Tags", "tags"],
    ["Task Owner Name", "task_owner_name"],
    ["Task Confirmed", "task_confirmed"],
    ["Task Status", "task_status"],
    ["Start Year", "start_year"],
    ["Expected Delivery Date", "expected_delivery_date"],
    ["PI Number", "pi_number"],
    ["TK Number", "tk_number"],
    ["Tox Gov Approved", "tox_gov_approved"],
    ["EcoTox Gov Approved", "ecotox_gov_approved"],

    ["Project Id", "project_id"],
    ["Task Category", "task_category"],
    ["Task Owner Id", "task_owner_id"],
    ["Gap Id", "gap_id"],
    ["Cost Center", "cost_center"],
    ["Budget Confirmed", "budget_confirmed"],
    ["Doc Link", "doc_link"],
    ["Actual Cost", "actual_cost"],
    ["PO Placed", "po_placed"],
    ["Contract Signed", "contract_signed"],
    ["Payment Method", "payment_method"],
    ["Payment Status", "payment_status"],
    ["VV Doc Uploaded", "vv_doc_uploaded"],
    ["VV Doc Number", "vv_doc_number"],

    ["Planned Start", "planned_start"],
    ["Expected Finish", "expected_finish"],
    ["Actual Start", "actual_start"],
    ["Actual Finish", "actual_finish"],
    ["Delivery Date", "delivery_date"],
    ["Stuff Days", "stuff_days"],
    ["Task Progress", "task_progress"],
    ["Crop", "crop"],
    ["Target", "target"],
    ["Cro Id", "cro_id"],
    ["Sample Id", "sample_id"],
    ["Study Notified", "study_notified"],
    ["Estimated Cost", "estimated_cost"],
    ["Analytes", "analytes"],
    ["Key Results", "key_results"],
    ["Guidelines", "guidelines"],
    ["Test Item Data Sheet", "test_item_data_sheet"],
    ["SSD Finished", "ssd_finished"],
    ["SED Uploaded", "sed_uploaded"],
    ["Global Study Manager", "global_study_manager"],
    ["Global Study Manager Email", "global_study_manager_email"],
    ["CRO Study Director", "cro_study_director"],
    ["Id", "id"],

    ["CRO Name", "cro_name"],
    ["Gap Snapshot Url", "gap_snapshot_url"],
    ["Sample Status", "sample_status"],
    ["Created At", "created_at"],
    ["Created By", "created_by"],
  ]);

  // 暴露方法给父组件
  defineExpose({
    toggle: (event) => poRef.value?.toggle(event),
  });

  const onApply = () => {
    // update visibleTaskColumns in TaskView

    // convert selectedColumns to field_col map
    const _selectedColumns = selectedColumns.value.reduce((acc, col) => {
      acc[columnFieldMap.get(col)] = col;
      return acc;
    }, {});

    emit("apply", _selectedColumns);
  };

  const onDefault = () => {
    selectedColumns.value = Object.values(defaultTaskColumns);
  };

  const onSelectAll = () => {
    selectedColumns.value = [...columnFieldMap.keys()];
  };
  const handleHide = () => {
    emit("cancel");
  };
</script>
