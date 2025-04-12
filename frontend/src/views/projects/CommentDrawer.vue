<template>
  <Drawer
    v-model:visible="visible"
    @hide="emit('close')"
    :position="position"
    class="w-[40rem]"
    pt:content="overflow-hidden">
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <!-- <Button v-show="(activeTab === '1' && !showCommentForm)" severity="secondary" size="small" outlined
          label="New Comment" @click="handleShowCommentForm"></Button> -->
        <Button
          severity="secondary"
          rounded
          variant="text"
          :icon="
            'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          "
          @click="togglePosition"></Button>
      </div>
    </template>

    <Tabs v-model:value="activeTab" class="flex flex-col h-full">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels class="overflow-auto">
        <TabPanel value="0">
          <div
            v-for="node in comments?.project_comments"
            :key="node.id"
            class="bg-surface-100">
            <CommentItem :comment="node"></CommentItem>
            <div v-for="child in node.children" :key="child.id" class="ml-20">
              <CommentItem :comment="child"></CommentItem>
            </div>
          </div>
        </TabPanel>
        <TabPanel value="1">
          <!-- new comment： can only add task comment on this drawer -->
          <CommentForm
            v-if="showCommentForm"
            :targetId="targetId"
            targetType="task"
            @close="showCommentForm = false"
            @refreshComment="handelRefreshComment"></CommentForm>
          <InputText
            v-else
            fluid
            placeholder="New Comment"
            @focus="showCommentForm = true"
            class="placeholder-surface-300 placeholder:italic mb-3" />
          <div
            v-for="node in comments?.task_comments"
            :key="node.id"
            class="bg-surface-100">
            <CommentItem
              :comment="node"
              @refreshReply="handelRefreshCommentReply"></CommentItem>
            <div v-for="child in node.children" :key="child.id" class="ml-20">
              <CommentItem :comment="child"></CommentItem>
            </div>
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>
  </Drawer>
</template>

<script setup>
  import { useToast } from "primevue";
  import { ref, inject, onMounted } from "vue";

  import CommentItem from "../../components/CommentItem.vue";
  import CommentForm from "../../components/CommentForm.vue";

  // whether the drawer is triggered from task or project
  const { targetId, commentType } = defineProps({
    targetId: {
      type: Number,
      required: true,
    },
    commentType: {
      type: String,
      required: true,
      validator: (value) => ["task", "project"].includes(value),
    },
  });

  const emit = defineEmits(["close"]);
  const visible = ref(true);
  const activeTab = ref(commentType === "task" ? "1" : "0");
  const position = ref("right");
  function togglePosition() {
    position.value = position.value === "full" ? "right" : "full";
  }

  // #region new comment
  const toast = useToast();
  const Api = inject("Api");
  const showCommentForm = ref(false);

  // #endregion new comment

  // #region comment list
  const comments = ref();
  onMounted(async () => {
    comments.value = await Api.get(`/comments/project/${targetId}`);
  });

  // #endregion comment list

  async function handelRefreshComment(commentType, newComment) {
    comments.value[commentType].unshift(newComment);
  }
  async function handelRefreshCommentReply(commentType, newComment) {
    const index = comments.value[commentType].findIndex(
      (comment) => comment.id === newComment.parent_id
    );
    if (index !== -1) {
      comments.value[commentType][index].children.unshift(newComment);
    }
  }
</script>
