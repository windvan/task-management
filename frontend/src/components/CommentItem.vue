<template>
  <!-- comment item -->
  <div class="border border-surface-100 rounded p-2">
    <!-- header line -->
    <div class="flex gap-2 items-center">
      <span>{{ comment.created_by_name }} on </span>
      <span>{{ toLocalStr(comment.updated_at) }}</span>
      <Select v-if="!comment.parent_id" v-model="comment.severity" :options="enums.CommentSeverityEnum"
        class="border-none ml-auto" :pt="{ dropdown: 'hidden', option: 'p-1', label: 'p-1 leading-none' }"
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
    <Editor :defaultValue="comment.rich_text" readonly pt:toolbar="hidden"
      pt:content="!border-none [&>.ql-editor]:!min-h-0"></Editor>

    <!-- footer -->
    <div class="flex gap-4 justify-end items-center text-sm">

      <span>{{ comment.children.length }} replies</span>
      <Button outlined severity="secondary" rounded :icon="toggleIcon" size="small" @click="handelToggle" title="Expand"
        v-if="comment.children.length !== 0"></Button>
      <Button v-if="!showReplay" icon="pi pi-reply " size="small" rounded outlined severity="secondary"
        @click="handelStartReplay" title="Reply"></Button>
    </div>

    <!-- replay -->
    <div v-if="showReplay" class="bg-surface-100 p-2 rounded mt-2">
      <!-- <MentionEditor v-model="mentionEditor"></MentionEditor> -->
      <Editor :defaultValue="null" :modules="modules" @textChange='handleEditorChange' pt:toolbar="!border-surface-200"
        pt:content="!border-surface-200">
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
      <div class="mt-2 flex gap-2 justify-end font-bold">
        <Button severity="secondary" class="bg-white" outlined size="small" @click="showReplay = false">Cancel</Button>
        <Button size="small" class="bg-white" @click="handleSaveReplay" outlined>Replay</Button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { toLocalStr } from "@/composables/dateTools";
  import { getCommentSeverity } from "@/composables/fieldTools";
  import { ref, inject, computed } from "vue";
  import { useToastService } from "../composables/useToastService";
  // import "quill-mention/autoregister";
  // import 'quill/dist/quill.snow.css';


  const { showWarning, showError } = useToastService()

  const Api = inject("Api")

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};

  const { comment } = defineProps({
    comment: Object,
  });
  const emit = defineEmits(["refreshReply"]);

  const showReplay = ref(false);
  const replayContent = ref();

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


  async function handelStartReplay() {
    replayContent.value = { htmlValue: null, textValue: null, mentions: [] }
    showReplay.value = true;
  }

  function handleEditorChange(event) {
    replayContent.value.htmlValue = event.htmlValue
    replayContent.value.textValue = event.textValue
    if (event.textValue?.length > 0) {
      for (const op of event.delta.ops) {
        if (op.insert?.mention) {
          const mention = op.insert.mention
          replayContent.value.mentions.push(parseInt(mention.id))

        }
      }
    }

  }
  async function handleSaveReplay() {
    if (!replayContent.value.textValue?.trim()) {
      showWarning('Please input comment')
      return;
    }

    const _comment = {
      [comment.project_id ? "project_id" : "task_id"]:
        comment.project_id ?? comment.task_id,
      parent_id: comment.id, //root comment
      rich_text: replayContent.value.htmlValue,
      plain_text: replayContent.value.textValue,
      mentions: replayContent.value.mentions,
      severity: null,
    };

    const dbNewComment = await Api.post(
      `/comments/${comment.project_id ? "project" : "task"}`,
      _comment
    );

    emit("refreshReply", comment.project_id ? 'project_comments' : 'task_comments', dbNewComment);
    showReplay.value = false;

  }

  async function handelChangeSeverity() {
    const targetType = comment.project_id ? "project" : "task";
    try {
      const response = await Api.patch(
        `/comments/${targetType}/${comment.id}`,
        { severity: comment.severity },
      );
    } catch (error) {
      showError('Update severity Failed', error.message)
    }
  }


  const toggleIcon = ref('pi pi-angle-down')
  function handelToggle() {
    // Toggle the icon
    toggleIcon.value = toggleIcon.value === 'pi pi-angle-up' ? 'pi pi-angle-down' : 'pi pi-angle-up'
    // new property will automatically be reactive
    comment.showChildren = !comment.showChildren


  }
</script>
