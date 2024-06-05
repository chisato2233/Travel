<template>
  <div class="search-bar">
    <div class="toolbar">
      <select v-model="selectedType" @change="handleTypeChange" class="input-select">
        <option value="attractions">景点</option>
        <option value="facilities">附近设施</option>
        <option value="diaries">日记</option>
      </select>
    </div>
    <div class="search-section">
      <div class="filter-card">
        <div class="filter-header" @click="toggleFilterCard">
          <span>筛选选项</span>
          <span>{{ isFilterCardOpen ? '▲' : '▼' }}</span>
        </div>
        <transition name="slide-fade">
          <div v-if="isFilterCardOpen" class="additional-inputs">
            <!-- 景点相关输入框 -->
            <div v-if="selectedType === 'attractions'">
              <input type="number" v-model="rating" placeholder="评分" min="0" max="5" step="0.1" class="rounded-input">
              <input type="number" v-model="popularity" placeholder="人气" class="rounded-input">
              <select v-model="category" class="input-select">
                <option value="">不排序</option>
                <option value="rating">评分</option>
                <option value="popularity">人气</option>
              </select>
            </div>

            <!-- 附近设施相关输入框 -->
            <div v-if="selectedType === 'facilities'">
              <select v-model="type" class="input-select">
                <option value="" disabled>请选择设施类型</option>
                <option value="supermarket">超市</option>
                <option value="wc">卫生间</option>
                <option value="restaurant">餐厅</option>
                <option value="node">游览点</option>
                <option value="others">其他</option>
              </select>
              <input type="number" v-model="radius" placeholder="搜索半径 (米)" min="0" class="rounded-input">
            </div>

            <!-- 日记相关输入框 -->
            <div v-if="selectedType === 'diaries'">
              <input type="number" v-model="userId" placeholder="用户ID" class="input-text">
              <input type="date" v-model="startDate" placeholder="起始日期" class="input-text">
              <input type="date" v-model="endDate" placeholder="结束日期" class="input-text">
              <div class="rating-sort">
                <label>
                  <input type="checkbox" v-model="isSortByRating" class="pingfenpaixu"> 按评分排序
                </label>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div class="search-input-section">
        <input type="text" v-model="query" :placeholder="placeholderText" @focus="isFocused = true"
          @blur="isFocused = false" class="input-text">
        <button @click="handleSearch" class="search-button" :disabled="isSearchButtonDisabled">搜索</button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, defineEmits, watch } from 'vue';

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

const isFilterCardOpen = ref(false); // 控制筛选框的展开和折叠

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
      location: query.value, // location is now based on the query
      radius: radius.value,
    };
  } else if (selectedType.value === 'diaries') {
    params = {
      keywords: query.value, // keywords are now based on the query
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
  clearInputs();
  emit('updateSearchType', selectedType.value);
  handleSearch(); // Immediately perform search on type change
};

// 清空输入框
const clearInputs = () => {
  query.value = '';
  category.value = '';
  rating.value = '';
  popularity.value = '';
  type.value = '';
  location.value = '';
  radius.value = '';
  userId.value = '';
  diaryKeywords.value = '';
  startDate.value = '';
  endDate.value = '';
  isSortByRating.value = false;
};

// 切换筛选框的展开和折叠
const toggleFilterCard = () => {
  isFilterCardOpen.value = !isFilterCardOpen.value;
};

// 动态计算搜索框的提示文本
const placeholderText = computed(() => {
  if (selectedType.value === 'attractions') {
    return '搜索景点名称';
  } else if (selectedType.value === 'facilities') {
    return '搜索您的位置';
  } else if (selectedType.value === 'diaries') {
    return '搜索关键词';
  }
  return '搜索';
});

// 计算搜索按钮的禁用状态
const isSearchButtonDisabled = computed(() => {
  return query.value.trim() === '';
});

watch(selectedType, (newType) => {
  clearInputs();
  emit('updateSearchType', newType);
});
</script>
<style scoped>
.search-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.toolbar {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 10px;
}

.input-select {
  margin: 0 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #f8f8f8;
}

.input-select:focus {
  border-color: #007BFF;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.search-section {
  display: flex;
  width: 100%;
}

.filter-card {
  flex: 1;
  max-width: 200px;
  margin-right: 20px;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border-radius: 5px;
  margin-bottom: 10px;
  transition: background-color 0.3s;
}

.filter-header:hover {
  background-color: #0056b3;
}

.additional-inputs {
  display: flex;
  flex-direction: column;
}

.input-text,
.rounded-input {
  width: 100%;
  margin: 5px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #f8f8f8;
}

.input-text:focus,
.rounded-input:focus {
  border-color: #007BFF;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.search-input-section {
  flex: 3;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.search-button {
  width: 100%;
  padding: 10px 20px;
  margin-top: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #0056b3;
}

.search-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
