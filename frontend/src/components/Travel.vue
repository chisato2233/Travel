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
      <label for="viaPointCount">途径点数量</label>
      <input type="number" id="viaPointCount" v-model="viaPointCount" min="2" max="200" class="rounded-input">
    </div>

    <div v-if="routeType === 'multi'" v-for="(viaPoint, index) in viaPoints" :key="index" class="form-group">
      <input type="text" :id="'viaPoint' + index" v-model="viaPoints[index]" :placeholder="'途径点' + (index + 1)" class="rounded-input"
        @input="validateAndSuggest('viaPoints', index)" @focus="inputFocus">
      <ul v-if="viaPointSuggestions[index] && viaPointSuggestions[index].length" class="suggestions">
        <li v-for="suggestion in viaPointSuggestions[index]" :key="suggestion" @click="selectSuggestion('viaPoints', suggestion, index)">{{ suggestion }}</li>
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
    <!-- <pre v-if="routeImageUrl">路径图片 URL: {{ routeImageUrl }}</pre> -->
  </div>

  <!-- 路径信息展示 -->
  <div v-if="route.length" class="route-info">
    <h3>路径信息</h3>
    <ul>
      <li v-for="(step, index) in steps" :key="index">
        <div class="step-info">
          <span class="step-index">{{ index + 1 }}</span>
          <span class="step-text">从 <strong>{{ step.from }}</strong> 到 <strong>{{ step.to }}</strong> - 距离: {{ step.distance }} km, 时间: {{ step.time }} 小时</span>
        </div>
      </li>
    </ul>
  </div>

  <!-- 导航栏组件 -->
  <Navbar />
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件
import globalMapImage from './graph_visualization.png'; // 导入本地全局地图图片

const startLocation = ref('');
const endLocation = ref('');
const viaPointCount = ref(2); // 默认途径点数量为2
const viaPoints = ref(Array(viaPointCount.value).fill(''));
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
const viaPointSuggestions = ref(Array(viaPointCount.value).fill([]));

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
  "node60", "node53", "supermarket18", "others25", "node59", "node54", "wc10", "others32", "restaurant20", "supermarket40", "others10", "others37", "restaurant9", "restaurant32", "supermarket2", "others5", 
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
  "others19", "restaurant13", "node42", "others23", "supermarket1", "supermarket12", "restaurant2", 
  "node13", "restaurant25", "node4", "others11", "restaurant29", "node2", "restaurant23",   "node12", "supermarket30", "node40", "supermarket31", "supermarket32", "restaurant24", "restaurant34", 
  "node36", "others30", "restaurant1"
];

const validateAndSuggest = (field, index = null) => {
  let input;
  let suggestionsRef;

  if (field === 'startLocation') {
    input = startLocation.value;
    suggestionsRef = startLocationSuggestions;
  } else if (field === 'endLocation') {
    input = endLocation.value;
    suggestionsRef = endLocationSuggestions;
  } else if (field === 'viaPoints') {
    input = viaPoints.value[index];
    suggestionsRef = viaPointSuggestions;
  }

  if (field !== 'viaPoints' && !validNodes.includes(input)) {
    errorMessage.value = '请输入合法的节点名称';
  } else if (field === 'viaPoints' && !validNodes.includes(input)) {
    errorMessage.value = '请输入合法的节点名称';
  } else {
    errorMessage.value = '';
  }

  const query = input.toLowerCase();
  suggestionsRef[index !== null ? index : 'value'] = validNodes.filter(node => node.toLowerCase().includes(query));
};

const selectSuggestion = (field, suggestion, index = null) => {
  if (field === 'startLocation') {
    startLocation.value = suggestion;
    startLocationSuggestions.value = [];
  } else if (field === 'endLocation') {
    endLocation.value = suggestion;
    endLocationSuggestions.value = [];
  } else if (field === 'viaPoints') {
    viaPoints.value[index] = suggestion;
    viaPointSuggestions[index] = [];
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
        viaPoints: viaPoints.value,
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

// 监听途径点数量变化，动态调整途径点输入框
watch(viaPointCount, (newCount) => {
  viaPoints.value = Array(newCount).fill('');
  viaPointSuggestions.value = Array(newCount).fill([]);
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
  border-radius: 20px;
  border: 1px solid #ccc;
}

.rounded-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
}

.search-button {
  width: 100%;
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #4CAF50;
  color: #fff;
}

.search-button[disabled] {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.travel-container {
  width: 400px;
  margin: 50px auto;
  padding: 50px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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

.global-map {
  width: 100%;
  max-width: 2000px;
  display: block;
  margin: auto;
  margin-bottom: 20px;
}

.route-map {
  width: 100%;
  max-width: 2000px;
  display: block;
  margin: auto;
  margin-bottom: 20px;
}

.route-info {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.route-info h3 {
  text-align: center;
  color: #4CAF50;
  margin-bottom: 20px;
}

.route-info ul {
  list-style-type: none;
  padding: 0;
}

.route-info li {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.step-info {
  display: flex;
  align-items: center;
  width: 100%;
}

.step-index {
  display: inline-block;
  width: 30px;
  height: 30px;
  background-color: #4CAF50;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 30px;
  margin-right: 10px;
}

.step-text {
  flex-grow: 1;
  color: #333;
}
</style>

