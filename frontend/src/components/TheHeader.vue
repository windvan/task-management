<template>
  <header class="bg-white h-16 flex align-middle justify-between px-4 shadow-sm sticky top-0 left-0">
    <div class="flex items-center gap-8">
      <span class="text-primary font-bold text-xl">Logo Here</span>
      <Button icon="pi pi-bars" rounded severity="secondary" class="size-8" iconClass="size-4"
        @click="emit('toggle')"></Button>
    </div>
    <div class="flex items-center gap-4">
      <OverlayBadge severity="danger" v-if="notificationStore.hasNotification">
        <Button icon="pi pi-bell" rounded severity="secondary" class="size-8" iconClass="size-4" @click="toggleNc">
        </Button>
      </OverlayBadge>
      <Button v-else icon="pi pi-bell" rounded severity="secondary" class="size-8" iconClass="size-4" @click="toggleNc">
      </Button>

      <Button icon="pi pi-cog" rounded severity="secondary" class="size-8" iconClass="size-4"
        @click="handleShowSettings"></Button>

      <Button :label="current_user.name" severity="secondary" class="h-8" rounded @click="toggleUc">
        <span class="pi pi-user text-primary"></span>
        <span class="user-name">{{ current_user.name }}</span>
      </Button>


      <Popover ref="ucRef" appendTo="self" class="popover">
        <Button icon="pi pi-sign-out" label="logout" severity="secondary" class="h-8" @click="logout"></Button>
      </Popover>

      <Settings v-if="showSettings" @close="handleCloseSettings"></Settings>

      <Suspense>
        <template #default>
          <NotificationCenter ref="ncRef" v-if="showNc" @close="toggleNc"></NotificationCenter>
        </template>
        <template #fallback>
          <div class=" rounded-full w-2"></div>
        </template>
      </Suspense>
    </div>
  </header>
</template>

<script setup>
  import { nextTick, useTemplateRef, ref, onMounted, defineAsyncComponent } from "vue"
  import { useAuthStore } from "@/stores/authStore";
  import Settings from "./Settings.vue";
  import { useNotificationStore } from "../stores/notificationStore";
  import { OverlayBadge } from "primevue";

  const NotificationCenter = defineAsyncComponent(() =>
    import('./NotificationCenter.vue')
  )

  const notificationStore = useNotificationStore()
  const { current_user, logout } = useAuthStore()
  const emit = defineEmits(['toggle'])

  // #region user center
  const ucRef = useTemplateRef('ucRef')
  function toggleUc(event) {
    ucRef.value.toggle(event)
  }

  // #endregion user center


  // #region settings

  const showSettings = ref(false)
  function handleShowSettings() {
    showSettings.value = true

  }

  function handleCloseSettings() {
    showSettings.value = false
  }

  // #region message center

  // #region notification center
  const ncRef = useTemplateRef('ncRef')
  const showNc = ref(false)

  onMounted(() => {
    notificationStore.startBackgroundCheck()
  })


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
