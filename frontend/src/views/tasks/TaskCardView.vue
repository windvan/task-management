<template v-if="layout === 'grid'">
  <SelectButton v-model="layout" :options="['list', 'grid']" :allowEmpty="false">
    <template #option="{ option }">
      <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
    </template>
  </SelectButton>
  <TaskCard v-for="task of tasks" :key="task.id" :task-data="task"></TaskCard>
</template>