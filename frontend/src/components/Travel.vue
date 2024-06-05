<template>
  <div class="travel-container">
    <div class="form-group">
      <select id="routeType" v-model="routeType" class="rounded-input">
        <option value="single">单个目的地</option>
        <option value="multi">多个目的地</option>
      </select>
    </div>

    <div class="form-group">
      <input type="text" id="startLocation" v-model="startLocation" placeholder="起点" class="rounded-input"
        @input="validateAndSuggest('startLocation')" @focus="inputFocus">
      <ul v-if="startLocationSuggestions.length" class="suggestions">
        <li v-for="suggestion in startLocationSuggestions" :key="suggestion" @click="selectSuggestion('startLocation', suggestion)">{{ suggestion }}</li>
      </ul>
    </div>

    <div v-if="routeType === 'multi'" class="form-group">
      <input type="text" id="viaPoint1" v-model="viaPoint1" placeholder="途径点1" class="rounded-input"
        @input="validateAndSuggest('viaPoint1')" @focus="inputFocus">
      <ul v-if="viaPoint1Suggestions.length" class="suggestions">
        <li v-for="suggestion in viaPoint1Suggestions" :key="suggestion" @click="selectSuggestion('viaPoint1', suggestion)">{{ suggestion }}</li>
      </ul>
    </div>
    <div v-if="routeType === 'multi'" class="form-group">
      <input type="text" id="viaPoint2" v-model="viaPoint2" placeholder="途径点2" class="rounded-input"
        @input="validateAndSuggest('viaPoint2')" @focus="inputFocus">
      <ul v-if="viaPoint2Suggestions.length" class="suggestions">
        <li v-for="suggestion in viaPoint2Suggestions" :key="suggestion" @click="selectSuggestion('viaPoint2', suggestion)">{{ suggestion }}</li>
      </ul>
    </div>

    <div class="form-group">
      <input type="text" id="endLocation" v-model="endLocation" placeholder="终点" class="rounded-input"
        @input="validateAndSuggest('endLocation')" @focus="inputFocus">
      <ul v-if="endLocationSuggestions.length" class="suggestions">
        <li v-for="suggestion in endLocationSuggestions" :key="suggestion" @click="selectSuggestion('endLocation', suggestion)">{{ suggestion }}</li>
      </ul>
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

  <div>
    <!-- 全局地图图片 -->
    <img v-if="globalMapUrl" :src="globalMapUrl" alt="全局地图" class="global-map">
    <!-- 路径图片 -->
    <img v-if="routeImageUrl" :src="routeImageUrl" alt="路径图片" class="route-map">
    <!-- 调试信息 -->
    <pre v-if="routeImageUrl">路径图片 URL: {{ routeImageUrl }}</pre>
  </div>

  <!-- 路径信息展示 -->
  <div v-if="route.length" class="route-info">
    <h3>路径信息</h3>
    <ul>
      <li v-for="(step, index) in steps" :key="index">
        从 {{ step.from }} 到 {{ step.to }} - 距离: {{ step.distance }} km, 时间: {{ step.time }} 小时
      </li>
    </ul>
  </div>

  <!-- 导航栏组件 -->
  <Navbar />
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件
import globalMapImage from './graph_visualization.png'; // 导入本地全局地图图片

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
const globalMapUrl = ref(globalMapImage); // 直接从本地获取全局地图图片
const routeImageUrl = ref(''); // 路径图片的 URL

const startLocationSuggestions = ref([]);
const endLocationSuggestions = ref([]);
const viaPoint1Suggestions = ref([]);
const viaPoint2Suggestions = ref([]);

const validNodes = [
  // 有效节点列表...
  "others39", "node19", "wc9", "supermarket23", "supermarket22", "supermarket29", "node27", "node58", "others36",
  "supermarket3", "node32", "node56", "supermarket17", "node39", "node31", "restaurant14", "wc7", "others7",
  "supermarket13", "wc12", "others6", "supermarket33", "restaurant15", "restaurant21", "others35", "node7", 
  "others31", "supermarket10", "others12", "others4", "node57", "node52", "others18", "supermarket32", 
  "supermarket14", "restaurant40", "node44", "others33", "node6", "restaurant4", "supermarket15", "node15", 
  "restaurant18", "supermarket7", "others40", "supermarket25", "others14", "restaurant8", "restaurant6", 
  "node55", "restaurant7", "others13", "node29", "supermarket35", "wc2", "supermarket9", "restaurant38", 
  "wc3", "restaurant28", "node16", "node20", "others26", "wc13", "node23", "supermarket36", "node49", 
  "node60", "node53", "supermarket18", "others25", "node59", "node54", "wc10", "others32", "restaurant20", 
  "supermarket40", "others10", "others37", "restaurant9", "restaurant32", "supermarket2", "others5", 
  "restaurant10", "others3", "others2", "node50", "restaurant3", "node47", "restaurant5", "wc16", "node8", 
  "wc11", "node28", "node14", "node24", "wc5", "node35", "restaurant16", "supermarket8", "node38", 
  "supermarket5", "restaurant35", "node41", "node33", "wc6", "supermarket34", "wc15", "node34", 
  "restaurant17", "node10", "node5", "wc20", "others24", "node26", "others21", "supermarket20", 
  "supermarket21", "wc14", "restaurant31", "node9", "node3", "restaurant36", "others8", "supermarket24", 
  "node17", "restaurant37", "restaurant39", "wc18", "node45", "node25", "others17", "others9", 
  "restaurant12", "restaurant11", "node1", "supermarket37", "node30", "supermarket16", "supermarket39", 
  "supermarket27", "supermarket28", "others1", "supermarket6", "restaurant22", "others15", "others22", 
  "others28", "others34", "others20", "node48", "others29", "wc17", "supermarket19", "node46", 
  "node11", "wc8", "node37", "supermarket11", "wc4", "others27", "restaurant27", "node43", "wc1", 
  "node18", "node21", "supermarket4", "restaurant33", "supermarket38", "restaurant30", "supermarket26", 
  "others19", "restaurant13", "node42", "others11", "supermarket12", "others16", "node2", "node12", 
  "restaurant2", "others38", "node4", "node22", "supermarket1", "restaurant29", "restaurant25", 
  "node51", "restaurant19", "node13", "node40", "supermarket30", "restaurant23", "others23", 
  "restaurant26", "restaurant24", "node36", "others30", "supermarket31", "restaurant34", "wc19", "restaurant1"
];

const validateAndSuggest = (field) => {
  let input;
  let suggestionsRef;

  switch (field) {
    case 'startLocation':
      input = startLocation.value;
      suggestionsRef = startLocationSuggestions;
      break;
    case 'viaPoint1':
      input = viaPoint1.value;
      suggestionsRef = viaPoint1Suggestions;
      break;
    case 'viaPoint2':
      input = viaPoint2.value;
      suggestionsRef = viaPoint2Suggestions;
      break;
    case 'endLocation':
      input = endLocation.value;
      suggestionsRef = endLocationSuggestions;
      break;
  }

  if (!validNodes.includes(input)) {
    errorMessage.value = '请输入合法的节点名称';
  } else {
    errorMessage.value = '';
  }
  const query = input.toLowerCase();
  suggestionsRef.value = validNodes.filter(node => node.toLowerCase().includes(query));
};

const selectSuggestion = (field, suggestion) => {
  switch (field) {
    case 'startLocation':
      startLocation.value = suggestion;
      startLocationSuggestions.value = [];
      break;
    case 'viaPoint1':
      viaPoint1.value = suggestion;
      viaPoint1Suggestions.value = [];
      break;
    case 'viaPoint2':
      viaPoint2.value = suggestion;
      viaPoint2Suggestions.value = [];
      break;
    case 'endLocation':
      endLocation.value = suggestion;
      endLocationSuggestions.value = [];
      break;
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

    routeImageUrl.value = routeImageResponse.data.image_url; // 更新路径图片的 URL
    console.log('路径图片 URL:', routeImageUrl.value); // 调试信息
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
  border-radius: 20px;
  /* 两端圆形 */
  border: 1px solid #ccc;
}

.rounded-input:focus {
  outline: none;
  /* 去掉默认的聚焦边框 */
  border-color: #4CAF50;
  /* 聚焦时边框颜色 */
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
  /* 聚焦时的阴影效果 */
}

.search-button {
  width: 100%;
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  /* 两端圆形 */
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #4CAF50;
  /* 绿色主色 */
  color: #fff;
}

.search-button[disabled] {
  background-color: #ccc;
  /* 禁用状态下按钮颜色变成灰色 */
  cursor: not-allowed;
  /* 设置鼠标样式为禁用 */
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.travel-container {
  width: 400px;
  margin: 50px auto;
  /* 50px 的顶部边距，水平居中 */
  padding: 50px;
  /* 添加内边距，使内容与盒子模型边缘有一定距离 */
  /*border: 1px solid #ccc; 添加边框 */
  border-radius: 10px;
  /* 圆角边框 */
}

.suggestions {
  list-style-type: none;
  padding: 0;
  margin: 0;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  max-height: 150px;
  overflow-y: auto;
}

.suggestions li {
  padding: 8px;
  cursor: pointer;
}

.suggestions li:hover {
  background-color: #eee;
}

/* 全局地图样式 */
.global-map {
  width: 100%;
  max-width: 2000px;
  /* 设置最大宽度以防止图片过大 */
  display: block;
  /* 让图片居中显示 */
  margin: auto;
  margin-bottom: 20px;
  /* 添加底部边距 */
}

/* 路径图片样式 */
.route-map {
  width: 100%;
  max-width: 2000px;
  /* 设置最大宽度以防止图片过大 */
  display: block;
  /* 让图片居中显示 */
  margin: auto;
  margin-bottom: 20px;
  /* 添加底部边距 */
}

/* 路径信息样式 */
.route-info {
  margin-top: 20px;
}

.route-info ul {
  list-style-type: none;
  padding: 0;
}

.route-info li {
  margin-bottom: 10px;
}
</style>
