<template>
  <div class="navbar">
    <div class="nav-item" :class="{ active: isCurrentRoute('/recommendations') }"
      @click="navigateTo('/recommendations')">推荐👍️</div>
    <div class="nav-item" :class="{ active: isCurrentRoute('/diarylist') }" @click="navigateTo('/diarylist')">日记📖</div>
    <div class="nav-item" :class="{ active: isCurrentRoute(profileLink) }" @click="navigateTo(profileLink)">我的🧑</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();
const router = useRouter();

const profileLink = computed(() => {
  return localStorage.getItem("token") ? '/profile' : '/login';
});

const navigateTo = (path) => {
  router.push(path);
};

const isCurrentRoute = (path) => {
  return router.currentRoute.value.path === path;
};
</script>

<style scoped>
.navbar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #f0f8ff;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.nav-item {
  text-decoration: none;
  color: #333;
  cursor: pointer;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.nav-item:hover {
  background-color: #87cefa;
  transform: scale(1.1);
}

.nav-item.active {
  background-color: #4682b4;
  color: #fff;
}
</style>
