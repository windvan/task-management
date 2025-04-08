<template>

  <Popover ref="poRef" class="popover w-[30rem]" @hide="emit('close')">
    <!-- header -->
    <div class="flex justify-between mb-4">
      <span class="font-bold">Notifications</span>
      <Button outlined severity="secondary" class="py-0 text-sm" @click="handleAllRead">Mark all as read</Button>
    </div>
    <!-- category -->

    <!-- <SelectButton v-model="activeNotiCategory" :options="NotiCategory" class="w-full justify-around rou"
      :pt:pcToggleButton:root="({ context }) => {return {class: context.active ? 'bg-primary rounded-2xl' : 'bg-surface-100 rounded-2xl' } }"/> -->
    <Tabs value="0">
      <TabList>
        <Tab value="0">
          <div class="relative">
            <span>Reminder</span>
            <i v-if="reminders?.length !== 0" class="pi pi-circle-fill text-[5px] absolute top-0 text-red-500"></i>
          </div>
        </Tab>
        <Tab value="1">
          <div class="relative">
            <span>Update</span>
            <i v-if="messages?.updates?.some(item => !item.is_read)"
              class="pi pi-circle-fill text-[5px] absolute top-0 text-red-500"></i>
          </div>
        </Tab>
        <Tab value="2">
          <div class="relative">
            <span>Message</span>
            <i v-if="messages?.mentions?.some(item => !item.is_read)"
              class="pi pi-circle-fill text-[5px] absolute top-0 text-red-500"></i>
          </div>
        </Tab>
      </TabList>
      <TabPanels pt:root=" rounded-md pt-0  h-[30rem] overflow-auto">
        <!-- reminder -->
        <TabPanel value="0">

          <div class="shadow rounded-md p-2 bg-surface-100 my-4 flex items-center gap-4" v-for="reminder of reminders">
            <Badge :class="reminder.days_remaining <= 15 ? 'bg-red-500' : 'bg-orange-400'"></Badge>
            <p>
              <span>{{ `Task 【 ${reminder.project_name}_${reminder.task_name}】is expected to be delivered in ` }}</span>
              <span class="font-bold" :class="reminder.days_remaining <= 15 ? 'text-red-500' : 'text-orange-400'">{{
                `${reminder.days_remaining} days (${toLocalStr(reminder.expected_delivery_date)})` }}</span>
            </p>
          </div>
        </TabPanel>
        <!-- update -->
        <TabPanel value="1">

          <div v-for="msg of messages?.updates" class="rounded border-t border-surface-300 p-3 hover:bg-surface-200">
            <div class="relative">
              <p class="bg-surface-100 rounded-md p-2 whitespace-pre-wrap">{{ msg.content }}</p>
              <i class="pi pi-eye absolute top-0 right-0" :class="msg.is_read ? 'text-surface-400' : 'text-primary'"
                @click="toggleUpdateReadStatus(msg)"></i>
            </div>
          </div>

        </TabPanel>
        <!-- Message -->
        <TabPanel value="2">
          <div v-for="msg of messages?.mentions" class="rounded border-t border-surface-300 p-3 hover:bg-surface-200">
            <div class="relative">
              <p class="bg-surface-100 rounded-md p-2 whitespace-pre-wrap">{{ msg.content }}</p>
              <i class="pi pi-eye absolute top-0 right-0" :class="msg.is_read ? 'text-surface-400' : 'text-primary'"
                @click="toggleMentionReadStatus(msg)"></i>
            </div>
          </div>


        </TabPanel>
      </TabPanels>

    </Tabs>


  </Popover>

</template>

<script setup>
  import { useTemplateRef, ref, onMounted, inject } from "vue"
  import { toLocalStr } from "../composables/dateTools"

  const Api = inject('Api')

  const poRef = useTemplateRef('poRef')
  const emit = defineEmits(['close'])
  defineExpose({
    toggle: (event) => poRef.value?.toggle(event),
  });


  // const NotiCategory = ['Reminder', 'Update', 'Message']
  // const activeNotiCategory = ref('Reminder')

  const reminders = ref()
  const messages = ref() //updates and mentions
  onMounted(async () => {
    reminders.value = await Api.get('/tasks/notifications/reminders/')
    messages.value = await Api.get('/tasks/notifications/messages/')
  })

  async function toggleUpdateReadStatus(msg) {
    const index = messages.value.updates.findIndex((m) => m.msg_recp_id === msg.msg_recp_id)
    if (index !== -1) {
      await Api.patch(`/messages/read/${msg.msg_recp_id}`, {
        is_read: !msg.is_read
      })
      messages.value.updates[index].is_read = !messages.value.updates[index].is_read
    }
  }

  async function toggleMentionReadStatus(msg) {
    const index = messages.value.mentions.findIndex((m) => m.msg_recp_id === msg.msg_recp_id)
    if (index !== -1) {
      await Api.patch(`/messages/read/${msg.msg_recp_id}`, {
        is_read: !msg.is_read
      })
      messages.value.updates[index].is_read = !messages.value.updates[index].is_read
    }
  }

  async function handleAllRead() {
    const unreadUpdates = messages.value.updates.filter((msg) => !msg.is_read)
    const unreadMentions = messages.value.mentions.filter((msg) => !msg.is_read)
    const unreadIds = [...unreadUpdates, ...unreadMentions].map((msg) => msg.msg_recp_id)
    if (unreadIds.length > 0) {
      // update database
      await Api.patch('/messages/batch-read', unreadIds)
      // update local state
      for (const id of unreadIds) {
        const index = messages.value.updates.findIndex((msg) => msg.msg_recp_id === id)

        if (index !== -1) {
          messages.value.updates[index].is_read = true
        }
        else {
          const index = messages.value.mentions.findIndex((msg) => msg.msg_recp_id === id)
          messages.value.mentions[index].is_read = true
        }
      }

    }
  }


</script>


<style module></style>
