<template>
  <div class="recommendation">
    <div v-for="destination in destinations" :key="destination.id" class="destination-card">
      <img :src="destination.imageURL" alt="Destination Image" class="destination-image">
      <div class="destination-info">
        <h3>{{ destination.name }}</h3>
        <p>{{ destination.description }}</p>
        <div class="destination-meta">
          <span class="rating">评分: {{ destination.rating }}</span>
          <span class="popularity">人气: {{ destination.popularity }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  destinations: {
    type: Array,
    required: true,
    validator: (value) => Array.isArray(value) && value.every(item => 
      'id' in item &&
      'imageURL' in item &&
      'name' in item &&
      'description' in item &&
      'rating' in item &&
      'popularity' in item
    )
  }
});
</script>

<style scoped>
.recommendation {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.destination-card {
  width: calc(50% - 10px);
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
}

.destination-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.destination-info {
  padding: 10px;
}

.destination-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.rating, .popularity {
  font-weight: bold;
}
</style>
