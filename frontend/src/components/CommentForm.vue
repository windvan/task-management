<template>
    <form class="flex flex-col  p-4 bg-surface-100 rounded-md mb-8">
        <p class="font-bold mb-4">Add new comment</p>
        <div class="flex gap-2 ">
            <Select v-model="newComment.severity" :options="enums.NoteSeverityEnum" placeholder="severity" size="small">
                <template #value="{ value, placeholder }">
                    <div v-if="value" class="flex items-center">
                        <i :class="['pi pi-circle-fill', getCommentSeverity(value)]" />
                        <span class="ml-2">{{ value }}</span>
                    </div>
                    <span v-else>
                        {{ placeholder }}
                    </span>
                </template>
                <template #option="{ option }">
                    <div class="flex items-center text-sm">
                        <i :class="['pi pi-circle-fill', getCommentSeverity(option)]" />
                        <span class="ml-2">{{ option }}</span>
                    </div>
                </template>

            </Select>

            <div class="p-inputtext p-inputtext-sm flex items-center gap-2 bg-surface-100">
                <i :class="targetType === 'project' ? 'pi pi-folder' : 'pi pi-list'" />
                <span>{{ targetType === 'project' ? 'Project Comment' : 'Task Comment' }}</span>
            </div>
            <input type="number" v-model="newComment.targetId" class="hidden" />
            <input type="number" v-model="newComment.parentId" class="hidden" />
        </div>

        <MentionEditor ref="mentionEditorRef" v-model="newComment.mentionEditor" class="my-2"></MentionEditor>
        <div class="flex gap-4 justify-end font-bold">
            <Button size="small" outlined severity="secondary" @click="mentionEditorRef?.reset">Reset</Button>
            <Button size="small" outlined severity="secondary" @click="emit('close')">Cancel</Button>
            <Button size="small" outlined @click="handleSave">Comment</Button>
        </div>
    </form>
</template>

<script setup>
    // can only create comment
    import { useToast } from "primevue";
    import { ref, inject, useTemplateRef } from 'vue'
    import { getCommentSeverity } from '@/composables/fieldTools'
    import MentionEditor from './MentionEditor.vue'
    const toast = useToast()

    const { targetId, targetType } = defineProps({ targetId: Number, targetType: String })
    
    
    const emit = defineEmits(['refreshComment','close'])
    // default initial value
    const newComment = ref({
        severity: 'Info',
        mentionEditor: {
            plain_text: null,
            rich_text: null,
            mentions: []
        }   
    })

    const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
    const Api = inject('Api')
    const mentionEditorRef = useTemplateRef('mentionEditorRef')
    async function handleSave() {

        if (!newComment.value.mentionEditor.plain_text?.trim()) {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Please input comment', life: 3000 })
            return
        }
        const _comment = {
            [targetType === 'project' ? 'project_id' : 'task_id']: targetId,
            parent_id: null,//root comment
            rich_text: newComment.value.mentionEditor.rich_text,
            plain_text: newComment.value.mentionEditor.plain_text,
            mentions: newComment.value.mentionEditor.mentions,
            severity: newComment.value.severity,
        }

        const dbNewComment = await Api.post(`/comments/${targetType}`, _comment)
        
        emit('refreshComment', targetType === 'project' ? 'project_comments' : 'task_comments', dbNewComment)
        emit('close')
    }



</script>