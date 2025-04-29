<template>
  <Editor v-model="editorVal" :modules="modules" @textChange="handler" readonly pt:toolbar="hidden" />
  
</template>

<script setup>

  import { ref } from 'vue';

  const editorVal = ref("<p>abc <strong style='color:red;'>def</strong ></p>")
  const modules = {

    mention: {
      allowedChars: /^[A-Za-z]*$/,
      mentionDenotationChars: ["@"],
      source: function (searchTerm, renderList, mentionChar) {
        if (searchTerm.length === 0) {
          renderList(userSuggestion, searchTerm);
        } else {
          const matches = userSuggestion.filter((item) => {
            return item.value.toLowerCase().includes(searchTerm.toLowerCase());
          });
          renderList(matches, searchTerm);
        }
      },

      dataAttributes: ['id', 'value'],
      listItemClass: "p-2  rounded",
      mentionContainerClass: "rounded border border-surface-200 shadow-sm bg-surface-50",
      mentionListClass: "max-h-48 overflow-y-auto",
      offsetLeft: 20,


    }
  }

  function handler(value) {
    console.log(value)
  }

</script>
