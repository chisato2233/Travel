<template>
  <div class="search-results" v-if="results.length > 0">
    <h3>搜索结果</h3>
    <div v-for="result in results" :key="result.id" class="search-result">
      <h4>{{ result.title || result.name }}</h4>
      <p>{{ result.summary || result.description }}</p>
      <p v-if="result.type">类型: {{ result.type }}</p>
      <p v-if="result.rating">评分: {{ result.rating }}</p>
      <p v-if="result.popularity">人气: {{ result.popularity }}</p>
      <p v-if="result.location">位置: {{ result.location }}</p>
      <p v-if="result.distance">距离: {{ result.distance }} 米</p>
      <p v-if="result.date">日期: {{ result.date }}</p>
      <p v-if="result.username">作者: {{ result.username }}</p>
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
      ('description' in item || 'summary' in item) &&
      (!('type' in item) || typeof item.type === 'string') &&
      (!('rating' in item) || typeof item.rating === 'number') &&
      (!('popularity' in item) || typeof item.popularity === 'number') &&
      (!('location' in item) || typeof item.location === 'string') &&
      (!('distance' in item) || typeof item.distance === 'number') &&
      (!('date' in item) || typeof item.date === 'string') &&
      (!('username' in item) || typeof item.username === 'string') &&
      (!('images' in item) || Array.isArray(item.images))
    )
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
