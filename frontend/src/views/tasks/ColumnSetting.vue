<template>
  <Popover ref="poRef" @show="onPopoverShow" pt:content="flex flex-col gap-4">
    <div class="flex gap-8 justify-center">
      <Button label="Apply" icon="pi pi-check" variant="outlined" size="small" @click="onApply"></Button>
      <Button label="Cancel" icon="pi pi-times" severity="secondary" size="small" @click="onCancel"></Button>
      <Button label="Default" icon="pi pi-undo" severity="secondary" size="small" @click="onDefault"></Button>
    </div>
    <PickList v-model="columnPicker" breakpoint="800px" scroll-height="20rem">
      <template #option="{ option }">
        {{ option.col }}
      </template>
      <template #sourceheader>
        <span class="font-bold">All Columns</span>
        <hr />
      </template>
      <template #targetheader>
        <span class="font-bold">Selected Columns</span>
        <hr />
      </template>
    </PickList>
    <div class="flex items-center gap-2">
      <Checkbox v-model="rememberSelection" binary inputId="remember" size="small" />
      <label for="remember"> Remember my selection</label>
    </div>
  </Popover>
</template>

<script setup>
  import { inject, onMounted, useTemplateRef } from 'vue';
  const poRef = useTemplateRef('poRef')
  const Api = inject("Api")

  const { visibleTaskColumns } = defineProps({ visibleTaskColumns: Array })

  let allTaskColumns
  // const visibleTaskColumns = ref(JSON.parse(localStorage.getItem("visibleTaskColumns")) ?? allTaskColumns)


  onMounted(async () => {
    let allFields= await Api.get('/tasks/task-columns')

    allTaskColumns = allFields.filter((field => !field.endsWith("id")))

    poRef.value.show()
  })


</script>