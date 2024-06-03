<template>
  <div class="search-bar">
    <select v-model="selectedType" @change="handleTypeChange" class="input-select">
      <option value="attractions">景点</option>
      <option value="facilities">附近设施</option>
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

    <!-- 附近设施相关输入框 -->
    <div v-if="selectedType === 'facilities'" class="additional-inputs">
      <select v-model="type" class="input-select">
        <option value="" disabled>请选择设施类型</option>
        <option value="supermarket">超市</option>
        <option value="wc">卫生间</option>
        <option value="restaurant">餐厅</option>
        <option value="node">游览点</option>
        <option value="others">其他</option>
      </select>
      <input type="text" v-model="location" placeholder="当前位置" class="input-text">
      <input type="number" v-model="radius" placeholder="搜索半径 (米)" min="0" class="rounded-input">
    </div>

    <!-- 日记相关输入框 -->
    <div v-if="selectedType === 'diaries'" class="additional-inputs">
      <input type="number" v-model="userId" placeholder="用户ID" class="input-text">
      <input type="text" v-model="diaryKeywords" placeholder="关键词" class="input-text">
      <input type="date" v-model="startDate" placeholder="起始日期" class="input-text">
      <input type="date" v-model="endDate" placeholder="结束日期" class="input-text">
      <div class="rating-sort">
        <label>
          <input type="checkbox" v-model="isSortByRating" class="pingfenpaixu"> 按评分排序
        </label>
      </div>
    </div>

    <button @click="handleSearch" class="search-button" :disabled="isSearchButtonDisabled">搜索</button>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue';

const query = ref('');
const isFocused = ref(false);
const selectedType = ref('attractions');

// 景点相关状态
const category = ref('');
const keywords = ref('');
const rating = ref('');
const popularity = ref('');

// 附近设施相关状态
const type = ref('');
const location = ref('');
const radius = ref('');

// 日记相关状态
const userId = ref('');
const diaryKeywords = ref('');
const startDate = ref('');
const endDate = ref('');
const isSortByRating = ref(false);

const emit = defineEmits(['search', 'updateSearchType', 'updateSearchParams']);

const handleSearch = () => {
  let params = {};

  if (selectedType.value === 'attractions') {
    params = {
      name: query.value,
      category: category.value,
      rating: rating.value,
      popularity: popularity.value,
    };
  } else if (selectedType.value === 'facilities') {
    params = {
      type: type.value,
      location: location.value,
      radius: radius.value,
    };
  } else if (selectedType.value === 'diaries') {
    params = {
      keywords: diaryKeywords.value,
      isSortByRating: isSortByRating.value,
      userId: userId.value,
      startDate: startDate.value,
      endDate: endDate.value,
    };
  }

  emit('search', query.value);
  emit('updateSearchType', selectedType.value);
  emit('updateSearchParams', params);
};

const handleTypeChange = () => {
  emit('updateSearchType', selectedType.value);
};

// 计算属性：检查是否禁用搜索按钮
const isSearchButtonDisabled = computed(() => {
  return !(
    query.value || category.value || keywords.value || rating.value || popularity.value ||
    type.value || location.value || radius.value || userId.value || diaryKeywords.value || startDate.value || endDate.value
  );
});
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
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
}

.input-select:focus, .input-text:focus, .rounded-input:focus {
  border-color: #28a745;
}

.rounded-input {
  border-radius: 20px;
}

.search-button {
  padding: 12px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  background-color: #28a745;
  color: #fff;
  transition: background-color 0.3s;
  white-space: nowrap;
  width: 100%;
  max-width: 200px;
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

.rating-sort {
  width: 100%;
  display: flex;
  justify-content: center;
}

label {
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>

