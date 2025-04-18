<template>
  <Dialog v-model:visible="visible" header="Associate Tasks" :modal="true" maximizable @hide="emit('close')"
    style="min-width: 50rem">
    <MultiSelect v-model="selectedTasks" :options="taskSuggestions" filter :filterFields multiple
      optionLabel="task_name" placeholder="Select Tasks" :maxSelectedLabels="0" @show="handleShowList" display="chip"
      class="w-full mb-12" filterPlaceholder="Search by product name,task name or tags">
      <template #option="{ option, index }">
        {{
          joinStrings(
            [
              index + 1,
              option.product_trade_name,
              option.product_internal_name,
              option.task_name,
              option.tags,
            ],
            " _ "
          )
        }}
      </template>
    </MultiSelect>

    <div v-if="selectedTasks?.length > 0">
      <p>Selected tasks:</p>
      <ol>
        <li v-for="(task, index) in selectedTasks" :key="index">
          {{
            joinStrings(
              [
                index + 1,
                task.product_trade_name,
                task.product_internal_name,
                task.task_name,
                task.tags,
              ],
              " _ "
            )
          }}
        </li>
      </ol>
    </div>

    <div class="flex justify-end mt-4">
      <Button label="Cancel" @click="emit('close')" class="mr-2" />
      <Button label="Save" @click="handleSave" />
    </div>
  </Dialog>
</template>

<script setup>
  import { ref, inject, onMounted } from "vue";
  import { joinStrings } from "../../composables/strTools";

  import useApi from "@/composables/useApi";;
  const Api = inject("Api")
  const visible = ref(true);
  const emit = defineEmits(["refresh", "close"]);
  const props = defineProps(["sample_id"]);

  // Add your search logic here
  const selectedTasks = ref();
  const taskSuggestions = ref();
  const filterFields = [
    "product_trade_name",
    "product_internal_name",
    "task_name",
    "tags",
  ];

  async function handleShowList() {
    taskSuggestions.value = await Api.get(
      "/tasks/search?query=&sample_id=" + props.sample_id
    );
  }
  async function handleSave() {
    await Api.post(
      `/samples/${props.sample_id}/tasks`,
      selectedTasks.value.map((task) => task.id)
    );
    emit("close");
    emit("refresh", props.sample_id);
  }
</script>

<style scoped>
  /* Add your styles here */
</style>
