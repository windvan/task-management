<template>
  <div>
    <Toolbar class="min-w-100 mb-3">
      <template #start>
        <Button icon="pi pi-plus" label="New" severity="primary" size="small" @click="openNew" />
      </template>
      <template #end>
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText placeholder="Search" size="small" />
        </IconField>
      </template>
    </Toolbar>

    <DataTable :value="cro_list" resizableColumns
      showGridlines
      tableStyle="min-width: 50rem"
      size="small">
      <Column field="certification_number" header="Cert Number"></Column>
      <Column field="Cro_name" header="CRO Name"></Column>
      <Column field="certification_expiration_date" header="Expiration"></Column>
      <Column field="certification_scope" header="Scope"></Column>
      <Column field="fw_contract_start" header="Fw Contract Start"></Column>
      <Column field="fw_contract_end" header="Fw Contract End"></Column>
      <Column field="fw_contract_detail" header="Fw Contract Detail"></Column>
      <Column field="address" header="Address"></Column>


    </DataTable>

    <div>
      <p>Contacts</p>
      <DataTable></DataTable>

    </div>

  </div>
</template>

<script setup>
  import { onMounted, ref ,inject} from 'vue';
   const api = inject('api')

  const cro_list=ref([])

  onMounted(async () => {
   
  try {
    const response = await api.get('/cros/cros');
    // 处理成功响应
    cro_list.value = response.data
    
    console.log(response.data);
  } catch (error) {
    // 处理错误
    console.error('An error occurred:', error);
  }
}
  )


</script>

<style module>

</style>
