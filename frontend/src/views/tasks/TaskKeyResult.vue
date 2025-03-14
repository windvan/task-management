<template>
  <Dialog v-model:visible="keyResultsvisible" modal maximizable header="Key Results" :style="{ width: '80rem' }">
    <div class="flex flex-col gap-4">
      <pre>{{ currentTaskKeyResults }}</pre>
    </div>
  </Dialog>
  <Dialog v-model:visible="samplesViewVisible" modal maximizable header="Task Samples" :style="{ width: '80rem' }">
    <pre>{{ currentTaskSamples }}</pre>
  </Dialog>
</template>
