<template>
  <Dialog v-model:visible="dialogVisible" :style="{ width: '900px' }" :modal="true" maximizable @hide="emit('close')">
    <template #header>
      <p class="font-bold text-lg">
        {{ initialFormData.id ? "Edit Product" : "Create Product" }}
      </p>
      <div class="flex gap-4">
        <Button icon="pi pi-save" label="Save" type="submit" form="productForm" />
        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form :resolver="resolver" :initialValues="initialFormData" :validateOnValueUpdate="true" id="productForm"
      @submit="handleSave" class="flex flex-col gap-4 overflow-auto p-4 mb-32">
      <FormField v-slot="$field" name="internal_name" class="form-field">
        <label for="internal_name" class="required-mark">Internal Name</label>
        <InputText id="internal_name"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="lead_ai" class="form-field">
        <label for="lead_ai" class="required-mark">Lead AI</label>
        <InputText id="lead_ai"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="stage" class="form-field">
        <label for="stage" class="required-mark">Stage</label>
        <Select inputId="stage" :options="enums.StageEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="a_number" class="form-field">
        <label for="a_number">A Number</label>
        <InputText id="a_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="product_name" class="form-field">
        <label for="product_name">Product Name</label>
        <InputText id="product_name"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="product_name_cn" class="form-field">
        <label for="product_name_cn">Product Name (CN)</label>
        <InputText id="product_name_cn"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="trade_name" class="form-field">
        <label for="trade_name">Trade Name</label>
        <InputText id="trade_name"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="product_origin" class="form-field">
        <label for="product_origin">Product Origin</label>
        <InputText id="product_origin"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="is_three_new" class="form-field">
        <label for="is_three_new">Three-New</label>
        <RadioButtonGroup class="flex gap-4 p-inputtext p-component">
          <RadioButton inputId="is_three_new_true" :value="true" />
          <label for="is_three_new_true">Yes</label>

          <RadioButton inputId="is_three_new_false" :value="false" />
          <label for="is_three_new_false">No</label>
        </RadioButtonGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
    </Form>
  </Dialog>
</template>

<script setup>
  import { toRefs, useTemplateRef, ref, inject } from "vue";
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";
  import { useToast } from "primevue/usetoast";

  import useApi from "@/composables/useApi";;
  const Api = inject("Api")
  const toast = useToast();
  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};

  const dialogVisible = ref(true);
  const { initialFormData } = defineProps({ initialFormData: Object });

  const emit = defineEmits(["close", "refresh"]);


  //yup resolver: (values,[names])=>{}->errors:obj
  const resolver = yupResolver(
    yup.object().shape({
      internal_name: yup.string().required(),
      lead_ai: yup.string().required(),
      stage: yup.string().required(),
    })
  );

  async function handleSave(event) {
    // only post modified form fields
    //form filed values are matained by primevue Form, no need to bind to a ref or reactive

    if (!event.valid) return;
    // distinguish add and patch through formData.id (Undefined == add)

    // modify current porduct
    let updatedFields = {};
    Object.entries(event.states).forEach(([field, state]) => {
      if (state.dirty) {

        updatedFields[field] = state.value;

      }
    });

    if (Object.keys(updatedFields).length === 0) {
      return;
    }

    let newData;
    if (initialFormData.id) {
      // edit product
      newData = await Api.patch(`/products/${initialFormData.id}`, updatedFields);
    } else {
      // add new product
      newData = await Api.post("/products", updatedFields);
    }
    // close dialog form
    emit("close");
    //refresh data
    emit("refresh", newData);
  }

  function handleCancel() {
    emit("close");
  }
</script>
