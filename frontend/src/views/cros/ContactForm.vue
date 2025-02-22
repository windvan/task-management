<template>
    <Dialog v-model:visible="visible" :style="{ width: '80%' }" :modal="true" maximizable @hide="emit('close')">
        <template #header>
            <p class="font-bold text-lg">{{ props.headerText }}</p>
            <div class="flex gap-4">
                <Button type="submit" form="contactForm" icon="pi pi-save" label="Save" />
                <Button icon="pi pi-times" label="Cancel" @click="handleCancel" />
            </div>
        </template>
        <Form pt:root:id="contactForm" :resolver="resolver" @submit="handleSave" :initialValues="props.initialFormData"
            class="flex flex-col gap-4 overflow-auto p-4 mb-32">
            <FormField v-slot="$field" name="contact_name" class="form-field">
                <label for="contact_name" class="required-mark">Contact Name</label>
                <InputText id="contact_name" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <!-- <input type="number" name="cro_id" :value="props.croId" visible="false" /> -->

            <FormField v-slot="$field" name="phone_number" class="form-field">
                <label for="phone_number" class="required-mark">Phone Number</label>
                <InputText id="phone_number"></InputText>
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="email" class="form-field">
                <label for="email" class="required-mark">Email</label>
                <InputText id="email" />
                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="discipline" class="form-field">
                <label for="discipline">Discipline</label>
                <Select :options="enums.DisciplineEnum" class="w-full"></Select>

                <Message v-if="$field?.invalid" size="small" variant="simple" severity="error">{{
                    $field.error?.message
                }}</Message>
            </FormField>

            <FormField v-slot="$field" name="remarks" class="form-field">
                <label for="remarks">Remarks</label>
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
    import { dateToStr } from '@/composables/dateTools'
    import { InputText, useToast } from 'primevue'

    const props = defineProps({ headerText: String, initialFormData: Object, croId: Number })
    const visible = ref(true)
    const enums = JSON.parse(localStorage.getItem('cachedEnums')) || {}
    // const toast = useToast()

    const emit = defineEmits(['refresh', 'close'])
    const Api = inject('Api')

    const resolver = yupResolver(
        yup.object().shape({
            contact_name: yup.string().required(),
            phone_number: yup.string().required(),
            email: yup.string().email().required(),
        })
    )

    async function handleSave(e) {
        if (!e.valid) return

        let updatedFields = { cro_id: props.croId }
        Object.entries(e.states).forEach(([field, state]) => {
            if (state.dirty) {
                if (state.value instanceof Date) {
                    // for date fields
                    updatedFields[field] = dateToStr(state.value)

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
            await Api.patch(`/cros/contacts/${initialFormData.id}`, updatedFields)
        } else {
            // new mode

            await Api.post('/cros/contacts', updatedFields)
        }
        visible.value = false
        emit("refresh", props.croId)
    }

    function handleCancel() {
        visible.value = false
    }
</script>
