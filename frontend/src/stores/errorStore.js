// 用于需要在页面显示信息的情况
import { defineStore } from 'pinia'
import { ref } from 'vue'


export const useErrorStore = defineStore('error', () => {
    const message = ref(null)
    //severity: "error" | "secondary" | "info" | "success" | "warn" | "contrast"
    function setMessage(severity,summary,detail,closable=true,life=3000,group=null) {
        message.value = { severity, summary, detail, closable, life, group }
    }
    function resetMessage() {
        message.value=null
    }
    return { message, setMessage, resetMessage }
})