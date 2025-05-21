<template>
  <div>
    <div class="loader1">
      <div class="dot1"></div>
      <div class="dot1"></div>
      <div class="dot1"></div>
      <div class="dot1"></div>
      <div class="dot1"></div>
    </div>
  </div>

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
<style scoped>

  .loader1 {
    display: flex;
    align-items:center;
    justify-content: center;
    height: 100vh;
  }

  .dot1 {
    width: 24px;
    height: 24px;
    background: #3ac;
    border-radius: 100%;
    display: inline-block;
    animation: slide 1s infinite;
  }

  .dot1:nth-child(1) {
    animation-delay: 0.1s;
    background: #32aacc;
  }

  .dot1:nth-child(2) {
    animation-delay: 0.2s;
    background: #64aacc;
  }

  .dot1:nth-child(3) {
    animation-delay: 0.3s;
    background: #96aacc;
  }

  .dot1:nth-child(4) {
    animation-delay: 0.4s;
    background: #c8aacc;
  }

  .dot1:nth-child(5) {
    animation-delay: 0.5s;
    background: #faaacc;
  }

  @-moz-keyframes slide {
    0% {
      transform: scale(1);
    }

    50% {
      opacity: 0.3;
      transform: scale(2);
    }

    100% {
      transform: scale(1);
    }
  }

  @-webkit-keyframes slide {
    0% {
      transform: scale(1);
    }

    50% {
      opacity: 0.3;
      transform: scale(2);
    }

    100% {
      transform: scale(1);
    }
  }

  @-o-keyframes slide {
    0% {
      transform: scale(1);
    }

    50% {
      opacity: 0.3;
      transform: scale(2);
    }

    100% {
      transform: scale(1);
    }
  }

  @keyframes slide {
    0% {
      transform: scale(1);
    }

    50% {
      opacity: 0.3;
      transform: scale(2);
    }

    100% {
      transform: scale(1);
    }
  }

</style>