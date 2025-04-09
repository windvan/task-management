<template>
  <div id="editor-container" class="border border-surface-200 rounded">

  </div>
</template>

<script setup>
  import Quill from "quill";
  import "quill-mention/autoregister";
  import { ref, inject, onMounted } from "vue";
  // import 'quill-mention/dist/quill.mention.css';
  import 'quill/dist/quill.snow.css';


  const modelValue = defineModel()

  const Api = inject('Api')
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
    quill = new Quill("#editor-container", {
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
          offsetLeft: 20

        }
      }
    });

    // 设置初始内容
    if (modelValue.value) {
      quill.setContents(modelValue.value)
    }

    // 监听内容变化
    quill.on('text-change', (delta, oldDelta, source) => {
   
      if (delta.ops.length === 0) {
        return
      }
      
      modelValue.value.content = quill.getContents()
      for (const op of delta.ops) {
        if (op.insert?.mention) {
          const mention = op.insert.mention
      
          modelValue.value.mentions.push(parseInt(mention.id))
          // 这里可以处理提及的用户信息
          // 比如：modelValue.value.mentions.push(mention)
        }
      }
    })
  })
</script>

<style>

  .mention {
    background-color: #d3e1eb;
    border-radius: 3px;
    margin-right: 2px;
    padding: 2px 2px;
    user-select: all;
  }

  #editor-container>.ql-editor {
    min-height: 200px;
  }

  #quill-mention-list>.selected {
    background-color: #d3e1eb;
  }

</style>