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

      <Button :label="current_user.name" severity="secondary" size="small" rounded @click="toggleUc">
        <span class="pi pi-user text-primary"></span>
        <span class="user-name">{{ current_user.name }}</span>
      </Button>


      <Popover ref="ucRef" appendTo="body" class="popover" pt:content="flex flex-col gap-2 text-left">
        <Button icon="pi pi-sign-out" label="Logout" severity="secondary" size="small" @click="logout"
          class=" justify-start"></Button>
        <Button icon="pi pi-lock" label="Change Password" severity="secondary" size="small"
          @click="showChangePassword = true" class=" justify-start"></Button>
      </Popover>
      <Dialog v-model:visible="showChangePassword" header="Change Password" :style="{ width: '500px' }" :modal="true"
        maximizable @hide="handleCloseSettings">

        <Form id="changePasswordForm" :resolver="resolver" @submit="handleChangePassword" class="flex flex-col gap-4">
          <FormField v-slot="$field" name="old_password" class="form-field">
            <label for="old_password" class="required-mark">Old Password</label>
            <InputText id="old_password" type="password" />
            <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="new_password" class="form-field">
            <label for="new_password" class="required-mark">New Password</label>
            <InputText id="new_password" type="password" />
            <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="confirm_password" class="form-field">
            <label for="confirm_password" class="required-mark">Confirm Password</label>
            <InputText id="confirm_password" type="password" />
            <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
            </Message>
          </FormField>

          <div class="flex gap-4">
            <Button type="submit" icon="pi pi-save" label="Save" />
            <Button icon="pi pi-times" label="Cancel" @click="showChangePassword = false" />
          </div>
        </Form>

      </Dialog>


      <Settings v-if="showSettings" @close="handleCloseSettings"></Settings>


      <NotificationCenter ref="ncRef" v-if="showNc" @close="toggleNc"></NotificationCenter>

    </div>
  </header>
</template>

<script setup>
  import { nextTick, useTemplateRef, ref, onMounted, inject, onUnmounted } from "vue"
  import { useAuthStore } from "@/stores/authStore";
  import Settings from "./Settings.vue";
  import { useNotificationStore } from "../stores/notificationStore";
  import { OverlayBadge } from "primevue";
  import NotificationCenter from "./NotificationCenter.vue";
  const Api = inject('Api')
  // const NotificationCenter = defineAsyncComponent(() =>
  //   import('./NotificationCenter.vue')
  // )

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



  // #region notification center
  const ncRef = useTemplateRef('ncRef')
  const showNc = ref(false)

  onMounted(() => {
    notificationStore.startBackgroundCheck()
  })

  onUnmounted(() => {
    notificationStore.stopBackgroundCheck()
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


  // #region USER CENTER

  const showChangePassword = ref(false)
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";
  const resolver = yupResolver(
    yup.object().shape({
      old_password: yup.string().required('Old password is required'),
      new_password: yup.string().required('New password is required').min(8, 'Password must be at least 8 characters'),
      confirm_password: yup.string().required().test({
        name: "passwords-match",
        test: function (value) {
          return this.parent.new_password === value;
        },
        message: "Password must match",
      }),
    })
  );
  async function handleChangePassword(e) {
    if (!e.valid) return;
 
    await Api.post('/auth/change-password/', e.values)
    showChangePassword.value = false
      
    }
  
  // #endregion USER CENTER

</script>
