<template>
  <div class="my-2">
    <!-- <div id="toolbar-container"></div> -->
    <div :id="uid" class="border border-surface-200 "></div>
  </div>
</template>

<script setup>
  import Quill from "quill";
  import "quill-mention/autoregister";
  import { inject, onMounted } from "vue";
  // import 'quill-mention/dist/quill.mention.css';
  import 'quill/dist/quill.snow.css';

  const Api = inject("Api")
  defineExpose({ reset });

  const uid = generateUniqueId()
  const modelValue = defineModel()
  // modelValue schema:
  // {
  //     plain_text: null,
  //     rich_text: null,
  //     mentions: []
  // }


  let userSuggestion = []
  let quill

  onMounted(async () => {

    const user_list = await Api.get('/users/')
    userSuggestion = user_list.map((user) => {
      return {
        id: user.id,
        value: user.name,
        role: user.role,
        email: user.email
      }
    })

    // Initialize Quill after DOM is mounted
    quill = new Quill("#" + uid, {
      placeholder: 'typing @ for mentions',
      theme: "snow",
      modules: {
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
    });


    // 设置初始内容
    if (modelValue.value) {
      quill.setContents(modelValue.value.plain_text)
    }

    // 监听内容变化
    quill.on('text-change', (delta, oldDelta, source) => {

      if (delta.ops.length === 0) {
        return
      }

      modelValue.value.rich_text = quill.getContents()
      modelValue.value.plain_text = extractTextFromHTML(quill.getSemanticHTML().replace(/\uFEFF|&#xFEFF;/g, ''))

      for (const op of delta.ops) {
        if (op.insert?.mention) {
          // 这里可以处理提及的用户信息
          const mention = op.insert.mention
          modelValue.value.mentions.push(parseInt(mention.id))

        }
      }
    })

    quill.focus()
  })

  function extractTextFromHTML(htmlString) {
    // quill.getText() will not contain mention text
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    return doc.body.textContent
  }
  function generateUniqueId() {
    const timestamp = new Date().getTime();
    const randomString = Math.random().toString(36).substring(2, 15);
    return `id-${timestamp}-${randomString}`;
  }

  function reset() {
    if (quill) {
      quill.setContents([]);
      modelValue.value = {
        plain_text: null,
        rich_text: null,
        mentions: []
      }
    }
  }

</script>

<style>

  .mention {
    background-color: #d3e1eb;
    border-radius: 3px;
    margin-right: 2px;
    padding: 2px 2px;
    user-select: all;
  }

  .ql-container>.ql-editor {
    min-height: 150px;
    background-color: white;
    border-radius: 2px;
  }

  #quill-mention-list>.selected {
    background-color: #d3e1eb;
  }

</style>