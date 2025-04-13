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
          <!-- new comment： can only add project comment on this drawer -->
          <CommentForm
            v-if="showCommentForm"
            :targetId="targetId"
            targetType="project"
            @close="showCommentForm = false"
            @refreshComment="handelRefreshComment"></CommentForm>
          <InputText
            v-else
            fluid
            placeholder="New Comment"
            @focus="showCommentForm = true"
            class="placeholder-surface-300 placeholder:italic mb-3" />
          <div
            v-for="node in comments?.project_comments"
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
        <TabPanel value="1">
          <div
            v-for="(task_comment, task_id) in comments?.task_comments"
            :key="task_id">
            <p>{{ task_comment[0].task_name }}</p>
            <div
              v-for="node in task_comment"
              :key="node.id"
              class="bg-surface-100 mb-2">
              <CommentItem
                :comment="node"
                @refreshReply="handelRefreshCommentReply"></CommentItem>
              <div v-for="child in node.children" :key="child.id" class="ml-20">
                <CommentItem :comment="child"></CommentItem>
              </div>
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
  const { targetId, targetType } = defineProps({
    targetId: {
      type: Number,
      required: true,
    },
    targetType: {
      type: String,
      required: true,
      validator: (value) => ["task", "project"].includes(value),
    },
  });

  const emit = defineEmits(["close"]);
  const visible = ref(true);
  const activeTab = ref(targetType === "task" ? "1" : "0");
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

  async function handelRefreshComment(targetType, newComment) {
    comments.value[targetType].unshift(newComment);
  }
  async function handelRefreshCommentReply(category, newComment) {
    
    console.log(category);
    if (category === "project_comments") {
      const index = comments.value[category].findIndex(
        (comment) => comment.id === newComment.parent_id
      );
      console.log(index);
      if (index !== -1) {
        comments.value[category][index].children.unshift(newComment);
      }
    } else {
      const task_id = newComment.parent_id;
      const index = comments.value[category][task_id].findIndex(
        (comment) => comment.id === newComment.parent_id
      );
      if (index !== -1) {
        comments.value[category][task_id][index].children.unshift(newComment);
      }
    }
  }
</script>
