<template>
  <Drawer
    v-model:visible="visible"
    @hide="emit('close')"
    :position="position"
    class="w-[40rem]"
    pt:content="overflow-hidden">
    <template #header>
      <div class="flex items-center justify-between w-full gap-2">
        <span class="font-bold text-xl">Comments</span>
        <Button
          label="Add Comment"
          icon="pi pi-plus"
          size="small"
          outlined
          @click="handleShowNewComment"
          v-if="!showNewComment"></Button>
        <Button
          severity="secondary"
          variant="text"
          :icon="
            'pi pi-window-' + (position === 'full' ? 'minimize' : 'maximize')
          "
          @click="togglePosition"></Button>
      </div>
    </template>

    <form class="flex flex-col gap-2 p-4" v-if="showNewComment">
      <div class="flex gap-1">
        <Select
          name="severity"
          v-model="newComment.severity"
          :options="enums.NoteSeverityEnum"
          placeholder="severity"
          size="small">
          <template #value="{ value, placeholder }">
            <div v-if="value" class="flex items-center">
              <i :class="['pi pi-circle-fill', getCommentSeverity(value)]" />
              <span class="ml-2">{{ value }}</span>
            </div>
            <span v-else>
              {{ placeholder }}
            </span>
          </template>
          <template #option="{ option }">
            <div class="flex items-center text-sm">
              <i :class="['pi pi-circle-fill', getCommentSeverity(option)]" />
              <span class="ml-2">{{ option }}</span>
            </div>
          </template>
        </Select>
        <div
          class="p-inputtext p-inputtext-sm flex items-center gap-2 bg-surface-100">
          <i :class="id_type === 'project' ? 'pi pi-folder' : 'pi pi-list'" />
          <span>{{
            id_type === "project" ? "Project Comment" : "Task Comment"
          }}</span>
        </div>

        <AutoComplete
          name="tags"
          v-model="newComment.tags"
          placeholder="#Tags"
          size="small"
          class="grow text-primary"
          pt:pcInputText:root="w-full"></AutoComplete>
      </div>
      <div class="relative">
        <Textarea
          id="textareaId"
          name="content"
          v-model="newComment.content"
          autoResize
          class="min-h-40 w-full relative"
          :class="{ 'has-mentions': showMentions }"
          @input="handleInput"
          @keydown="handleKeydown"></Textarea>
        

        <!-- Mention suggestions overlay -->
        <div
          v-if="showMentions"
          class="absolute z-10"
          :style="mentionListStyle">
          <div
            v-for="user in filteredUsers"
            :key="user.id"
            @click="selectMention(user)"
            class="p-2 hover:bg-surface-100 cursor-pointer">
            {{ user.name }}
          </div>
        </div>
      </div>
      <MentionEdit v-model="newComment.content"></MentionEdit>
      <div class="flex gap-4 justify-center">
        <Button
          label="Cancel"
          icon="pi pi-times"
          size="small"
          outlined
          @click="handleHideNewComment"></Button>
        <Button
          label="Save"
          icon="pi pi-save"
          size="small"
          outlined
          @click="handleCreateComment"></Button>
      </div>
    </form>

    <Tabs v-else v-model:value="activeTab">
      <TabList>
        <Tab value="0">Project</Tab>
        <Tab value="1">Tasks</Tab>
      </TabList>
      <TabPanels pt:root="pl-0 pr-2" class="h-dvh overflow-auto">
        <TabPanel value="0">
          <div
            v-for="comment in comments?.project_notes"
            key="comment.id"
            class="border border-surface-200 rounded mb-6 p-2 bg-surface-50">
            <div class="flex gap-2">
              <span class="font-bold">{{ comment.created_by_name }}</span>
              <span>{{
                new Date(comment.updated_at + "Z").toLocaleDateString()
              }}</span>
              <span class="text-primary mx-auto"> {{ comment.tags }}</span>
              <Select
                v-model="comment.severity"
                :options="enums.NoteSeverityEnum"
                placeholder="severity"
                size="small"
                class="border-none bg-surface-50"
                pt:dropdown="hidden"
                @change="handelChangeSeverity(comment)">
                <template #value="{ value, placeholder }">
                  <div v-if="value" class="flex items-center">
                    <i
                      :class="[
                        'pi pi-circle-fill',
                        getCommentSeverity(value),
                      ]" />
                    <!-- <span class="ml-2">{{ value }}</span> -->
                  </div>
                  <span v-else>
                    {{ placeholder }}
                  </span>
                </template>
                <template #option="{ option }">
                  <div class="flex items-center">
                    <i
                      :class="[
                        'pi pi-circle-fill',
                        getCommentSeverity(option),
                      ]" />
                    <span class="ml-2">{{ option }}</span>
                  </div>
                </template>
              </Select>
            </div>
            <!-- <Textarea v-model="comment.content" fluid></Textarea> -->
            <div
              class="px-2 whitespace-pre-wrap"
              v-html="formatCommentContent(comment.content)"></div>
          </div>
        </TabPanel>
        <TabPanel value="1">
          <div
            v-for="comment in comments?.task_notes"
            key="comment.id"
            class="border border-surface-200 rounded mb-6 p-2 bg-surface-50">
            <div class="flex gap-2">
              <span class="font-bold">{{ comment.created_by_name }}</span>
              <span>{{
                new Date(comment.updated_at + "Z").toLocaleDateString()
              }}</span>
              <span class="text-primary mx-auto"> {{ comment.tags }}</span>
              <Select
                v-model="comment.severity"
                :options="enums.NoteSeverityEnum"
                placeholder="severity"
                size="small"
                class="border-none bg-surface-50"
                pt:dropdown="hidden"
                @change="handelChangeSeverity(comment)">
                <template #value="{ value, placeholder }">
                  <div v-if="value" class="flex items-center">
                    <i
                      :class="[
                        'pi pi-circle-fill',
                        getCommentSeverity(value),
                      ]" />
                    <!-- <span class="ml-2">{{ value }}</span> -->
                  </div>
                  <span v-else>
                    {{ placeholder }}
                  </span>
                </template>
                <template #option="{ option }">
                  <div class="flex items-center">
                    <i
                      :class="[
                        'pi pi-circle-fill',
                        getCommentSeverity(option),
                      ]" />
                    <span class="ml-2">{{ option }}</span>
                  </div>
                </template>
              </Select>
            </div>
            <!-- <Textarea v-model="comment.content" fluid></Textarea> -->
            <div
              class="px-2 whitespace-pre-wrap"
              v-html="formatCommentContent(comment.content)"></div>
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>
    <!-- <template #footer>
      <div class="flex items-center gap-2">
        <Button label="Add Comment" icon="pi pi-plus" class="flex-auto" outlined></Button>
      </div>
    </template> -->
  </Drawer>
</template>

<script setup>
  import { useToast } from "primevue";
  import {
    ref,
    watch,
    inject,
    onMounted,
    computed,
    nextTick,
    useTemplateRef,
  } from "vue";
  import MentionEdit from "./MentionEdit.vue";

  // whether the drawer is triggered from task or project
  const { trigger_id, id_type } = defineProps({
    trigger_id: {
      type: Number,
      required: false,
    },
    id_type: {
      type: String,
      required: false,
      validator: (value) => ["task", "project"].includes(value),
    },
  });
  const emit = defineEmits(["close"]);
  const visible = ref(true);
  const activeTab = ref(id_type === "task" ? "1" : "0");
  const position = ref("right");
  function togglePosition() {
    position.value = position.value === "full" ? "right" : "full";
  }

  // #region new comment
  // import { useAuthStore } from "@/stores/auth";
  // const {currentUser} = useAuthStore();
  const showNewComment = ref(false);
  const toast = useToast();
  const Api = inject("Api");

  const newComment = ref();

  const enums = JSON.parse(localStorage.getItem("cachedEnums")) || {};
  function handleShowNewComment() {

    let defalut = {};
    defalut[id_type === "task" ? "task_id" : "project_id"] = trigger_id;
    defalut["severity"] = "Info";
    newComment.value = defalut;
    showNewComment.value = true;
  }
  function handleHideNewComment() {
    showNewComment.value = false;
  }
  function getCommentSeverity(severity) {
    switch (severity) {
      case "Danger":
        return "text-red-600";
      case "Warning":
        return "text-orange-400";
      case "Info":
        return "text-green-600";
      default:
        return "text-green-60";
    }
  }

  const showMentions = ref(false);
  const users = ref([]);
  const filteredUsers = ref([]);
  const currentMentionStart = ref(-1);
  const currentMentionText = ref("");

  const caretCoords = ref({ x: 0, y: 0 });

  const getCaretCoordinates = () => {
    // 等待 DOM 更新后获取 textarea
    return new Promise((resolve) => {
      nextTick(() => {
        const textarea = document.querySelector("#textareaId");
        if (!textarea) {
          console.log("No textarea found");
          resolve(null);
          return;
        }

        // 获取textarea的位置信息
        const textareaRect = textarea.getBoundingClientRect();
        const paddingLeft = parseInt(getComputedStyle(textarea).paddingLeft);
        const paddingTop = parseInt(getComputedStyle(textarea).paddingTop);
        const lineHeight = parseInt(getComputedStyle(textarea).lineHeight);

        // 获取当前光标位置前的文本
        const text = textarea.value;
        const caretPos = textarea.selectionStart;
        const textBeforeCaret = text.substring(0, caretPos);

        // 计算光标位置
        const lines = textBeforeCaret.split("\n");
        const currentLineNumber = lines.length;
        const currentLine = lines[lines.length - 1];

        // 创建测量用的临时元素
        const span = document.createElement("span");
        span.style.cssText = `
          position: absolute;
          visibility: hidden;
          white-space: pre;
          font: ${getComputedStyle(textarea).font}
        `;
        span.textContent = currentLine;
        document.body.appendChild(span);

        // 计算坐标
        const offsetX = span.offsetWidth;
        document.body.removeChild(span);

        const x = offsetX + paddingLeft;
        const y = (currentLineNumber - 1) * lineHeight + paddingTop;

        console.log("Calculated coordinates:", { x, y, textareaRect });

        resolve({
          x,
          y,
          textareaRect,
        });
      });
    });
  };

  const mentionListStyle = computed(() => {
    // 默认样式
    const baseStyle = {
      position: "absolute",
      maxHeight: "140px",
      minWidth: "200px",
      backgroundColor: "white",
      border: "1px solid #ddd",
      borderRadius: "4px",
      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
      overflowY: "auto",
      zIndex: 1000,
    };

    if (!showMentions.value) {
      return { ...baseStyle, display: "none" };
    }

    return {
      ...baseStyle,
      left: `${caretCoords.value.x}px`,
      top: `${caretCoords.value.y + 30}px`,
    };
  });

  const loadUsers = async () => {
    try {
      const response = await Api.get("/users/");
      users.value = response;
    } catch (error) {
      console.error("Failed to load users:", error);
    }
  };

  onMounted(async () => {
    try {
      await loadUsers();
      console.log("Users loaded:", users.value); // 调试日志
      comments.value = await Api.get(`/notes/${id_type}/${trigger_id}`);
    } catch (error) {
      console.error("Error loading users:", error);
    }
  });

  const handleInput = async (event) => {
    const textarea = event.target;
    const text = textarea.value;
    const caretPosition = textarea.selectionStart;

    console.log("Input event:", { text, caretPosition });

    const lastAtSign = text.lastIndexOf("@", caretPosition - 1);

    if (lastAtSign !== -1) {
      const textAfterAt = text.slice(lastAtSign + 1, caretPosition);
      console.log("Found @ symbol:", { lastAtSign, textAfterAt });

      if (!/\s/.test(textAfterAt)) {
        currentMentionStart.value = lastAtSign;
        currentMentionText.value = textAfterAt;

        if (users.value?.length > 0) {
          filteredUsers.value = users.value.filter((user) =>
            user.name.toLowerCase().includes(textAfterAt.toLowerCase())
          );

          if (filteredUsers.value.length > 0) {
            // 获取新的坐标
            const coords = await getCaretCoordinates();
            if (coords) {
              caretCoords.value = coords;
              showMentions.value = true;
            }
          }
        }
        return;
      }
    }

    showMentions.value = false;
  };

  const isInMentionRange = (position) => {
    const text = newComment.value.content;
    const beforeCaret = text.substring(0, position);
    const lastAtIndex = beforeCaret.lastIndexOf("@");

    if (lastAtIndex === -1) return false;

    // 检查光标是否在@mention附近
    const currentPosition = position - lastAtIndex;
    if (currentPosition > 30) return false; // 如果光标距离@太远，不处理

    // 检查这个@后面是否跟着[数字:文本]格式
    const afterAt = text.substring(lastAtIndex);
    const mentionMatch = afterAt.match(/^@<<(\d+)>>([^<\s]+)(?:\s|$)/);

    if (!mentionMatch) return false;

    // 确保光标在@mention范围内
    const mentionLength = mentionMatch[0].length;
    if (currentPosition > mentionLength) return false;

    // 返回@mention的范围
    return {
      start: lastAtIndex,
      end: lastAtIndex + mentionLength,
      userId: mentionMatch[1],
      userName: mentionMatch[2],
    };
  };

  const handleKeydown = (event) => {
    if (event.key === "Backspace") {
      const caretPos = event.target.selectionStart;
      const mentionRange = isInMentionRange(caretPos);

      if (mentionRange) {
        // 如果光标在@mention范围内，删除整个@mention
        event.preventDefault();
        const content = newComment.value.content;
        newComment.value.content =
          content.slice(0, mentionRange.start) +
          content.slice(mentionRange.end);
        // 设置光标位置到删除后的位置
        nextTick(() => {
          event.target.selectionStart = event.target.selectionEnd =
            mentionRange.start;
        });
      }
    } else if (event.key === "Escape" && showMentions.value) {
      showMentions.value = false;
      event.preventDefault();
    }
  };

  const selectMention = (user) => {
    const content = newComment.value.content;
    const beforeMention = content.slice(0, currentMentionStart.value);
    const afterMention = content.slice(
      currentMentionStart.value + currentMentionText.value.length + 1
    );

    // 使用新的格式: @<<userId>>userName
    newComment.value.content = `${beforeMention}@<<${user.id}>>${user.name} ${afterMention}`;

    showMentions.value = false;

    // 保持焦点并将光标移动到mention后面
    nextTick(() => {
      const textarea = document.querySelector("#textareaId");
      if (textarea) {
        textarea.focus();
        const newPosition =
          currentMentionStart.value + `@<<${user.id}>>${user.name} `.length;
        textarea.setSelectionRange(newPosition, newPosition);
      }
    });
  };

  async function handleCreateComment() {
    if (!newComment.value?.content?.trim()) {
      toast.add({
        severity: "error",
        summary: "Error",
        detail: "Please input comment content",
        life: 3000,
      });
      return;
    }

    const mentions = [];
    // 修改正则表达式以匹配新格式
    const mentionRegex = /@<<(\d+)>>([^<\s]+)(?:\s|$)/g;
    let match;

    while ((match = mentionRegex.exec(newComment.value.content)) !== null) {
      mentions.push({
        user_id: parseInt(match[1]),
        name: match[2],
      });
    }

    // 转换内容中的@mentions为后端格式
    const content = newComment.value.content.replace(
      /@<<(\d+)>>([^<\s]+)(?:\s|$)/g,
      "@[$1:$2] "
    );

    const commentData = {
      ...newComment.value,
      content,
      mentions: mentions,
    };

    const dbNewComment = await Api.post("/notes/", commentData);
    if (dbNewComment.project_id) {
      comments.value.project_notes.unshift(dbNewComment);
    } else {
      comments.value.task_notes.unshift(dbNewComment);
    }
    showNewComment.value = false;
  }

  async function handelChangeSeverity(comment) {
    try {
      await Api.patch(
        `/notes/${comment.id}`,
        { severity: comment.severity },
        { skipInterceptor: true }
      );
    } catch (error) {
      toast.add({
        severity: "error",
        summary: "Update severity Failed",
        detail: error.message,
        life: 3000,
      });
    }
  }

  const formatCommentContent = (content) => {
    return content.replace(/@\[(\d+):([^\]]+)\]\s/g, "@$2 ");
  };

  watch(
    () => showNewComment.value,
    (newVal) => {
      if (newVal) {
        if (!newComment.value) {
          newComment.value = {
            [id_type === "task" ? "task_id" : "project_id"]: trigger_id,
            severity: "Info",
            content: "",
          };
        }
      }
    }
  );

  // #endregion new comment

  // #region comment list
  const comments = ref();

  // #endregion comment list
</script>

<style scoped>
  .mention-suggestions {
    position: absolute;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    max-height: 140px;
    overflow-y: auto;
  }

  .mention-item {
    padding: 4px 8px;
    cursor: pointer;
  }

  .mention-item:hover {
    background-color: #f0f0f0;
  }

  /* 移除之前的 mentions-list 样式，改用 JS 动态计算 */
  :deep(.p-inputtextarea) {
    position: relative !important;
  }

  .relative {
    position: relative !important;
  }

  /* 确保mentions容器相对于父元素定位 */
  .mentions-list {
    position: absolute !important;
    z-index: 1000;
  }

  /* 添加@mention的样式 */
  .mention {
    color: #2196f3;
    background-color: rgba(33, 150, 243, 0.1);
    padding: 0 4px;
    border-radius: 4px;
    white-space: nowrap;
  }
</style>
