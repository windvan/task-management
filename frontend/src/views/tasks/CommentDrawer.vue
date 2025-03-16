<template>
  <Drawer
    v-model:visible="visible"
    position="right"
    class="w-[40rem]">
    <template #header>
      <div class="flex items-center gap-2">
        <span class="font-bold">header="Task Comments"</span>
      </div>
    </template>

    <template #footer>
      <div class="flex items-center gap-2">
        <Button
          label="Account"
          icon="pi pi-user"
          class="flex-auto"
          outlined></Button>
        <Button
          label="Logout"
          icon="pi pi-sign-out"
          class="flex-auto"
          severity="danger"
          text></Button>
      </div>
    </template>
    <pre>{{ currentTask }}</pre>
  </Drawer>
</template>
