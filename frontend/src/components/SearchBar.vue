<template>
  <div class="search-bar">
    <select v-model="selectedType" @change="handleTypeChange" class="input-select">
      <option value="attractions">景点</option>
      <option value="facilities">附近设施与美食</option>
      <option value="diaries">日记</option>
    </select>
    <input type="text" v-model="query" placeholder="搜索" @focus="isFocused = true" @blur="isFocused = false" class="input-text">

    <!-- 景点相关输入框 -->
    <div v-if="selectedType === 'attractions'" class="additional-inputs">
      <input type="text" v-model="category" placeholder="类别" class="input-text">
      <input type="text" v-model="keywords" placeholder="关键词" class="input-text">
      <input type="number" v-model="rating" placeholder="评分" min="0" max="5" step="0.1" class="rounded-input">
      <input type="number" v-model="popularity" placeholder="人气" class="rounded-input">
    </div>

    <!-- 附近设施与美食相关输入框 -->
    <div v-if="selectedType === 'facilities'" class="additional-inputs">
      <input type="number" v-model="locationId" placeholder="位置ID" required class="input-text">
      <input type="text" v-model="type" placeholder="设施类型" required class="input-text">
      <input type="number" v-model="radius" placeholder="搜索半径" min="0" class="rounded-input">
    </div>

    <!-- 日记相关输入框 -->
    <div v-if="selectedType === 'diaries'" class="additional-inputs">
      <input type="number" v-model="userId" placeholder="用户ID" class="input-text">
      <input type="text" v-model="diaryKeywords" placeholder="关键词" class="input-text">
      <input type="date" v-model="startDate" placeholder="起始日期" class="input-text">
      <input type="date" v-model="endDate" placeholder="结束日期" class="input-text">
    </div>

    <button @click="handleSearch" class="search-button">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const isFocused = ref(false);
const selectedType = ref('attractions');

// 景点相关状态
const category = ref('');
const keywords = ref('');
const rating = ref('');
const popularity = ref('');

// 附近设施与美食相关状态
const locationId = ref('');
const type = ref('');
const radius = ref(500); // 默认搜索半径为500米

// 日记相关状态
const userId = ref('');
const diaryKeywords = ref('');
const startDate = ref('');
const endDate = ref('');

const emit = defineEmits(['search', 'updateSearchType', 'updateSearchParams']);

const handleSearch = () => {
  let params = {};
  if (selectedType.value === 'attractions') {
    params = {
      category: category.value,
      keywords: keywords.value,
      rating: rating.value,
      popularity: popularity.value,
    };
  } else if (selectedType.value === 'facilities') {
    params = {
      locationId: locationId.value,
      type: type.value,
      radius: radius.value,
    };
  } else if (selectedType.value === 'diaries') {
    params = {
      userId: userId.value,
      keywords: diaryKeywords.value,
      startDate: startDate.value,
      endDate: endDate.value,
    };
  }
  emit('search', query.value);
  emit('updateSearchParams', params);
};

const handleTypeChange = () => {
  emit('updateSearchType', selectedType.value);
};
</script>

<style scoped>
.search-bar {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.input-select, .input-text, .rounded-input {
  padding: 12px;
  border-radius: 20px;
  border: 1px solid #ccc;
  transition: border-color 0.3s;
  outline: none;
  width: 100%; /* Full width to ensure responsiveness */
  max-width: 400px; /* Max width for better aesthetics */
  box-sizing: border-box;
}

.input-select:focus, .input-text:focus, .rounded-input:focus {
  border-color: #28a745;
}

.rounded-input {
  border-radius: 20px; /* Round the edges completely */
}

.search-button {
  padding: 12px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  background-color: #28a745;
  color: #fff;
  transition: background-color 0.3s;
  white-space: nowrap; /* Ensure text stays in one line */
  width: 100%;
  max-width: 200px; /* Button width for better aesthetics */
}

.search-button:hover {
  background-color: #218838;
}

.additional-inputs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  width: 100%;
}
</style>
