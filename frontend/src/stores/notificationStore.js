import { computed, ref, onUnmounted } from 'vue'
import { defineStore } from 'pinia'
import useApi from '../composables/useApi'

export const useNotificationStore = defineStore('notification', () => {
    const Api = useApi()
    const reminders = ref([])
    const updates = ref([])
    const messages = ref([])
    let checkInterval = null

    const hasNotification = computed(() => {
        return reminders.value?.length > 0 || 
               updates.value?.length > 0 || 
               messages.value?.length > 0
    })
    
    async function getNotifications() {
        try {
            const [newReminders, newUpdates, newMessages] = await Promise.all([
                Api.get('/notifications/reminders/'),
                Api.get('/notifications/updates/'),
                Api.get('/notifications/messages/')
            ])
            
            reminders.value = newReminders
            updates.value = newUpdates
            messages.value = newMessages
        } catch (error) {
            console.error('Failed to fetch notifications:', error)
        }
    }

    function hasChanges(oldData, newData) {
        return JSON.stringify(oldData) !== JSON.stringify(newData)
    }

    async function backgroundCheck() {
        const [newReminders, newUpdates, newMessages] = await Promise.all([
            Api.get('/notifications/reminders/'),
            Api.get('/notifications/updates/'),
            Api.get('/notifications/messages/')
        ])

        if (hasChanges(reminders.value, newReminders) ||
            hasChanges(updates.value, newUpdates) ||
            hasChanges(messages.value, newMessages)) {
            
            reminders.value = newReminders
            updates.value = newUpdates
            messages.value = newMessages
        }
    }

    // Start background checking
    function startBackgroundCheck(interval = 120000) {
        checkInterval = setInterval(backgroundCheck, interval)
    }

    // Stop background checking
    function stopBackgroundCheck() {
        if (checkInterval) {
            clearInterval(checkInterval)
            checkInterval = null
        }
    }

    // Initial fetch
    getNotifications()
    startBackgroundCheck()

    // Cleanup on unmount
    onUnmounted(() => {
        stopBackgroundCheck()
    })

    return { 
        reminders, 
        updates, 
        messages, 
        hasNotification, 
        getNotifications, 
        startBackgroundCheck, 
        stopBackgroundCheck 
    }
})