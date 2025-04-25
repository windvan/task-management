<template>

  <Popover ref="poRef" class="popover w-[30rem]" @hide="emit('close')">
    <!-- header -->
    <div class="flex justify-between mb-4">
      <span class="font-bold">Notifications</span>
      <Button outlined severity="secondary" class="py-0 text-sm" @click="batchRead">Mark all as read</Button>
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
            <i v-if="updates?.some(item => !item.is_read)"
              class="pi pi-circle-fill text-[5px] absolute top-0 text-red-500"></i>
          </div>
        </Tab>
        <Tab value="2">
          <div class="relative">
            <span>Message</span>
            <i v-if="messages?.some(item => !item.is_read)"
              class="pi pi-circle-fill text-[5px] absolute top-0 text-red-500"></i>
          </div>
        </Tab>
      </TabList>
      <TabPanels pt:root=" rounded-md pt-0  h-[30rem] overflow-auto">
        <!-- reminder -->
        <TabPanel value="0" class="flex flex-col gap-4 pt-4">

          <div class="rounded bg-surface-100 p-4 border"
            :class="reminder.days_remaining <= 15 ? 'border-red-500' : 'brder-orange-400'" v-for="reminder of reminders">

            <span>{{ `Task 【 ${reminder.project_name}_${reminder.task_name}】is expected to be delivered in ` }}</span>
            <span class="font-bold" :class="reminder.days_remaining <= 15 ? 'text-red-500' : 'text-orange-400'">{{
              `${reminder.days_remaining} days (${toLocalStr(reminder.expected_delivery_date)})` }}</span>
          </div>
        </TabPanel>
        <!-- update -->
        <TabPanel value="1" class="flex flex-col gap-4 pt-4">

          <div v-for="msg of updates" class="rounded bg-surface-100 p-4" :class="{'font-bold':!msg.is_read}"
            @contextmenu="(event)=>handleItemRightClick(event,msg)">

            <p class="bg-surface-100 rounded-md p-2 whitespace-pre-wrap">{{ msg.content }}</p>

          </div>

        </TabPanel>
        <!-- Message -->
        <TabPanel value="2" class="flex flex-col gap-4 pt-4">
          <div v-for="msg of messages" class="rounded bg-surface-100 p-4" :class="{ 'font-bold': !msg.is_read }"
            @contextmenu="(event)=>handleItemRightClick(event,msg)">
            {{ msg.content }}
            <!-- <p class="bg-surface-100 rounded-md p-2 whitespace-pre-wrap">{{ msg.content }}</p> -->

          </div>

        </TabPanel>

        <ContextMenu ref="ctxMenuRef" :model="ctxMenu" />
      </TabPanels>

    </Tabs>


  </Popover>

</template>

<script setup>
  import { useTemplateRef, ref, onMounted, inject } from "vue"
  import { toLocalStr } from "../composables/dateTools"
  import { storeToRefs } from "pinia";
  import { useNotificationStore } from "../stores/notificationStore";

  const Api = inject("Api")

  const emit = defineEmits(['close'])
  defineExpose({
    toggle: (event) => poRef.value?.toggle(event),
  });

  const { reminders, updates, messages } = storeToRefs(useNotificationStore())

  const poRef = useTemplateRef('poRef')


  // context menu
  const ctxMenu=ref()
  const ctxMenuRef = useTemplateRef("ctxMenuRef")
  function handleItemRightClick(event, msg) {

    ctxMenu.value = [
      {
        label: 'Mark as read',
        icon: 'pi pi-sun',
        command: () => readMessage(msg),
        disabled:msg.is_read
      },
      {
        label: 'Mark as unread',
        icon: 'pi pi-moon',
        command: () => unreadMessage(msg),
        disabled: !msg.is_read
      }
    ];

    ctxMenuRef.value.show(event);

  }


  async function readMessage(msg) {
    const source  =  msg.category==="Update"?updates:messages  
      const index = source.value.findIndex((m) => m.msg_recp_id === msg.msg_recp_id)
      if (index !== -1) {
        await Api.patch('/notifications/read', msg.msg_recp_id)
        source.value[index].is_read = true
      }
    }
    
  async function unreadMessage(msg) {
    
    const source = msg.category === "Update" ? updates : messages
    const index = source.value.findIndex((m) => m.msg_recp_id === msg.msg_recp_id)
    if (index !== -1) {
      await Api.patch('/notifications/unread', msg.msg_recp_id )
      source.value[index].is_read = false
    }
  }


  async function batchRead() {
    const unreadUpdates = updates.value.filter((msg) => !msg.is_read)
    const unreadMessagess = messages.value.filter((msg) => !msg.is_read)
    const unreadIds = [...unreadUpdates, ...unreadMessagess].map((msg) => msg.msg_recp_id)
    if (unreadIds.length > 0) {
      // update database
      await Api.patch('/notifications/read', unreadIds)
      // update local state
      for (const id of unreadIds) {
        const index = updates.value.findIndex((msg) => msg.msg_recp_id === id)

        if (index !== -1) {
          updates.value[index].is_read = true
        }
        else {
          const index = messages.value.findIndex((msg) => msg.msg_recp_id === id)
          messages.value[index].is_read = true
        }
      }

    }
  }


</script>


<style module></style>
