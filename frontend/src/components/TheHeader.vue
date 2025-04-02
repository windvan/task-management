<template>
  <header class="bg-white h-16 flex align-middle justify-between px-4 shadow-sm sticky top-0 left-0">
    <div class="flex items-center gap-8">
      <span class="text-primary font-bold text-xl">Logo Here</span>
      <Button icon="pi pi-bars" rounded severity="secondary" class="size-8" iconClass="size-4"
        @click="emit('toggle')"></Button>
    </div>
    <div class="flex items-center gap-4">
      <Button icon="pi pi-bell" rounded severity="secondary" class="size-8" iconClass="size-4"
        @click="toggleNc"></Button>
      <Button icon="pi pi-envelope" rounded severity="secondary" class="size-8" iconClass="size-4"
        @click="toggleMc"></Button>

      <Button :label="current_user.name" severity="secondary" class="h-8" rounded @click="toggleUc">
        <span class="pi pi-user text-primary"></span>
        <span class="user-name">{{ current_user.name }}</span>
      </Button>


      <Popover ref="ucRef" appendTo="self" class="popover">
        <Button icon="pi pi-sign-out" label="logout" severity="secondary" class="h-8" @click="logout"></Button>
      </Popover>

      <MessageCenter ref="mcRef" v-if="showMc"></MessageCenter>
      <NotificationCenter ref="ncRef" v-if="showNc"></NotificationCenter>
    </div>
  </header>
</template>

<script setup>
  import { nextTick, useTemplateRef, ref } from "vue"
  import { useAuthStore } from "@/stores/authStore";
  import MessageCenter from "./MessageCenter.vue";
  import NotificationCenter from './NotificationCenter.vue'

  const { current_user, logout } = useAuthStore()
  const emit = defineEmits(['toggle'])

  // #region user center
  const ucRef = useTemplateRef('ucRef')
  function toggleUc(event) {
    ucRef.value.toggle(event)
  }

  // #endregion user center


  // #region message center
  const mcRef = useTemplateRef('mcRef')
  const showMc = ref(false)
  async function toggleMc(event) {
    if (showMc.value) {
      // mcRef.value.toggle(event)
      showMc.value = !showMc.value
    } else {
      showMc.value = !showMc.value
      await nextTick()
      mcRef.value.toggle(event)
    }

  }

  // #region message center

  // #region notification center
  const ncRef = useTemplateRef('ncRef')
  const showNc = ref(false)
  async function toggleNc(event) {
    if (showNc.value) {
      // mcRef.value.toggle(event)
      showNc.value = !showNc.value
    } else {
      showNc.value = !showNc.value
      await nextTick()
      ncRef.value.toggle(event)
    }
  }
  // #endregion nitification center

</script>

<style module></style>
