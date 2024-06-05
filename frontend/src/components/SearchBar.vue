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
      <input type="number" v-model="rating" placeholder="评分" min="0" max="5" step="0.1" class="rounded-input">
      <input type="number" v-model="popularity" placeholder="人气" class="rounded-input">
      <select v-model="category" class="input-select">
        <option value="">排序类别</option>
        <option value="rating">评分</option>
        <option value="popularity">人气</option>
      </select>
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

// 计算搜索按钮的禁用状态
const isSearchButtonDisabled = computed(() => {
  if (selectedType.value === 'attractions') {
    return query.value.trim() === '' && category.value === '' && rating.value === '' && popularity.value === '';
  } else if (selectedType.value === 'facilities') {
    return type.value === '' && location.value.trim() === '' && radius.value === '';
  } else if (selectedType.value === 'diaries') {
    return diaryKeywords.value.trim() === '' && !isSortByRating.value && userId.value.trim() === '' && startDate.value === '' && endDate.value === '';
  }
  return false;
});

</script>

<style scoped>
.search-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-select, .input-text, .rounded-input, .search-button {
  margin: 5px;
}

.input-select {
  padding: 5px;
  border-radius: 5px;
}

.input-text {
  padding: 5px;
  border-radius: 5px;
}

.rounded-input {
  padding: 5px;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  border-radius: 5px;
  background-color: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
}

.search-button:disabled {
  background-color: #CCC;
  cursor: not-allowed;
}

.additional-inputs {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-sort {
  display: flex;
  align-items: center;
}

.pingfenpaixu {
  margin-left: 5px;
}
</style>
