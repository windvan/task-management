<template>
  <Dialog v-model:visible="visible" :style="{ width: '900px' }" :modal="true" maximizable @hide="emit('close')"
    pt:header="bg-surface-100 rounded-t-xl py-2">
    <template #header>
      <p class="font-bold text-lg">
        {{ formMode === "edit" ? "Edit Project" : "Create Project" }}
      </p>
      <div class="flex gap-4">
        <Button icon="pi pi-save" label="Save" form="projectForm" type="submit" />
        <!-- <Button icon="pi pi-replay" label="Reset" @click="handleReset" v-show="showForm" /> -->
        <Button icon="pi pi-times" label="Cancel" @click="emit('close')" />
      </div>
    </template>
    <Form v-slot="$form" :resolver="resolver" :initialValues="initialFormData" ref="formRef"
      class="flex flex-col gap-4 overflow-auto p-4 mb-32" @submit="handleSave" id="projectForm">
      <FormField v-slot="$field" name="product" class="form-field">
        <label for="product" class="required-mark">Product</label>
        <AutoComplete inputId="product" optionLabel="internal_name" :suggestions="productSuggestion"
          @complete="filterProductSuggestion" forceSelection placeholder="Search" dropdown fluid
          :disabled="Boolean(initialFormData?.id)" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="registration_type" class="form-field">
        <label for="registration_type" class="required-mark">Registration Type</label>
        <Select inputId="registration_type" :options="enums.RegistrationTypeEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="reg_entity" class="form-field">
        <label for="reg_entity" class="required-mark">Reg Entity</label>
        <Select inputId="reg_entity" :options="enums.RegEntityEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <!-- project_name  prod_internal_name + reg_type + reg_entity + <crop> + <target> -->
      <FormField v-slot="$field" name="project_name" class="form-field">
        <label class="required-mark">Project Name</label>
        <InputGroup>
          <InputGroupAddon>{{ projectNameFixed + "_" }}
          </InputGroupAddon>
          <InputText name="project_name_crop" v-model="projectNameCrop" placeHolder="Crop" class="flex-auto" />
          <InputText name="project_name_target" v-model="projectNameTarget" placeHolder="Target" class="flex-auto" />
        </InputGroup>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="indication" class="form-field">
        <label for="indication" class="required-mark">Indication</label>
        <Select inputId="indication" :options="enums.IndicationEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>


      <FormField v-slot="$field" name="project_status" class="form-field">
        <label for="project_status" class="required-mark">Project Status</label>
        <Select inputId="project_status" :options="enums.ProjectStatusEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="portfolio_contact" class="form-field">
        <label for="portfolio_contact" class="required-mark">Portfolio Contact</label>
        <AutoComplete inputId="portfolio_contact" optionLabel="name" :suggestions="portfolioContactSuggestion"
          @complete="filterPortfolioContactSuggestion" forceSelection placeholder="Type to filter" fluid dropdown />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="project_manager" class="form-field">
        <label for="project_manager" class="required-mark">Project Manager</label>
        <Select inputId="project_manager" :options="enums.ProjectManagerEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-slot="$field" name="reg_manager" class="form-field">
        <label for="reg_manager" class="required-mark">Reg Manager</label>
        <Select inputId="reg_manager" :options="enums.RegManagerEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="notification_entrance" class="form-field">
        <label for="notification_entrance">Notification Entrance</label>
        <InputText id="notification_entrance"></InputText>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="submission_status" class="form-field">
        <label for="submission_status">Submission Status</label>
        <Select inputId="submission_status" :options="enums.SubmissionStatusEnum" showClear></Select>
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="approved_date" class="form-field">
        <label for="approved_date" :class="{
          'required-mark': $form?.submission_status?.value === 'Approved',
        }">Approved Date</label>
        <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd"
          :disabled="$form?.submission_status?.value !== 'Approved'" />
        <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{ $field.error?.message }}
        </Message>
      </FormField>
    </Form>
  </Dialog>
</template>

<script setup>
  import { ref, inject, useTemplateRef, watch, computed, onMounted } from "vue";
  import { yupResolver } from "@primevue/forms/resolvers/yup";
  import * as yup from "yup";
  import { AutoComplete, Select } from "primevue";

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  // const toast = useToast();
  const Api = inject("Api");

  const { initialFormData } = defineProps({ initialFormData: Object });
  const emit = defineEmits(["close", "refresh"]);
  const visible = ref(true);
  const formMode = initialFormData.id ? "edit" : "new";

  // form select options
  const productSuggestion = ref();
  async function filterProductSuggestion(event) {
    productSuggestion.value = await Api.get(
      `/products/search?query=${event.query}`
    );
    // if (event.query.trim()) {
    //     productSuggestion.value = await Api.get(`/products/search?query=${event.query}`);
    // } else {
    //     // return all products if query is empty
    //     productSuggestion.value = [];
    // }
  }

  const portfolioContactSuggestion = ref();
  async function filterPortfolioContactSuggestion(event) {
    portfolioContactSuggestion.value = await Api.get(
      `/users/search?query=${event.query}`
    );
  }

  //yup resolver: (values,[names])=>{}->errors:obj
  const resolver = yupResolver(
    yup.object().shape({
      product: yup
        .mixed()
        .label("Product")
        .test("not-empty1", "Product is required", (value) => {
          return value !== "" && value !== undefined && value !== null;
        }),
      registration_type: yup.string().required(),
      reg_entity: yup.string().required(),
      project_name: yup.string(),
      indication: yup.string().label("Indication").required(),
      portfolio_contact: yup
        .mixed()
        .label("Portfolio Contact")
        .test("not-empty", "Portfolio Contact is required", (value) => {
          return value !== "" && value !== undefined && value !== null;
        }),
      project_manager: yup.string().required(),
      reg_manager: yup.string().required(),
      project_status: yup.string().required(),

      submission_status: yup.string().nullable(),
      approved_date: yup
        .date()
        .when("submission_status", ([submission_status], schema) => {
          return submission_status === "Approved"
            ? schema.required()
            : schema.nullable();
        }),
    })
  );

  async function handleSave(e) {
    // form filed values are matained by primevue Form, no need to bind to a ref or reactive

    if (!e.valid) return;
    // get and transform modified data
    let updatedFields = {};

    let _flag = true
    Object.entries(e.states).forEach(([field, state]) => {
      if (state.dirty) {
        console.log("dirty_field", field, state.value);
        if (field === "product") {
          // for product field
          updatedFields["product_id"] = state.value.id;
        }
        else if (field === "portfolio_contact") {
          // for portfolio_contact field
          updatedFields["portfolio_contact_id"] = state.value.id;
        } else if (["project_name_crop", "project_name_target"].includes(field)) {
          // exclude project_name_crop and project_name_target from updatedFields
        } else {
          // for other fields
          updatedFields[field] = state.value;
        };
        // update project_name if product, registration_type, reg_entity, project_name_crop, project_name_target is modified
        console.log("flag", _flag, field, ["product", "registration_type", "reg_entity", "project_name_crop", "project_name_target"]);
        if (_flag && ["product", "registration_type", "reg_entity", "project_name_crop", "project_name_target"].includes(field)) {
          console.log("project_name", projectNameFixed.value, projectNameCrop.value, projectNameTarget.value);
          updatedFields["project_name"] = `${projectNameFixed.value}_${projectNameCrop.value}_${projectNameTarget.value}`
          _flag = false
        }
      }
    });

    // do nothing if no field is modified
    if (Object.keys(updatedFields).length === 0) {
      return;
    }

    // distinguish add and patch through formData.id (Undefined == add)
    let newData;
    if (formMode === "edit") {
      // modify current porduct
      newData = await Api.patch(`/projects/${initialFormData.id}`, updatedFields);
    } else {
      // add new product
      newData = await Api.post("/projects/", updatedFields);
    }

    emit("refresh", newData);
    emit("close");
  }



  // #region project_name
  const formRef = useTemplateRef('formRef')
  const projectNameCrop = ref();
  const projectNameTarget = ref();

  // Compute fixed part of project name
  const projectNameFixed = computed(() => {
    const product = formRef.value?.states.product?.value?.internal_name || ''
    const regType = formRef.value?.states.registration_type.value || ''
    const regEntity = formRef.value?.states.reg_entity.value || ''
    return `${product}_${regType}_${regEntity}`
  })

  onMounted(() => {
    projectNameCrop.value = initialFormData?.project_name?.split('_')[3]
    projectNameTarget.value = initialFormData?.project_name?.split('_')[4]
  })
  // #endregion project_name
</script>
