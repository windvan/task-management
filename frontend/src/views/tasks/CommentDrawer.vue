<template>
  <Drawer v-model:visible="visible" @hide="emit('close')" :position="position" class="w-[40rem]"
    pt:content="overflow-hidden">
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <Button label="Add Comment" icon='pi pi-plus' size="small" outlined @click="handleShowNewComment"
          v-if="!showNewComment"></Button>
        <Button severity="secondary" variant="text" :icon="'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          " @click="togglePosition"></Button>
      </div>
    </template>


    <form class="flex flex-col gap-2 p-4" v-if="showNewComment">
      <div class="flex gap-1">
        <Select name="severity" v-model="newComment.severity" :options="enums.NoteSeverityEnum" placeholder="severity"
          size="small">
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
          <i :class="id_type === 'project' ? 'pi pi-folder' : 'pi pi-list'" />
          <span>{{ id_type === 'project' ? 'Project Comment' : 'Task Comment' }}</span>
        </div>


        <AutoComplete name='tags' v-model="newComment.tags" placeholder="#Tags" size="small" class="grow text-primary"
          pt:pcInputText:root="w-full"></AutoComplete>
      </div>
      <Textarea name="content" v-model="newComment.content" autoResize class="min-h-40"></Textarea>
      <div class="flex gap-4 justify-center">
        <Button label="Cancel" icon="pi pi-times" size="small" outlined @click="handleHideNewComment"></Button>
        <Button label="Save" icon="pi pi-save" size="small" outlined @click="handleCreateComment"></Button>
      </div>
    </form>

    <Tabs v-else v-model:value="activeTab">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels pt:root="pl-0 pr-2" class=" h-dvh overflow-auto">
        <TabPanel value="0">
          <div v-for="comment in comments?.project_notes" key="comment.id"
            class="border border-surface-200 rounded mb-6 p-2 bg-surface-50">
            <div class="flex gap-2">
              <span class=" font-bold">{{ comment.created_by_name }}</span>
              <span>{{ new Date(comment.updated_at+'Z').toLocaleDateString() }}</span>
              <span class="text-primary mx-auto"> {{ comment.tags }}</span>
              <Select v-model="comment.severity" :options="enums.NoteSeverityEnum" placeholder="severity" size="small"
                class=" border-none bg-surface-50" pt:dropdown="hidden" @change="handelChangeSeverity(comment)">
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
            <!-- <Textarea v-model="comment.content" fluid></Textarea> -->
            <div class="px-2 whitespace-pre-wrap">

              {{ comment.content }}
            </div>

          </div>
        </TabPanel>
        <TabPanel value="1">
          <div v-for="comment in comments?.task_notes" key="comment.id"
            class="border border-surface-200 rounded mb-6 p-2 bg-surface-50">
            <div class="flex gap-2">
              <span class=" font-bold">{{ comment.created_by_name }}</span>
              <span>{{ new Date(comment.updated_at+'Z').toLocaleDateString() }}</span>
              <span class="text-primary mx-auto"> {{ comment.tags }}</span>
              <Select v-model="comment.severity" :options="enums.NoteSeverityEnum" placeholder="severity" size="small"
                class=" border-none bg-surface-50" pt:dropdown="hidden" @change="handelChangeSeverity(comment)">
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
            <!-- <Textarea v-model="comment.content" fluid></Textarea> -->
            <div class="px-2 whitespace-pre-wrap">
              {{ comment.content }}
            </div>

          </div>
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
  import { ref, watch, inject, onMounted } from "vue";

  // whether the drawer is triggered from task or project
  const { trigger_id, id_type } = defineProps({
    trigger_id: {
      type: Number,
      required: false
    },
    id_type: {
      type: String,
      required: false,
      validator: (value) => ['task', 'project'].includes(value)
    }
  });
  const emit = defineEmits(["close"]);
  const visible = ref(true);
  const activeTab = ref((id_type === "task") ? '1' : '0')
  const position = ref("right");
  function togglePosition() {
    position.value = position.value === "full" ? "right" : "full";
  }


  // #region new comment
  // import { useAuthStore } from "@/stores/auth";
  // const {currentUser} = useAuthStore();
  const showNewComment = ref(false)
  const toast = useToast()
  const Api = inject('Api')

  const newComment = ref()

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  function handleShowNewComment() {
    let defalut = {}
    defalut[(id_type === "task") ? 'task_id' : 'project_id'] = trigger_id
    defalut['severity'] = 'Info'
    newComment.value = defalut
    showNewComment.value = true
  }
  function handleHideNewComment() {
    showNewComment.value = false
  }
  function getCommentSeverity(severity) {
    switch (severity) {
      case 'Danger':
        return 'text-red-600'
      case 'Warning':
        return 'text-orange-400'
      case 'Info':
        return 'text-green-600'
      default:
        return 'text-green-60'
    }
  }




  async function handleCreateComment() {

    // if (!(newComment.value.task_id || newComment.value.project_id)) {
    //   toast.add({ severity: 'error', summary: 'Error', detail: 'Please select a project or a task to comment on', life: 3000 })
    //   return
    // }

    if (!newComment.value?.content?.trim()) {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Please input comment content', life: 3000 })
      return
    }

    const dbNewComment = await Api.post('/notes/', newComment.value)
    if (dbNewComment.project_id) {
      // project comment
      comments.value.project_notes.unshift(dbNewComment)
    } else {
      comments.value.task_notes.unshift(dbNewComment)
    }
    showNewComment.value = false
  }

  async function handelChangeSeverity(comment) {
    try {
      await Api.patch(`/notes/${comment.id}`, { severity: comment.severity }, { skipInterceptor:true})
    } catch (error) {
      toast.add({ severity: 'error', summary: 'Update severity Failed', detail: error.message, life: 3000 })
    }
  }

  // #endregion new comment

  // #region comment list
  const comments = ref()
  onMounted(async () => {
    // comments.value = await Api.get(`/notes/?project_id=${project_id}&task_id=${task_id}`)
    comments.value = await Api.get(`/notes/${id_type}/${trigger_id}`)
  })



  // #endregion comment list
</script>
