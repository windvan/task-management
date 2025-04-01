<template>
  <Drawer v-model:visible="visible" @hide="emit('close')" :position="position" class="w-[40rem]">
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
          size="small" class="w-36">
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
            <div class="flex items-center">
              <i :class="['pi pi-circle-fill', getCommentSeverity(option)]" />
              <span class="ml-2">{{ option }}</span>
            </div>
          </template>
          <template #dropdownicon>
            <i class="pi pi-map" />
          </template>
        </Select>
        <AutoComplete name='tags' v-model="newComment.tags" placeholder="#Tags" size="small" class="grow"
          pt:pcInputText:root="w-full"></AutoComplete>
        <Select v-model="commentCategroy" :options="['Project Comment', 'Task Comment']" size="small" class="w-44"
          placeholder="Category">

        </Select>
      </div>
      <Textarea name="content" v-model="newComment.content" class="h-40"></Textarea>
      <div class="flex gap-4 justify-center">
        <Button label="Cancel" icon="pi pi-times" size="small" outlined @click="handleHideNewComment"></Button>
        <Button label="Save" icon="pi pi-save" size="small" outlined @click="handleCreateComment"></Button>
      </div>
    </form>

    <Tabs v-else value="0">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="0">
          <p class="m-0">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
            dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
            ea commodo
            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id
            est laborum.
          </p>
        </TabPanel>
        <TabPanel value="1">
          <p class="m-0">
            Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem
            aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.
            Nemo enim
            ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos
            qui ratione voluptatem sequi nesciunt. Consectetur, adipisci velit, sed quia non numquam eius modi.
          </p>
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

  const { project_id, task_id } = defineProps({
    project_id: {
      type: Number,
      required: false
    },
    task_id: {
      type: Number,
      required: false
    }
  });
  const emit = defineEmits(["close"]);
  const visible = ref(true);
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

  const newComment = ref({ severity: 'Info' })
  const commentCategroy = ref()
  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  function handleShowNewComment() {
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

  watch(commentCategroy, () => {

    if (commentCategroy.value === 'Project Comment') {
      newComment.value.task_id = null
      newComment.value.project_id = project_id
    } else {
      newComment.value.project_id = null
      newComment.value.task_id = task_id
    }
  })


  async function handleCreateComment() {
    console.log(!(newComment.value.task_id && newComment.value.project_id))
    if (!(newComment.value.task_id || newComment.value.project_id)) {

      toast.add({ severity: 'error', summary: 'Error', detail: 'Please select a project or a task to comment on', life: 3000 })
      return
    }
    if (!(newComment.value.content.trim())) {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Please input comment content', life: 3000 })
      return
    }

    newComment = await Api.post('/notes/', newComment.value)
  }


  // #endregion new comment

  // #region comment list
  onMounted(async () => {
    if (project_id) {
      const comments = await Api.get(`/notes/?project_id=${project_id}`)
    } else {
      const comments = await Api.get(`/notes/?task_id=${task_id}`)
    }
  })



  // #endregion comment list
</script>
