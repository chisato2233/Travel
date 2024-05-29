<template>
  <div>
    <!-- 全局地图图片 -->
    <img v-if="globalMapUrl" :src="globalMapUrl" alt="全局地图" class="global-map">
  </div>

  <div class="travel-container">
    <div class="form-group">
      <select id="routeType" v-model="routeType" class="rounded-input">
        <option value="single">单个目的地</option>
        <option value="multi">多个目的地</option>
      </select>
    </div>

    <div class="form-group">
      <input type="text" id="startLocation" v-model="startLocation" placeholder="起点" class="rounded-input" @focus="inputFocus">
    </div>

    <div v-if="routeType === 'multi'" class="form-group">
      <input type="text" id="viaPoint1" v-model="viaPoint1" placeholder="途径点1" class="rounded-input" @focus="inputFocus">
    </div>
    <div v-if="routeType === 'multi'" class="form-group">
      <input type="text" id="viaPoint2" v-model="viaPoint2" placeholder="途径点2" class="rounded-input" @focus="inputFocus">
    </div>

    <div class="form-group">
      <input type="text" id="endLocation" v-model="endLocation" placeholder="终点" class="rounded-input" @focus="inputFocus">
    </div>

    <div class="form-group">
      <select id="strategy" v-model="strategy" class="rounded-input">
        <option value="shortest">最短路线</option>
        <option value="fastest">最快路线</option>
      </select>
    </div>

    <button class="search-button" @click="searchRoute" :disabled="isSearching">
      <span v-if="isSearching">查询中...</span>
      <span v-else>查询</span>
    </button>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
  
  <!-- 导航栏组件 -->
  <Navbar />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件

const startLocation = ref('');
const endLocation = ref('');
const viaPoint1 = ref('');
const viaPoint2 = ref('');
const strategy = ref('shortest');
const routeType = ref('single');
const errorMessage = ref('');
const isSearching = ref(false); // 控制查询状态
const route = ref([]);
const distance = ref(0);
const time = ref(0);
const steps = ref([]);
const globalMapUrl = ref(''); // 全局地图图片的 URL

const fetchGlobalMap = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/routes/global_map/');
    globalMapUrl.value = response.data.image_url;
  } catch (error) {
    console.error('获取全局地图失败:', error);
  }
};

const searchRoute = async () => {
  try {
    isSearching.value = true; // 开始查询，禁用按钮
    let response;

    if (routeType.value === 'single') {
      response = await axios.post('http://localhost:8000/api/routes/optimal/', {
        startLocation: startLocation.value,
        endLocation: endLocation.value,
        strategy: strategy.value
      });
    } else {
      response = await axios.post('http://localhost:8000/api/routes/multi-destinations/', {
        startLocation: startLocation.value,
        endLocation: endLocation.value,
        viaPoints: [viaPoint1.value, viaPoint2.value],
        strategy: strategy.value
      });
    }

    const data = response.data;
    route.value = data.route;
    distance.value = data.distance;
    time.value = data.time;
    steps.value = data.steps;

    // 获取路径图片
    const routeImageResponse = await axios.post('http://localhost:8000/api/routes/routes_image/', {
      route: data.route
    });

    globalMapUrl.value = routeImageResponse.data.image_url; // 更新全局地图图片的 URL
  } catch (error) {
    console.error('查询失败:', error);
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = '查询失败，请稍后重试。';
    }
  } finally {
    isSearching.value = false; // 查询结束，启用按钮
  }
};

const inputFocus = () => {
  errorMessage.value = ''; // 清除错误消息
};

onMounted(() => {
  fetchGlobalMap(); // 在页面加载时获取全局地图图片
});
</script>

<style scoped>
.travel-container {
  width: 400px;
  margin: auto;
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.rounded-input {
  width: 100%;
  padding: 8px;
  border-radius: 20px; /* 两端圆形 */
  border: 1px solid #ccc;
}

.rounded-input:focus {
  outline: none; /* 去掉默认的聚焦边框 */
  border-color: #4CAF50; /* 聚焦时边框颜色 */
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); /* 聚焦时的阴影效果 */
}

.search-button {
  width: 100%;
  padding: 8px 16px;
  border: none;
  border-radius: 20px; /* 两端圆形 */
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #4CAF50; /* 绿色主色 */
  color: #fff;
}

.search-button[disabled] {
  background-color: #ccc; /* 禁用状态下按钮颜色变成灰色 */
  cursor: not-allowed; /* 设置鼠标样式为禁用 */
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.travel-container {
  width: 400px;
  margin: 50px auto; /* 50px 的顶部边距，水平居中 */
  padding: 50px; /* 添加内边距，使内容与盒子模型边缘有一定距离 */
  /*border: 1px solid #ccc; 添加边框 */
  border-radius: 10px; /* 圆角边框 */
}

/* 全局地图样式 */
.global-map
{
  width: 100%;
  max-width: 600px; /* 设置最大宽度以防止图片过大 */
  display: block; /* 让图片居中显示 */
  margin: auto;
  margin-bottom: 20px; /* 添加底部边距 */
}
</style>
