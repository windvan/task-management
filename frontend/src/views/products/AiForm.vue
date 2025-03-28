<template>
    <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
        <template #header>
            <p class="font-bold text-lg">
                {{ initialFormData.id ? "Edit Product Ai" : "Create Product Ai" }}
            </p>
            <div class="flex gap-4">
                <Button type="submit" form="aiForm" icon="pi pi-save" label="Save" />
                <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
            </div>
        </template>
        <Form pt:root:id="aiForm" :resolver="resolver" @submit="handleSave" :initialValues="initialFormData"
            class="flex flex-col gap-4 overflow-auto p-4 mb-32">

            <FormField v-slot="$field" name="product_id" class="form-field ">
                <InputNumber id="product_id" class="hidden" />
                Procuct Internal Name: {{ initialFormData.product_internal_name }}
            </FormField>

            <FormField v-slot="$field" name="abbreviation" class="form-field">
                <label for="abbreviation" class="required-mark">Abbreviation</label>
                <InputText id="abbreviation" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <!-- <input type="number" name="cro_id" :value="props.croId" visible="false" /> -->

            <FormField v-slot="$field" name="common_name" class="form-field">
                <label for="common_name" class="required-mark">Common Name</label>
                <InputText id="common_name"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="common_name_cn" class="form-field">
                <label for="common_name_cn">Common Name(CN)</label>
                <InputText id="common_name_cn" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="design_code" class="form-field">
                <label for="design_code">Design Code</label>
                <InputText id="remarks" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

        </Form>
    </Dialog>
</template>

<script setup>
    import { inject, ref } from 'vue'
    import { yupResolver } from '@primevue/forms/resolvers/yup'
    import * as yup from 'yup'

    import { InputNumber, InputText, useToast } from 'primevue'

    const { initialFormData } = defineProps({ initialFormData: Object })
    const visible = ref(true)
    // const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
    // const toast = useToast()

    const emit = defineEmits(['refresh', 'close'])
    const Api = inject('Api')

    const resolver = yupResolver(
        yup.object().shape({
            product_id: yup.number().required(),
            abbreviation: yup.string().required(),
            common_name: yup.string().required()
        })
    )

    async function handleSave(e) {
        if (!e.valid) return
        let updatedFields = { product_id: initialFormData.product_id }
        Object.entries(e.states).forEach(([field, state]) => {
            if (state.dirty) {    
                updatedFields[field] = state.value
            }
        })
        // do nothing if no field is updated
        if (Object.entries(updatedFields).length === 0) {
            return
        }
        // send data to server
        let newData
        if (initialFormData.id) {
            // edit mode
            newData = await Api.patch(`/products/${initialFormData.product_id}/ais/${initialFormData.id}`, updatedFields)
        } else {
            // new mode
            newData = await Api.post(`/products/${initialFormData.product_id}/ais`, updatedFields)
        }
    
        emit('close')
        emit("refresh", initialFormData.product_id, newData)
    }

    function handleCancel() {
        visible.value = false
    }
</script>
