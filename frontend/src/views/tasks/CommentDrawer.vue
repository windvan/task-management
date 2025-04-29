<template>
  <Drawer v-model:visible="visible" @hide="emit('close')" :position="position" class="w-[40rem]"
    pt:content="overflow-hidden">
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <!-- <Button v-show="(activeTab === '1' && !showCommentForm)" severity="secondary" size="small" outlined
          label="New Comment" @click="handleShowCommentForm"></Button> -->
        <Button severity="secondary" rounded variant="text" :icon="'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          " @click="togglePosition"></Button>
      </div>
    </template>

    <Tabs v-model:value="activeTab" class="flex flex-col h-full">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels class="overflow-auto bg-surface-50">
        <!-- proj comment -->
        <TabPanel value="0">
          <div v-for="node in comments?.project_comments" :key="node.id"
            class="bg-white mb-4 rounded border border-surface-200">
            <CommentItem :comment="node" @refreshReply="handelRefreshCommentReply"></CommentItem>
            <TimeLine v-if="node.showChildren" :value="node.children"
              pt:eventOpposite="grow-0 whitespace-nowrap text-xs" pt:eventContent="rounded mb-4 mx-2 p-0"
              pt:root="my-4">
              <template #opposite="{ item, index }">
                <p>{{ item.created_by_name }}</p>
                <p>{{ toLocalStr(item.created_at) }}</p>
              </template>
              <template #content="{ item, index }">
                <Editor :defaultValue="item.rich_text" readonly pt:toolbar="hidden"
                  pt:content="!rounded-md !border-none [&>.ql-editor]:!min-h-0 [&>.ql-editor]:!bg-surface-100"></Editor>
              </template>
            </TimeLine>
          </div>
        </TabPanel>
        <TabPanel value="1">
          <!-- task comment -->
          <CommentForm v-if="showCommentForm" :targetId="targetId" targetType="task" @close="showCommentForm = false"
            @refreshComment="handelRefreshComment"></CommentForm>
          <InputText v-else fluid placeholder="New Comment" @focus="showCommentForm = true"
            class="placeholder-surface-300 placeholder:italic mb-3" />
          <div v-for="node in comments?.task_comments" :key="node.id"
            class="bg-white mb-4 rounded border border-surface-200">

            <CommentItem :comment="node" @refreshReply="handelRefreshCommentReply"></CommentItem>
            <TimeLine v-if="node.showChildren" :value="node.children"
              pt:eventOpposite="grow-0 whitespace-nowrap text-xs" pt:eventContent="rounded mb-4 mx-2 p-0"
              pt:root="my-4">
              <template #opposite="{ item, index }">
                <p>{{ item.created_by_name }}</p>
                <p>{{ toLocalStr(item.created_at) }}</p>
              </template>
              <template #content="{ item, index }">
                <Editor :defaultValue="item.rich_text" readonly pt:toolbar="hidden"
                  pt:content="!rounded-md !border-none [&>.ql-editor]:!min-h-0 [&>.ql-editor]:!bg-surface-100"></Editor>
              </template>
            </TimeLine>
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
  import { toLocalStr } from "../../composables/dateTools";

  const Api = inject("Api")

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


  const showCommentForm = ref(false);

  // #endregion new comment

  // #region comment list
  const comments = ref();
  const expandedComments = ref([]);


  onMounted(async () => {
    comments.value = await Api.get(`/comments/task/${targetId}`);
  });

  // #endregion comment list

  async function handelRefreshComment(targetType, newComment) {
    comments.value[targetType].unshift(newComment);
  }
  async function handelRefreshCommentReply(targetType, newComment) {
    const index = comments.value[targetType].findIndex(
      (comment) => comment.id === newComment.parent_id
    );
    if (index !== -1) {
      comments.value[targetType][index].children.unshift(newComment);
    }
  }
</script>
