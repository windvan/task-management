<template>
    <Dialog v-model:visible="gapViewvisible" modal maximizable header="Gap Snapshots" :style="{ width: '80rem' }">
        <div class="flex flex-col gap-4">
            <div v-for="(gap, index) in currentTaskGaps.gapURLs" :key="index" class="border rounded-md p-2">
                <div class="flex items-center gap-4 mb-2">
                    <span>{{ index + 1 }} </span>
                    <span>{{ gap.split("/").pop() }}</span>
                    <Button icon="pi pi-times" rounded severity="warn" variant="outlined" class="size-8"
                        @click="onGapDelete(currentTaskGaps.task_id, gap)"></Button>
                </div>
                <!-- <img :src="apiBaseStaticUrl + gap" class=" max-w-full max-h-96 object-contain rounded" /> -->
                <Image :src="apiBaseStaticUrl + gap" class="h-64" preview
                    pt:originalContainer="max-w-full overflow-auto" />
            </div>
            <FileUpload name="gap_snapshot" customUpload @uploader="onGapUpload" accept="image/*"
                :maxFileSize="1048576">
                <template #empty>
                    <span>Drag and drop image to here to upload.</span>
                </template>
            </FileUpload>
            <pre>{{ currentTaskGaps }}</pre>
        </div>
    </Dialog>
</template>

<script setup>
import { ref } from 'vue';

// Define your reactive variables and functions here
const gapData = ref({});
const saveGap = () => {
    // Add your save logic here
};
</script>

<style module>

</style>