<template>
  <div>
    <Toolbar class="min-w-100 mb-3">
      <template #start>
        <Button icon="pi pi-plus" label="New" severity="primary" size="small" @click="handleShowCroForm('new', null)" />
      </template>
      <template #end>
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText v-model="filters['global'].value" placeholder="Search Cro"
            v-tooltip="'Search by Name, Scope, Cert Number'" size="small" />
        </IconField>
      </template>
    </Toolbar>

    <DataTable :value="cro_list" v-model:selection="selectedCro" v-model:expandedRows="expandedRows"
      v-model:filters="filters" :globalFilterFields="globalFilterFields" @rowExpand="onRowExpand" scrollable
      selectionMode="single" dataKey="id" resizableColumns columnResizeMode="expand" showGridlines
      tableStyle="min-width: 50rem" size="small">
      <Column expander class="w-12" frozen />
      <Column field="certification_number" header="Cert Number">
        <template #body="{ data, field }">
          <Button :label="data[field]" variant="link" @click="handleShowCroForm('edit', data)"
            class="px-0 text-left"></Button>
        </template>
      </Column>
      <Column field="cro_name" header="CRO Name"></Column>
      <Column field="certification_expiration_date" header="Expiration">
        <template #body="{ data, field }">
          {{ toLocalStr(data[field]) }}</template>
      </Column>
      <Column field="certification_scope" header="Scope" class="w-20"></Column>
      <Column field="fw_contract_start" header="Fw Contract Start"><template #body="{ data, field }">
          {{ toLocalStr(data[field]) }}</template></Column>
      <Column field="fw_contract_end" header="Fw Contract End"><template #body="{ data, field }">
          {{ toLocalStr(data[field]) }}</template></Column>
      <Column field="fw_contract_detail" header="Fw Contract Detail"></Column>
      <Column field="address" header="Address"></Column>

      <template #expansion="{ data }">
        <div class="mt-4 flex flex-col gap-4 rounded" @click="selectedCro = data">
          <!-- <p class="font-bold">Contacts</p> -->
          <div class="flex gap-4 items-center">
            <p class="text-xl">Contacts</p>
            <Button icon="pi pi-plus" rounded variant="outlined"
              @click="handleShowContactForm('new', data.id)"></Button>
            <Button icon="pi pi-pencil" rounded variant="outlined" v-if="selectedContact?.cro_id === data.id"
              @click="handleShowContactForm('edit', data.id)"></Button>
            <Button icon=" pi pi-trash" rounded variant="outlined" v-if="selectedContact?.cro_id === data.id"
              @click="handleDeleteContact(data)"></Button>
          </div>

          <DataTable :value="data.contacts" dataKey="id" scrollable scrollHeight="flex" selectionMode="single"
            v-model:selection="selectedContact" showGridlines resizableColumns columnResizeMode="expand">
            <Column selectionMode="single" class="w-8"></Column>
            <Column field="contact_name" header="Contact Name"></Column>
            <Column field="discipline" header="Discipline"></Column>
            <Column field="phone_number" header="phone_number"></Column>
            <Column field="email" header="email"></Column>
            <Column field="remarks" header="remarks"></Column>

            <template #empty>
              <p class="text-center text-primary">No Contacts Found!</p>
            </template>
          </DataTable>
        </div>
      </template>

      <template #empty>
        <p class="text-center text-primary">No Cros Found!</p>
      </template>
    </DataTable>
    <CroForm v-if="showCroForm" :initialFormData="initialCro" @close="showCroForm = false" @refresh="handleRefreshCro">
    </CroForm>

    <ContactForm v-if="showContactForm" :croId="targetCroID" :initialFormData="initialContact"
      @close="showContactForm = false" @refresh="handleRefreshContact"></ContactForm>
  </div>
</template>

<script setup>
  import CroForm from "./CroForm.vue";
  import ContactForm from "./ContactForm.vue";
  import { onMounted, ref, inject } from "vue";
  import { FilterMatchMode } from "@primevue/core/api";
  import { toLocalStr } from "../../composables/dateTools";
  // import { useErrorStore } from "../../stores/errorStore";
  import useApi from "@/composables/useApi";;
  const Api = inject("Api")
  const cro_list = ref([]);
  const expandedRows = ref([]);

  // cro form use
  const selectedCro = ref();
  const showCroForm = ref(false);
  let croFormHeaderText = "";
  let initialCro = null;
  // contact form use
  const selectedContact = ref();
  const showContactForm = ref(false);
  let contactFormHeaderText = "";
  let initialContact = null;
  const targetCroID = ref();

  const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  });
  const globalFilterFields = ["certification_number", "cro_name", "scope"];

  onMounted(async () => {
    cro_list.value = await Api.get("/cros/");
  });

  async function onRowExpand(event) {
    event.data.contacts = await Api.get(`cros/${event.data.id}/contacts`);
  }

  async function handleShowCroForm(mode, data) {
    initialCro = mode === "new" ? {} : data;
    showCroForm.value = true;
  }

  function handleShowContactForm(mode, cro_id) {
    initialContact = mode === "new" ? {} : selectedContact.value;
    targetCroID.value = cro_id;
    showContactForm.value = true;
  }

  import { useConfirm } from "primevue/useconfirm";
  const confirm = useConfirm();
  async function handleDeleteContact(data) {



    confirm.require({
      message: "Are you sure you want to delete this contact?",
      header: "Delete Confirmation",
      icon: "pi pi-exclamation-triangle",
      acceptLabel: "Yes",
      rejectLabel: "No",
      acceptClass: "p-button-danger",
      accept: async () => {
        Api.delete(`cros/contacts/${selectedContact.value.id}`);
        data.contacts.splice(
          data.contacts.findIndex((obj) => (obj.id === selectedContact.value.id)),
          1
        );
        selectedContact.value = null;
      },
    });

    // await Api.delete(`cros/contacts/${selectedContact.value.id}`);
    // data.contacts = await Api.get(`cros/${data.id}/contacts`);
    // selectedContact.value = null;
  }

  async function handleRefreshContact(newData) {
    let cro_index = cro_list.value.findIndex((obj) => (obj.id === newData.cro_id));
    let contact_index = cro_list.value[cro_index].contacts.findIndex(
      (obj) => (obj.id === newData.id)
    );

    if (contact_index == -1) {
      cro_list.value[cro_index].contacts.push(newData);
    } else {
      cro_list.value[cro_index].contacts[contact_index] = newData;
    }
  }

  async function handleRefreshCro(newData) {
    let index = cro_list.value.findIndex((obj) => (obj.id = newData.id));
    if (index == -1) {
      cro_list.value[index].push(newData);
    } else {
      cro_list.value[index] = newData;
    }
  }
</script>

<style module></style>
