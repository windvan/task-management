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
          <Button icon="pi pi-user-edit" severity="success" rounded outlined @click="handleEdit(data)" class="mr-4" />
          <Button icon="pi pi-trash" severity="danger" rounded outlined @click="handleDelete(data)" />
        </template>
      </Column>

      <template #empty>
        <p class="text-center text-primary">No Users Found!</p>
      </template>
    </DataTable>

    <Dialog v-model:visible="showUserForm" :style="{ width: '450px' }"
      :header="initialFormData?.id ? 'Update user info' : 'Create new user'" :modal="true">

      <Form id="userForm" @submit="handleSave" :initialValues="initialFormData" :resolver="resolver"
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
          <Select inputId="role" :options="enums.RoleEnum" showClear placeholder="Select a Role" />
          <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
            $field.error?.message
          }}</Message>
        </FormField>

      </Form>


      <template #footer>
        <Button label="Cancel" icon="pi pi-times" severity="secondary" @click="showUserForm = false" />
        <Button label="Save" icon="pi pi-check" type="submit" form="userForm" />
      </template>
    </Dialog>


  </div>
</template>

<script setup>
  import { inject, ref, onMounted, computed, useTemplateRef } from 'vue'
  import { useConfirm } from 'primevue/useconfirm'
  import { useToast } from 'primevue/usetoast'
  import { FilterMatchMode } from '@primevue/core/api'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'


  import useApi from "@/composables/useApi";
  const Api = inject("Api")
  const users = ref([])
  let initialFormData
  const formRef = useTemplateRef("formRef")
  const showUserForm = ref(false)
  const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}

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
      password: initialFormData.id ? yup.string() : yup.string().required()
    })
  ))

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
  })
  const globalFilterFields = ['name', 'email', 'role']

  onMounted(async () => {
    users.value = await Api.get('/users/')
  })

  function handleNew() {
    initialFormData = {}
    showUserForm.value = true
  }

  function handleEdit(currentUser) {
    initialFormData = currentUser
    showUserForm.value = true
  }

  async function handleSave(e) {

    if (!e.valid) return;

    let updatedFields = {};
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        updatedFields[field] = state.value;
      }
    });
    let newData
    if (initialFormData.id) {
      newData = await Api.patch(`/users/${initialFormData.id}`, updatedFields)
    } else {
      newData = await Api.post('/users', updatedFields)
    }

    const index = users.value.findIndex(user => user.id === newData.id)
    if (index == -1) {

      users.value.push(newData);

    } else {
      // tasks.value.splice(index, 1, newData);
      users.value[index] = newData;

    }

    showUserForm.value = false



  }


  function handleDelete(data) {
    confirm.require({
      
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

    })
  }

  async function deleteUser(user_id) {

    try {
      let response
      // delete user
      response = await Api.delete(`/users/${user_id}`)

      // refresh users
      response = await Api.get('/users')
      users.value = response.data
    } catch (err) {
      toast.add({ severity: 'error', summary: 'Error', detail: err.message })
    }
  }

</script>
