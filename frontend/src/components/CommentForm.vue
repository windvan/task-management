<template>
    <div class="flex flex-col gap-2 bg-surface-200 rounded mb-8 p-2">
        <!-- header -->
        <div class="flex items-center justify-between p-2">
            <p class="font-bold text-xl">New comment</p>
            <div class="flex gap-2 ">
                <Select v-model="newComment.severity" :options="enums.NoteSeverityEnum" placeholder="severity" :pt="{
                    label: 'p-1 flex', option: 'p-1'
                }">
                    <template #value="{ value, placeholder }">
                        <div v-if="value" class="flex items-center">
                            <i :class="['pi pi-circle-fill text-xs', getCommentSeverity(value)]" />
                            <span class="ml-2 text-xs">{{ value }}</span>
                        </div>
                        <span v-else>
                            {{ placeholder }}
                        </span>
                    </template>
                    <template #option="{ option }">
                        <div class="flex items-center ">
                            <i :class="['pi pi-circle-fill text-xs', getCommentSeverity(option)]" />
                            <span class="ml-2 text-xs">{{ option }}</span>
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
        </div>

        <!-- editor -->
        <Editor :defaultValue="null" :modules="modules" @textChange='handleEditorChange'
            pt:toolbar="!border-surface-200" pt:content="!border-surface-200">
            <template v-slot:toolbar>
                <span class="ql-formats">
                    <select class="ql-size">
                        <option value="small"></option>
                        <option selected></option>
                        <option value="large"></option>
                        <option value="huge"></option>
                    </select>
                </span>
                
                <span class="ql-formats">
                    <button class="ql-bold"></button>
                    <button class="ql-italic"></button>
                    <button class="ql-underline"></button>
                    <button class="ql-strike"></button>
                </span>

                <span class="ql-formats">
                    <button class="ql-list" value="ordered"></button>
                    <button class="ql-list" value="bullet"></button>
                </span>
                <span class="ql-formats">
                    <button class="ql-script" value="sub"></button>
                    <button class="ql-script" value="super"></button>
                </span>
                <span class="ql-formats">
                    <button class="ql-align" value=""></button>
                    <button class="ql-align" value="center"></button>
                    <button class="ql-align" value="right"></button>
                    <button class="ql-align" value="justify"></button>
                </span>
                <span class="ql-formats">
                    <button class="ql-link"></button>
                    <button class="ql-image"></button>
                </span>
                <span class="ql-formats">
                    <button class="ql-clean"></button>
                </span>
            </template>
        </Editor>

        <!-- buttons -->
        <div class="flex gap-4 justify-end font-bold">
            <Button size="small" outlined class="bg-white" severity="secondary" @click="resetComment">Reset</Button>
            <Button size="small" outlined class="bg-white" severity="secondary" @click="emit('close')">Cancel</Button>
            <Button size="small" outlined class="bg-white" @click="handleSave">Comment</Button>
        </div>
    </div>
</template>

<script setup>
    // can only create comment
    import { useToastService } from '../composables/useToastService'
    import { ref, inject, useTemplateRef } from 'vue'
    import { getCommentSeverity } from '@/composables/fieldTools'
    import "quill-mention/autoregister";
    // import 'quill/dist/quill.snow.css';


    const { showError, showWarning } = useToastService()
    const { targetId, targetType } = defineProps({ targetId: Number, targetType: String })


    const emit = defineEmits(['refreshComment', 'close'])
    // default initial value
    const newComment = ref({
        severity: 'Info',
        content: {
            plain_text: null,
            rich_text: null,
            mentions: []
        }
    })

    const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
    const Api = inject('Api')

    const modules = {

        mention: {
            allowedChars: /^[A-Za-z]*$/,
            mentionDenotationChars: ["@"],
            source: async function (searchTerm, renderList, mentionChar) {
                const user_list = await Api.get('/users/')
                const userSuggestion = user_list.map((user) => {
                    return {
                        id: user.id,
                        value: user.name,
                        role: user.role,
                        email: user.email
                    }
                })
                if (searchTerm.length === 0) {
                    renderList(userSuggestion, searchTerm);
                } else {
                    const matches = userSuggestion.filter((item) => {
                        return item.value.toLowerCase().includes(searchTerm.toLowerCase());
                    });
                    renderList(matches, searchTerm);
                }
            },

            dataAttributes: ['id', 'value'],
            listItemClass: "p-2  rounded",
            mentionContainerClass: "rounded border border-surface-200 shadow-sm bg-surface-50",
            mentionListClass: "max-h-48 overflow-y-auto",
            offsetLeft: 20,


        }
    }


    function handleEditorChange(event) {
        console.log(event)

        newComment.value.content.plain_text = event.textValue
        newComment.value.content.rich_text = event.htmlValue
        if (event.textValue?.length > 0) {
            for (const op of event.delta.ops) {
                if (op.insert?.mention) {
                    const mention = op.insert.mention
                    newComment.value.content.mentions.push(parseInt(mention.id))
                }
            }
        }

    }



    async function handleSave() {

        if (!newComment.value.content.plain_text?.trim()) {
            showWarning('Please input comment')
            return
        }
        const _comment = {
            [targetType === 'project' ? 'project_id' : 'task_id']: targetId,
            parent_id: null,//root comment
            rich_text: newComment.value.content.rich_text,
            plain_text: newComment.value.content.plain_text,
            mentions: newComment.value.content.mentions,
            severity: newComment.value.severity,
        }

        const dbNewComment = await Api.post(`/comments/${targetType}`, _comment)

        emit('refreshComment', targetType === 'project' ? 'project_comments' : 'task_comments', dbNewComment)
        emit('close')
    }

    function resetComment() {
        newComment.value = {
            severity: 'Info',
            content: {
                plain_text: null,
                rich_text: null,
                mentions: []
            }
        }

    }

</script>

<style>

    .mention {
        background-color: #d3e1eb;
        border-radius: 3px;
        margin-right: 2px;
        padding: 2px 2px;
        user-select: all;
    }

    .ql-container>.ql-editor {
        min-height: 150px;
        background-color: white;
        border-radius: 2px;
    }

    #quill-mention-list>.selected {
        background-color: #d3e1eb;
    }

</style>