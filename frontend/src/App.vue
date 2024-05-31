<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

// 在页面加载后导航到HomePage组件
onMounted(() => {
  const router = useRouter();
  router.push({ name: 'Recommendations' });
});
</script>

<style>
/* App.vue样式 */
</style>
