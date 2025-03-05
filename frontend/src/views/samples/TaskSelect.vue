<template>
    <AutoComplete v-model="tasks" :suggestions="filteredTasks" field="name" @complete="searchTasks" multiple="true">
        <template #item="item">
            <div>{{ item.name }}</div>
        </template>
    </AutoComplete>
    <div>
        <h1>Task Select</h1>
        <!-- Add your template code here -->
    </div>
</template>

<script setup>
    import { AutoComplete } from 'primevue';
    import { ref } from 'vue';

    // Add your script setup code here
    const tasks = ref([]);
    async function searchTasks(event) {

        tasks.value = await Api.get(`https://api.example.com/tasks?query=${event.query}`);

    }
        // Add your search logic here
    const filteredTasks = ref([]);
</script>



<style scoped>
    /* Add your styles here */
</style>
