<template>
  <div>
    <DataTable :value="items" editMode="row" @row-edit-save="onRowEditSave" v-model:editingRows="editingRows">
      <Column field="name" header="名称">
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" />
        </template>
      </Column>
      <Column field="image" header="图片">
        <template #body="slotProps">
          <ImageUploader v-model="slotProps.data.image" />
        </template>
      </Column>
      <Column :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
    </DataTable>
    <Button label="保存所有更改" @click="saveAllChanges" />
    <FileUpload
          accept="image/*"
          :maxFileSize="1048576"
          :pt="{ root: 'flex', header: 'p-2', content: 'p-2' }"
        >
          <template #header="{ chooseCallback }">
            <Button icon="pi pi-upload" rounded class="size-8" @click="chooseCallback" />
          </template>
          <template #content="{ files }">
            <img
              :src="files[0]?.objectURL"
              :title="files[0]?.name"
              tabindex="0"
              @keyup.delete="files.splice(0, 1)"
              class="max-w-12 items-center cursor-pointer rounded focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            /> </template>
        </FileUpload>
  </div>

  
</template>

<script>
import { ref } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import ImageUploader from './ImageUploader.vue';

export default {
  components: {
    DataTable,
    Column,
    InputText,
    Button,
    ImageUploader
  },
  setup() {
    const items = ref([
      { id: 1, name: '项目1', image: '' },
      { id: 2, name: '项目2', image: '' },
      { id: 3, name: '项目3', image: '' },
    ]);
    const editingRows = ref([]);

    const onRowEditSave = (event) => {
      // 处理单行编辑保存
      console.log('Row edited:', event.data);
    };

    const saveAllChanges = () => {
      // 实现保存所有更改的逻辑
      console.log('Saving all changes:', items.value);
      // 这里可以发送 API 请求来保存数据
    };

    return {
      items,
      editingRows,
      onRowEditSave,
      saveAllChanges
    };
  }
};
</script>