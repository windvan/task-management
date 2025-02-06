<template>
  <div class="flex flex-col items-center justify-center h-screen bg-gray-900 text-white font-sans">
    <h1 class="text-8xl mb-4 tracking-widest">
      4<span class="inline-block" :style="rotationStyle">0</span>4
    </h1>
    <p class="text-2xl mb-8">Oops! Looks like we're lost in space.</p>
    <div :class="astronautClass">👨‍🚀</div>
    <Button label="Return to Earth" icon="pi pi-home" @click="goHome" class="mb-8" />
    <Slider v-model="gravity" :min="0" :max="100" class="w-48 mb-2" />
    <p>Gravity: {{ gravity }}%</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import Slider from 'primevue/slider';

const router = useRouter();
const gravity = ref(80);

const astronautClass = computed(() => [
  'text-7xl mb-8',
  `animate-float-${Math.ceil((101 - gravity.value) / 10)}`
]);

  const rotationStyle = {
  animation: `spin ${Math.ceil((101 - gravity.value) / 10)}s linear infinite`
}

const goHome = () => {
  router.push('/');
};
</script>

<style>
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.animate-float-1 { animation: float 1s ease-in-out infinite; }
.animate-float-2 { animation: float 2s ease-in-out infinite; }
.animate-float-3 { animation: float 3s ease-in-out infinite; }
.animate-float-4 { animation: float 4s ease-in-out infinite; }
.animate-float-5 { animation: float 5s ease-in-out infinite; }
.animate-float-6 { animation: float 6s ease-in-out infinite; }
.animate-float-7 { animation: float 7s ease-in-out infinite; }
.animate-float-8 { animation: float 8s ease-in-out infinite; }
.animate-float-9 { animation: float 9s ease-in-out infinite; }
.animate-float-10 { animation: float 10s ease-in-out infinite; }


</style>