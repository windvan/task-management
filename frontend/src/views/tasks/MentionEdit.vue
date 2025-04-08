<template>
  <div 
    ref="editorRef" 
    class="mention-editor"
    contenteditable="true"
    @input="handleInput"
    @keydown="handleKeydown"
    @blur="handleBlur"
  ></div>

  <div 
    v-show="showPicker && filteredUsers.length > 0"
    ref="pickerRef"
    class="mention-picker"
    :style="pickerPosition"
  >
    <div
      v-for="(user, index) in filteredUsers"
      :key="user.id"
      class="mention-item"
      :class="{ 'selected': selectedIndex === index }"
      @click="insertMention(user)"
    >
      {{ user.name }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, inject, nextTick } from 'vue';

const editorRef = ref(null);
const pickerRef = ref(null);
const showPicker = ref(false);
const selectedIndex = ref(0);
const searchText = ref('');
const pickerPosition = ref({ left: 0, top: 0 });
const Api = inject("Api"); // 注入API实例

// 双向绑定支持
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ text: '', mentions: [] })
  }
});

const emit = defineEmits(['update:modelValue']);

// 用户数据（示例）
const users = ref([]);

// 数据同步逻辑
const syncContent = () => {
  const text = editorRef.value?.innerHTML || '';
  const mentions = extractMentions();
  emit('update:modelValue', { text, mentions });
};

// 提及提取函数
const extractMentions = () => {
  if (!editorRef.value) return [];
  return [...editorRef.value.querySelectorAll('.mention-tag')]
    .map(node => ({
      id: node.dataset.userId,
      name: node.textContent.slice(1) // 移除@符号
    }));
};

// 输入处理
const handleInput = (event) => {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);
  const node = range.startContainer;
  const text = node.textContent || '';
  const offset = range.startOffset;

  // 检查是否刚输入了@符号
  if (text[offset - 1] === '@') {
    showPicker.value = true;
    searchText.value = '';
    updatePickerPosition();
    return;
  }

  // 检查现有的@搜索
  const beforeCursor = text.slice(0, offset);
  const lastAtPos = beforeCursor.lastIndexOf('@');
  
  if (lastAtPos > -1) {
    const afterAtText = beforeCursor.slice(lastAtPos + 1);
    // 检查@后是否有特殊字符或多个空格
    if (!/[^\w\s]/.test(afterAtText) && !/\s{2,}/.test(afterAtText)) {
      searchText.value = afterAtText.trim();
      showPicker.value = true;
      updatePickerPosition();
    } else {
      showPicker.value = false;
    }
  } else {
    showPicker.value = false;
  }
  
  syncContent();
};

// 初始化内容
onMounted(async () => {
  if (props.modelValue.text) {
    editorRef.value.innerHTML = props.modelValue.text;
  }
  try {
    users.value = await Api.get("/users/");
  } catch (error) {
    console.error("Failed to fetch users:", error);
    users.value = [];
  }

  window.addEventListener('scroll', updatePickerPosition, true);
  window.addEventListener('resize', updatePickerPosition);
});

onUnmounted(() => {
  window.removeEventListener('scroll', updatePickerPosition, true);
  window.removeEventListener('resize', updatePickerPosition);
});

// 用户列表过滤
const filteredUsers = computed(() => {
  return users.value.filter(user => 
    user.name.toLowerCase().includes(searchText.value.toLowerCase())
  );
});

// 光标坐标计算
const updatePickerPosition = () => {
  if (!editorRef.value) return;

  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0).cloneRange();
  const editorRect = editorRef.value.getBoundingClientRect();
  
  // 创建一个临时span来获取准确位置
  const span = document.createElement('span');
  range.insertNode(span);
  const spanRect = span.getBoundingClientRect();
  span.remove();

  // 计算相对于编辑器的位置
  const left = spanRect.left - editorRect.left;
  const top = spanRect.bottom - editorRect.top;

  // 确保选择器不会超出视口
  const maxLeft = editorRect.width - (pickerRef.value?.offsetWidth || 200);

  pickerPosition.value = {
    left: `${Math.min(Math.max(0, left), maxLeft)}px`,
    top: `${top + 5}px`
  };
};

// 键盘事件处理
const handleKeydown = (e) => {
  // 处理@快捷键
  if (e.key === '@') {
    showPicker.value = true;
    searchText.value = '';
    // 使用nextTick确保在DOM更新后计算位置
    nextTick(() => {
      updatePickerPosition();
    });
  }

  if (showPicker.value) {
    switch(e.key) {
      case 'ArrowUp':
        e.preventDefault();
        selectedIndex.value = Math.max(0, selectedIndex.value - 1);
        break;
      case 'ArrowDown':
        e.preventDefault();
        selectedIndex.value = Math.min(filteredUsers.value.length - 1, selectedIndex.value + 1);
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredUsers.value[selectedIndex.value]) {
          insertMention(filteredUsers.value[selectedIndex.value]);
        }
        break;
      case 'Escape':
        showPicker.value = false;
        break;
    }
  }
};

// 插入提及标签
const insertMention = (user) => {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);
  const node = document.createElement('span');
  
  node.className = 'mention-tag';
  node.contentEditable = 'false';
  node.dataset.userId = user.id;
  node.textContent = `@${user.name}`;
  
  // 替换@符号后的文本
  range.setStart(range.startContainer, range.startOffset - searchText.value.length - 1);
  range.deleteContents();
  range.insertNode(node);
  
  // 在提及后添加空格
  const space = document.createTextNode('\u00A0');
  range.insertNode(space);
  
  // 移动光标到空格后
  const newRange = document.createRange();
  newRange.setStartAfter(space);
  newRange.setEndAfter(space);
  selection.removeAllRanges();
  selection.addRange(newRange);
  
  // 重置状态
  showPicker.value = false;
  searchText.value = '';
  
  syncContent();
};

// 添加失焦处理
const handleBlur = (e) => {
  // 给一个小延时，确保点击选择器时能正常工作
  setTimeout(() => {
    showPicker.value = false;
  }, 200);
};
</script>

<style>
.mention-editor {
  min-height: 150px;
  border: 1px solid #ccc;
  padding: 10px;
  white-space: pre-wrap;
}

.mention-editor:empty::before {
  content: '输入@可提及用户...';
  color: #999;
}

.mention-picker {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
  min-width: 150px;
  transform-origin: top left;
  transition: opacity 0.1s ease;
  opacity: 1;
}

.mention-item {
  padding: 8px 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.mention-item:hover, .selected {
  background: #f0f0f0;
}

.mention-tag {
  color: #409eff;
  background: #e8f4ff;
  padding: 2px 4px;
  border-radius: 3px;
  margin: 0 2px;
  user-select: none;
}
</style>