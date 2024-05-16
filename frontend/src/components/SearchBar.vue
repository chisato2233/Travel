<template>
  <div class="search-bar">
    <input type="text" v-model="query" placeholder="搜索" @focus="isFocused = true" @blur="isFocused = false">
    <button @click="$emit('search', query)">搜索</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const isFocused = ref(false);

defineEmits(['search']);
</script>

<style scoped>
.search-bar {
  margin-top: 20px;
  display: flex;
}

input[type="text"] {
  padding: 12px; /* Increase padding to make the input box bigger */
  width: 250px; /* Increase width for larger input */
  border-radius: 20px; /* Round the edges */
  border: 1px solid #ccc;
  margin-right: 10px;
  transition: border-color 0.3s; /* Smooth transition for border color change */
  outline: none; /* Remove default focus outline */
}

input[type="text"]:focus {
  border-color: #28a745; /* Green border color when focused */
}

button {
  padding: 12px 20px; /* Increase padding for larger button */
  border: none;
  border-radius: 20px; /* Round the edges */
  cursor: pointer;
  background-color: #28a745; /* Green background color */
  color: #fff;
  transition: background-color 0.3s; /* Smooth transition for background color change */
}

button:hover {
  background-color: #218838; /* Darker green on hover */
}
</style>
