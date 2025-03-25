<template>
    <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
        <template #header>
            <p class="font-bold text-lg">{{ props.headerText }}</p>
            <div class="flex gap-4">
                <Button type="submit" form="croForm" icon="pi pi-save" label="Save" />
                <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
            </div>
        </template>
        <Form pt:root:id="croForm" :resolver="resolver" @submit="handleSave" :initialValues="props.initialFormData"
            class="flex flex-col gap-4 overflow-auto p-4 mb-32">
            <FormField v-slot="$field" name="cro_name" class="form-field">
                <label for="cro_name" class="required-mark">CRO Name</label>
                <InputText id="cro_name" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="certification_number" class="form-field">
                <label for="certification_number" class="required-mark">Certification Number</label>
                <InputText id="certification_number"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="certification_expiration_date" class="form-field">
                <label for="certification_expiration_date" class="required-mark">Expiration Date</label>
                <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="certification_scope" class="form-field">
                <label for="certification_scope" class="required-mark">Certification Scope</label>
                <InputText id="certification_scope"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="fw_contract_start" class="form-field">
                <label for="fw_contract_start">FW Contract Start</label>
                <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="fw_contract_end" class="form-field">
                <label for="fw_contract_end">FW Contract End</label>
                <DatePicker showIcon showButtonBar iconDisplay="input" dateFormat="yy-mm-dd" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="fw_contract_detail" class="form-field">
                <label for="fw_contract_detail">FW Contract Detail</label>
                <InputText id="fw_contract_detail"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="address" class="form-field">
                <label for="address">Address</label>
                <InputText id="address"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

        </Form>
    </Dialog>
</template>

<script setup>
    import { inject, ref} from 'vue'
    import { yupResolver } from '@primevue/forms/resolvers/yup'
    import * as yup from 'yup'
    import { dateToStr } from '@/composables/dateTools'
    import { useToast } from 'primevue'

    const props = defineProps({ headerText: String, initialFormData: Object })
    const visible = ref(true)
    // const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
    // const toast = useToast()

    const emit = defineEmits(['refresh', 'close'])


    let selectOptions //all select components options on this page
    const Api = inject('Api')
    const expandedRowGroups = ref(null)
    const tableError = ref('')
    const selectedNodes = ref(null)

    const resolver = yupResolver(
        yup.object().shape({
            cro_name: yup.string().required(),
            certification_number: yup.string().required(),
            certification_expiration_date: yup.date().required(),
            certification_scope: yup.string().required()
        })
    )


    async function handleSave(e) {
        if (!e.valid) return

        let updatedFields = {}
        Object.entries(e.states).forEach(([field, state]) => {
            if (state.dirty) {
                if (state.value instanceof Date) {
                    // for date fields
                    updatedFields[field] =state.value

                } else if (state.value && typeof state.value === 'object') {
                    // for relational fields
                    updatedFields[field + '_id'] = state.value.id
                } else {
                    // for string and select field
                    updatedFields[field] = state.value
                }
            }
        })

        // update cro

        if (props.initialFormData) {
            // edit mode
            await Api.patch(`/cros/${props.initialFormData.id}/`, updatedFields)
        } else {
            // new mode
            await Api.post('/cros', updatedFields)
        }
        visible.value = false
        emit("refresh")
    }

    function handleCancel() {
        visible.value = false
    }
</script>
