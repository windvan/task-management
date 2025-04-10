<template>
  <Drawer v-model:visible="visible" @hide="emit('close')" :position="position" class="w-[40rem]"
    pt:content="overflow-hidden">
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <Button severity="secondary" variant="text" :icon="'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          " @click="togglePosition"></Button>
      </div>
    </template>


    <Tabs v-model:value="activeTab" class="flex flex-col h-full">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels class=" overflow-auto">
        <TabPanel value="0">
          <CommentItem v-for="comment in comments?.project_comments" key="comment.id" :comment></CommentItem>
          <CommentForm :targetId="triggerId" targetType="project" @refreshComment="handelRefreshComment"></CommentForm>
        </TabPanel>
        <TabPanel value="1">
          <CommentItem v-for="comment in comments?.task_comments" key="comment.id" :comment></CommentItem>
          <CommentForm :targetId="triggerId" targetType="task" @refreshComment="handelRefreshComment"></CommentForm>
        </TabPanel>

      </TabPanels>
    </Tabs>
    <!-- <template #footer>
      <div class="flex items-center gap-2">
        <Button label="Add Comment" icon="pi pi-plus" class="flex-auto" outlined></Button>
      </div>
    </template> -->
  </Drawer>
</template>

<script setup>

  import { useToast } from "primevue";
  import { ref, inject, onMounted } from "vue";

  import CommentItem from "./CommentItem.vue";
  import CommentForm from "./CommentForm.vue";

  // whether the drawer is triggered from task or project
  const { triggerId, commentType } = defineProps({
    triggerId: {
      type: Number,
      required: true
    },
    commentType: {
      type: String,
      required: true,
      validator: (value) => ['task', 'project'].includes(value)
    }
  });

  const emit = defineEmits(["close"]);
  const visible = ref(true);
  const activeTab = ref((commentType === "task") ? '1' : '0')
  const position = ref("right");
  function togglePosition() {
    position.value = position.value === "full" ? "right" : "full";
  }

  // #region new comment
  // import { useAuthStore } from "@/stores/auth";
  // const {currentUser} = useAuthStore();

  const toast = useToast()
  const Api = inject('Api')



  // #endregion new comment

  // #region comment list
  const comments = ref()
  onMounted(async () => {

    comments.value = await Api.get(`/comments/all`)
  })

  // #endregion comment list

  function handelRefreshComment(commentType,newComment) {
    comments.value[commentType].unshift(newComment)
  }

</script>
