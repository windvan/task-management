<template>
  <div>
    <DataTable :value="users" dataKey="id" resizableColumns v-model:filters="filters"
      :globalFilterFields="globalFilterFields" pt:header="px-0" tableStyle="min-width: 50rem">
      <template #header>
        <Toolbar>
          <template #start>
            <Button icon="pi pi-plus" label="New" severity="primary" @click="handleNew" />
          </template>

          <template #end>
            <IconField>
              <InputIcon>
                <i class="pi pi-search" />
              </InputIcon>
              <InputText placeholder="Search" v-model="filters['global'].value" />
            </IconField>
          </template>
        </Toolbar>
      </template>

      <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header"
        :hidden="col.field === 'id'">
      </Column>
      <Column key="action" header="Action" class="text-center" :pt="{ columnTitle: 'mx-auto' }">
        <template #body="{ data }">
          <Button icon="pi pi-user-edit" severity="success" rounded outlined @click="handleEdit(data)" class="mr-4"/>
          <Button icon="pi pi-trash" severity="danger" rounded outlined @click="handleDelete(data)" />
        </template>
      </Column>

      <template #empty>
        <p class="text-center text-primary">No Users Found!</p>
      </template>
    </DataTable>

    <Dialog v-model:visible="showUserForm" :style="{ width: '450px' }"
      :header="initialFormData.id ? 'Update user info' : 'Create new user'" :modal="true">

      <Form ref="formRef" :initialValues="initialFormData" :resolver="resolver"
        class="flex flex-col gap-4 overflow-auto p-4 mb-4">
        <FormField v-slot="$field" name="name" class="form-field">
          <label for="name" class="required-mark">Name</label>
          <InputText id="name"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="email" class="form-field">
          <label for="email" class="required-mark">Email</label>
          <InputText id="email"></InputText>
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="password" class="form-field">
          <label for="password" :class="{ 'required-mark': !initialFormData.id }">
            Password
            <p v-if="initialFormData.id" class="text-primary-300 font-light italic">leave password empty if you don't
              want
              to change password</p>
          </label>

          <Password inputId="password" :feedback="false" toggleMask fluid />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

        <FormField v-slot="$field" name="role" class="form-field">
          <label for="role" class="required-mark">Role</label>
          <Select inputId="role" :options="roleEnum" showClear placeholder="Select a Role" />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

      </Form>


      <template #footer>
        <Button label="Cancel" icon="pi pi-times" severity="secondary" @click="showUserForm = false" />
        <Button label="Save" icon="pi pi-check" @click="handleSave" />
      </template>
    </Dialog>

    <ConfirmDialog></ConfirmDialog>
  </div>
</template>

<script setup>
  import { inject, ref, onMounted, computed, useTemplateRef } from 'vue'
  import { useEnumsStore } from '@/stores/enumsStore'
  import { useConfirm } from 'primevue/useconfirm'
  import { useToast } from 'primevue/usetoast'
  import { FilterMatchMode } from '@primevue/core/api'
  import { FormField } from '@primevue/forms'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'
  import { Password } from 'primevue'


  const $axios = inject('$axios')
  const users = ref([])
  const initialFormData = ref({})
  const formRef = useTemplateRef("formRef")
  const showUserForm = ref(false)


  const roleEnum = useEnumsStore().enums.RoleEnum

  const confirm = useConfirm()
  const toast = useToast()
  const columns = [
    { field: 'name', header: 'Name' },
    { field: 'email', header: 'Email' },
    { field: 'role', header: 'Role' },
    { field: 'id', header: 'Id' }
  ]
  const resolver = computed(() => yupResolver(
    yup.object().shape({
      name: yup.string().required(),
      email: yup.string().email().required(),
      role: yup.string().required(),
      password: initialFormData.value.id ? yup.string() : yup.string().required()
    })
  ))

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
  })
  const globalFilterFields = ['name', 'email', 'role']

  onMounted(async () => {
    try {
      const response = await $axios.get('/users')
      users.value = response.data
    } catch (err) {
      console.error('Failed to fetch users:', err)
    }
  })

  function handleNew() {
    initialFormData.value = {}
    showUserForm.value = true
  }

  function handleEdit(currentUser) {
    initialFormData.value = currentUser
    showUserForm.value = true
  }

  async function handleSave() {
    const { values, errors } = await formRef.value.validate()

    if (Object.keys(errors).length !== 0) {
      return
    }

    try {
      let response
      if (initialFormData.value.id) {
        // update user
        response = await $axios.patch(`/users/${initialFormData.value.id}`, values)
        response = await $axios.get('/users')
        users.value=response.data
        showUserForm.value = false

        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: response.data.message,
          life: 3000
        })
      } else {
        // add new user
        response = await $axios.post('/users', values)
        response = await $axios.get('/users')
        users.value=response.data
        showUserForm.value = false
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: response.data.message,
          life: 3000
        })
      }
    } catch (err) {
      console.log(err)
      toast.add({ severity: 'error', summary: 'Error', detail: 'Add User Failed!' })
    }
  }


  function handleDelete(data) {
    confirm.require({
      position: 'top-center',
      message: 'Do you want to delete this record?',
      header: 'Deletion Confirm',
      icon: 'pi pi-info-circle',
      // rejectLabel: 'Cancel',
      rejectProps: {
        label: 'Cancel',
        severity: 'secondary',
        outlined: true
      },
      acceptProps: {
        label: 'Delete',
        severity: 'danger'
      },
      accept: async () => { await deleteUser(data.id) },
      reject: () => { }
    })
  }

  async function deleteUser(user_id) {

    try {
      let response
      // delete user
      response = await $axios.delete(`/users/${user_id}`)

      // refresh users
      response = await $axios.get('/users')
      users.value = response.data
    } catch (err) {
      toast.add({ severity: 'error', summary: 'Error', detail: err.message })
    }
  }

</script>

<style module></style>
