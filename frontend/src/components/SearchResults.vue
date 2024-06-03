<template>
  <div class="search-results" v-if="results.length > 0">
    <h3>搜索结果</h3>
    <div v-for="result in results" :key="result.id" class="search-result">
      <template v-if="selectedType === 'attractions'">
        <h4>{{ result.name }}</h4>
        <p>{{ result.description }}</p>
        <p v-if="result.category">类别: {{ result.category }}</p>
        <p v-if="result.rating">评分: {{ result.rating }}</p>
        <p v-if="result.popularity">人气: {{ result.popularity }}</p>
      </template>
      
      <template v-if="selectedType === 'facilities'">
        <h4>{{ result.name }}</h4>
        <p v-if="result.type">类型: {{ result.type }}</p>
        <p v-if="result.distance">距离: {{ result.distance }} 米</p>
      </template>
      
      <template v-if="selectedType === 'diaries'">
        <h4>{{ result.title }}</h4>
        <p>{{ result.content }}</p>
        <p v-if="result.date">日期: {{ result.date }}</p>
        <p v-if="result.author">作者: {{ result.author }}</p>
        <p v-if="result.rating">评分: {{ result.rating }}</p>
        <p v-if="result.userRating">用户评分: {{ result.userRating }}</p>
      </template>
      
      <div v-if="result.images && result.images.length > 0">
        <img v-for="image in result.images" :key="image" :src="image" :alt="result.title || result.name" class="result-image">
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  results: {
    type: Array,
    required: true,
    validator: (value) => Array.isArray(value) && value.every(item => 
      'id' in item &&
      ('name' in item || 'title' in item) &&
      ('description' in item || 'content' in item)
    )
  },
  selectedType: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.search-results {
  margin-top: 20px;
}

.search-result {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.search-result h4 {
  margin-bottom: 5px;
}

.search-result p {
  margin: 5px 0;
}

.result-image {
  max-width: 100px;
  max-height: 100px;
  margin: 5px;
}
</style>
