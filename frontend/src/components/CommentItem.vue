<template>
  <div class="border border-surface-100 rounded">
    <!-- header line -->
    <div class="border-surface-100 p-4">
      <!-- header line -->
      <div class="flex gap-2 items-center">
        <span>{{ comment.created_by_name }} on </span>
        <span>{{ toLocalStr(comment.updated_at) }}</span>
        <Select v-if="!comment.parent_id" v-model="comment.severity" :options="enums.CommentSeverityEnum"
          class="border-none ml-auto" :pt="{dropdown:'hidden', option:'p-1',label:'p-1 leading-none'}"
          @change="handelChangeSeverity()">
          <template #value="{ value }">
            <i :class="[
                'pi pi-circle-fill text-sm',
                getCommentSeverity(value),
              ]" />
          </template>
          <template #option="{ option }">
            <div class="flex items-center text-sm h-au">
              <i :class="['pi pi-circle-fill text-sm', getCommentSeverity(option)]" />
              <span class="ml-2">{{ option }}</span>
            </div>
          </template>
        </Select>
      </div>
      <!-- content -->
      <div class="whitespace-pre-wrap my-4 break-words">
        {{ comment.plain_text }}
      </div>

      <!-- footer -->
      <div class="flex gap-4 justify-end items-center text-sm">

        <span>{{ comment.children.length }} replies</span>
        <Button  outlined severity="secondary" rounded :icon="toggleIcon" size="small" @click="handelToggleChild" v-if="comment.children.length!==0"></Button>
        <Button v-if="!showReplay" icon="pi pi-reply " size="small" rounded outlined severity="secondary"
          @click="handelStartReplay"></Button>
      </div>

    </div>

    <!-- replay -->
    <div v-if="showReplay" class="bg-surface-100 p-4 border-t border-surface-200">
      <MentionEditor v-model="mentionEditor"></MentionEditor>
      <div class="mt-2 flex gap-2 justify-end font-bold">
        <Button severity="secondary" outlined size="small" @click="showReplay = false">Cancel</Button>
        <Button size="small" @click="handleSaveReplay" outlined>Replay</Button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { toLocalStr } from "@/composables/dateTools";
  import { getCommentSeverity } from "@/composables/fieldTools";

  import MentionEditor from "./MentionEditor.vue";
  import { ref, inject } from "vue";

  const Api = inject("Api");

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};

  const { comment } = defineProps({
    comment: Object,
  });
 const emit = defineEmits(["refreshReply","toggleChild"]);
  const showReplay = ref(false);
  const mentionEditor = ref();
  function handelStartReplay() {
    mentionEditor.value = {
      plain_text: null,
      rich_text: null,
      mentions: [],
    };
    showReplay.value = true;
  }

  async function handleSaveReplay() {
    if (!mentionEditor.value.plain_text?.trim()) {
      toast.add({
        severity: "error",
        summary: "Error",
        detail: "Please input comment",
        life: 3000,
      });
      return;
    }

    const _comment = {
      [comment.project_id ? "project_id" : "task_id"]:
        comment.project_id ?? comment.task_id,
      parent_id: comment.id, //root comment
      rich_text: mentionEditor.value.rich_text,
      plain_text: mentionEditor.value.plain_text,
      mentions: mentionEditor.value.mentions,
      severity: null,
    };

    const dbNewComment = await Api.post(
      `/comments/${comment.project_id ? "project" : "task"}`,
      _comment
    );

    emit("refreshReply",comment.project_id?'project_comments' : 'task_comments',dbNewComment);
    showReplay.value = false;
    
  }

  async function handelChangeSeverity() {
    const targetType = comment.project_id ? "project" : "task";
    try {
      const response = await Api.patch(
        `/comments/${targetType}/${comment.id}`,
        { severity: comment.severity },
        { skipInterceptor: true }
      );
    } catch (error) {
      toast.add({
        severity: "error",
        summary: "Update severity Failed",
        detail: error.message,
        life: 3000,
      });
    }
  }
  const toggleIcon=ref('pi pi-angle-down')
  function handelToggleChild() {
    toggleIcon.value = toggleIcon.value === 'pi pi-angle-down' ? 'pi pi-angle-up' :'pi pi-angle-down'
    emit('toggleChild')
  }
</script>
