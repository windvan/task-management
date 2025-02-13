<template>
  <header class="bg-white h-16 flex align-middle justify-between px-4 shadow-sm sticky top-0 left-0">
    <div class="flex items-center gap-8">
      <span class="text-primary font-bold text-xl">Logo Here</span>
      <Button icon="pi pi-bars" rounded severity="secondary" class="size-8" iconClass="size-4" @click="emit('toggle')" ></Button>
    </div>
    <div class="flex items-center gap-4">
      <Button icon="pi pi-bell" rounded severity="secondary" class="size-8" iconClass="size-4"></Button>
      <Button icon="pi pi-envelope" rounded severity="secondary" class="size-8" iconClass="size-4"></Button>

      <Button :label="current_user.name" severity="secondary" class="h-8" rounded @click="toggleUser">
        <span class="pi pi-user text-primary"></span>
        <span class="user-name">{{ current_user.name }}</span>
      </Button>
      

      <Popover ref="op" appendTo="self" class="popover">
        <Button icon="pi pi-sign-out" label="logout" severity="secondary" class="h-8" @click="logout"></Button>
      </Popover>
    </div>
  </header>
</template>

<script setup>
  import { useTemplateRef } from "vue"
  import { useAuthStore } from "@/stores/authStore";

  const { current_user, logout } = useAuthStore()
  const emit = defineEmits(['toggle'])
  const op = useTemplateRef('op')
  function toggleUser(event) {
    op.value.toggle(event)
  }

</script>

<style module>


</style>
