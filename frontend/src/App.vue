<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" class="router-view" />
      </transition>
    </router-view>
  </div>
</template>


<script>
export default {
  name: 'App'
};
</script>

<style>
@keyframes gradientBackground {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

body {
  margin: 0;
  padding: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background: linear-gradient(45deg, #ffcccc, #ccffff);
  background-size: 200% 200%;
  animation: gradientBackground 10s ease infinite;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
