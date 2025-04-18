<template>
  <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
    <template #header>
      <p class="font-bold text-lg">
        {{ formMode === "edit" ? "Edit CRO" : "Add CRO" }}
      </p>
      <div class="flex gap-4">
        <Button type="submit" form="croForm" icon="pi pi-save" label="Save" />
        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form pt:root:id="croForm" :resolver="resolver" @submit="handleSave" :initialValues="initialFormData"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32">
      <FormField v-slot="$field" name="cro_name" class="form-field">
        <label for="cro_name" class="required-mark">CRO Name</label>
        <InputText id="cro_name" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="certification_number" class="form-field">
        <label for="certification_number" class="required-mark">Certification Number</label>
        <InputText id="certification_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="certification_expiration_date" class="form-field">
        <label for="certification_expiration_date" class="required-mark">Expiration Date</label>
        <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="certification_scope" class="form-field">
        <label for="certification_scope" class="required-mark">Certification Scope</label>
        <InputText id="certification_scope"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="fw_contract_start" class="form-field">
        <label for="fw_contract_start">FW Contract Start</label>
        <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="fw_contract_end" class="form-field">
        <label for="fw_contract_end">FW Contract End</label>
        <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="fw_contract_detail" class="form-field">
        <label for="fw_contract_detail">FW Contract Detail</label>
        <InputText id="fw_contract_detail"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="address" class="form-field">
        <label for="address">Address</label>
        <InputText id="address"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
    </Form>
  </Dialog>
</template>

<script setup>
  import { inject, ref } from "vue";
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";
  import useApi from "@/composables/useApi";;
  const Api = inject("Api")

  const { initialFormData } = defineProps({ initialFormData: Object });
  const emit = defineEmits(["refresh", "close"]);

  const formMode = initialFormData.id ? "edit" : "new";

  const visible = ref(true);


  const resolver = yupResolver(
    yup.object().shape({
      cro_name: yup.string().required(),
      certification_number: yup.string().required(),
      certification_expiration_date: yup.date().required(),
      certification_scope: yup.string().required(),
    })
  );

  async function handleSave(e) {
    if (!e.valid) return;

    let updatedFields = {};
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        // sepcial handling for special field types if needed
        updatedFields[field] = state.value;
      }
    });

    // update cro
    let newData
    if (formMode === "edit") {
      newData = await Api.patch(`/cros/${initialFormData.id}/`, updatedFields);
    } else {
      // new mode
      newData = await Api.post("/cros/", updatedFields);
    }
    emit('close');
    emit("refresh", newData);
  }

  function handleCancel() {
    visible.value = false;
  }
</script>
