<template>
    <div class="border border-surface-300 rounded mb-6">
        <!-- header line -->
        <div class="border-surface-100  p-4">
            <!-- header line -->
            <div class="flex gap-2">
                <span>{{ comment.created_by_name }} on </span>
                <span>{{ toLocalStr(comment.updated_at) }}</span>
                <Select v-model="comment.severity" :options="enums.CommentSeverityEnum" placeholder="severity"
                    size="small" class=" border-none ml-auto" pt:dropdown="hidden" @change="handelChangeSeverity()">
                    <template #value="{ value, placeholder }">
                        <div v-if="value" class="flex items-center">
                            <i :class="['pi pi-circle-fill', getCommentSeverity(value)]" />
                            <!-- <span class="ml-2">{{ value }}</span> -->
                        </div>
                        <span v-else>
                            {{ placeholder }}
                        </span>
                    </template>
                    <template #option="{ option }">
                        <div class="flex items-center">
                            <i :class="['pi pi-circle-fill', getCommentSeverity(option)]" />
                            <span class="ml-2">{{ option }}</span>
                        </div>
                    </template>

                </Select>

            </div>
            <!-- content -->
            <div class="whitespace-pre-wrap my-4 break-words ">
                {{ comment.plain_text }}
            </div>
        </div>

        <!-- replay -->
        <div v-if="showReplay" class="bg-surface-100 p-4 border-t border-surface-200">
            <MentionEditor v-model="mentionEditor"></MentionEditor>
            <div class="mt-2 flex gap-2 justify-end font-bold">
                <Button severity="secondary" outlined  size="small" @click="showReplay = false">Cancel</Button>
                <Button size="small" @click="handleSaveReplay" outlined>Replay</Button>
            </div>

        </div>
        <div v-else class="px-4 pb-4">
            <InputText fluid placeholder="replay" @focus="handelStartReplay" />
        </div>

        <!-- mention eidt -->


    </div>
</template>

<script setup>
    import { toLocalStr } from '@/composables/dateTools'
    import { getCommentSeverity } from '@/composables/fieldTools'
    import { InputText } from 'primevue';
    import MentionEditor from './MentionEditor.vue';
    import { ref, inject } from 'vue';

    const Api = inject('Api')

    const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};


    const { comment } = defineProps({
        comment: Object
    })


    const showReplay = ref(false)
    const mentionEditor = ref()
    function handelStartReplay() {
        mentionEditor.value = {
            plain_text: null,
            rich_text: null,
            mentions: []
        }
        showReplay.value = true
    }



    async function handleSaveReplay() {

        if (!mentionEditor.value.plain_text?.trim()) {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Please input comment', life: 3000 })
            return
        }

        const _comment =

        {
            [comment.project_id ? 'project_id' : 'task_id']: comment.project_id ?? comment.task_id,
            parent_id: comment.id,//root comment
            rich_text: mentionEditor.value.rich_text,
            plain_text: mentionEditor.value.plain_text,
            mentions: mentionEditor.value.mentions,
            severity: null,
        }

        const dbNewComment = await Api.post(`/comments/${comment.project_id ? 'project' : 'task'}`, _comment)
        // if (comment.project_id) {
        //     // project comment
        //     comment.value.project_comment.unshift(dbNewComment)
        // } else {
        //     comment.value.task_comment.unshift(dbNewComment)
        // }
        showReplay.value = false
    }

    async function handelChangeSeverity() {
        const commentType = comment.project_id ? 'project' : 'task'
        try {
            const response = await Api.patch(`/comments/${commentType}/${comment.id}`, { severity: comment.severity }, { skipInterceptor: true })
        } catch (error) {

            toast.add({ severity: 'error', summary: 'Update severity Failed', detail: error.message, life: 3000 })
        }
    }
</script>