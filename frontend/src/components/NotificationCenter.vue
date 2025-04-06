<template>

  <Popover ref="poRef" class="popover w-[30rem]" @hide="emit('close')">
    <!-- header -->
    <div class="flex justify-between mb-4">
      <span class="font-bold">Notifications</span>
      <Button outlined severity="secondary" class="py-0 text-sm">Mark all as read</Button>
    </div>
    <!-- category -->

    <!-- <SelectButton v-model="activeNotiCategory" :options="NotiCategory" class="w-full justify-around rou"
      :pt:pcToggleButton:root="({ context }) => {return {class: context.active ? 'bg-primary rounded-2xl' : 'bg-surface-100 rounded-2xl' } }"/> -->
    <Tabs value="0">
      <TabList>
        <Tab value="0">Reminder</Tab>
        <Tab value="1">Update</Tab>
        <Tab value="2">Message</Tab>
      </TabList>
      <TabPanels pt:root=" rounded-md pt-0  h-[30rem] overflow-auto">
        <!-- reminder -->
        <TabPanel value="0">

          <div class="shadow rounded-md p-2 bg-surface-100 my-4 flex items-center gap-4" v-for="reminder of reminders">
            <Badge :class="reminder.days_remaining <=15?'bg-red-500':'bg-orange-400'"></Badge>
            <p>
              <span>{{ `Task 【 ${reminder.project_name}_${reminder.task_name}】is expected to be delivered in `}}</span>
              <span class="font-bold" :class="reminder.days_remaining <=15?'text-red-500':'text-orange-400'">{{ `${reminder.days_remaining} days` }}</span>
            </p>
          </div>
        </TabPanel>
        <!-- update -->
        <TabPanel value="1">
         
          <div v-for="msg of messages?.updates" class="rounded border-t border-surface-300 p-3 hover:bg-surface-200">
            <!-- <div :class="{ 'font-bold': !msg.read }" class="flex justify-between">
              
              <OverlayBadge :severity="msg.severity"></OverlayBadge>
            </div> -->
            <p class="bg-surface-100 rounded-md p-2 whitespace-pre-wrap">{{ msg.content }}</p>
          </div>

        </TabPanel>
        <!-- Message -->
        <TabPanel value="2">
          <div v-for="msg of messages?.mentions" class="rounded border-t border-surface-300 p-3 hover:bg-surface-200">
            <!-- <div :class="{ 'font-bold': !msg.read }" class="flex justify-between">
              
              <OverlayBadge :severity="msg.severity"></OverlayBadge>
            </div> -->
            <p class="bg-surface-100 rounded-md p-2">{{ msg.content }}</p>
          </div>


        </TabPanel>
      </TabPanels>

    </Tabs>


  </Popover>

</template>

<script setup>
  import { useTemplateRef, ref, onMounted, inject } from "vue"

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

</script>

<style module></style>
