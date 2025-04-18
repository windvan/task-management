<template>
  <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
    <template #header>
      <p class="font-bold text-lg">{{ props.header }}</p>
      <div class="flex gap-4">
        <Button type="submit" form="sampleForm" icon="pi pi-save" label="Save" />
        <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
      </div>
    </template>
    <Form pt:root:id="sampleForm" :resolver="resolver" @submit="handleSave" :initialValues="props.initialFormData"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32">
      <FormField v-slot="$field" name="product" class="form-field">
        <label for="product" class="required-mark">Product Name</label>
        <AutoComplete inputId="product" dropdown optionLabel="internal_name" :suggestions="productSuggestions"
          @complete="filterProductSuggestion" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="sample_name" class="form-field">
        <label for="sample_name" class="required-mark">Sample Name</label>
        <InputText id="sample_name"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="sample_status" class="form-field">
        <label for="sample_status" class="required-mark">Sample Status</label>
        <Select inputId="sample_status" :options="enums?.SampleStatusEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="sample_quantity" class="form-field">
        <label for="sample_quantity">Sample Quantity</label>
        <InputText id="sample_quantity"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="batch_number" class="form-field">
        <label for="batch_number">Batch Number</label>
        <InputText id="batch_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="sealing_number" class="form-field">
        <label for="sealing_number">Sealing Number</label>
        <InputText id="sealing_number"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="production_date" class="form-field">
        <label>Production Date</label>
        <DatePicker inputId="production_date" showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="expiration_date" class="form-field">
        <label>Expiratioin Date</label>
        <DatePicker inputId="expiration_date" showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="shipped_quantity" class="form-field">
        <label for="shipped_quantity">Shipped Quantity</label>
        <InputText id="shipped_quantity"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="receiver_information" class="form-field">
        <label for="receiver_information">Receiver Information</label>
        <InputText id="receiver_information"></InputText>
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

  const props = defineProps({ header: String, initialFormData: Object });
  const visible = ref(true);
  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  // const toast = useToast()

  const emit = defineEmits(["refresh", "close"]);

  const productSuggestions = ref([]);
  async function filterProductSuggestion(event) {
    productSuggestions.value = await Api.get(
      `/products/search?query=${event.query}`
    );
    // if (query.length === 0) {
    //     productSuggestions.value = Api.get('/products/')
    // } else {
    //     productSuggestions.value = Api.get(`/products?search=${query}`)
    // }
  }

  const expandedRowGroups = ref(null);
  const tableError = ref("");
  const selectedNodes = ref(null);

  const resolver = yupResolver(
    yup.object().shape({
      product: yup.object().required(),
      sample_name: yup.string().required(),
      sample_status: yup.string().required(),
    })
  );

  async function handleSave(e) {
    if (!e.valid) return;

    let updatedFields = {};
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        if (field === 'product') {
          // for date fields
          updatedFields['product_id'] = state.value.id;
        } else {
          // for string and select field
          updatedFields[field] = state.value;
        }
      }
    });

    // update cro

    if (props.initialFormData) {
      // edit mode
      await Api.patch(`/samples/${props.initialFormData.id}`, updatedFields);
    } else {
      // new mode
      await Api.post("/samples/", updatedFields);
    }
    visible.value = false;
    emit("refresh");
  }

  function handleCancel() {
    visible.value = false;
  }
</script>
