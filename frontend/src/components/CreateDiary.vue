<template>
  <div class="create-diary">
    <h2>创建日记</h2>
    
    <!-- 创建日记表单 -->
    <form @submit.prevent="createDiary" class="diary-form">
      <input type="text" v-model="newDiary.title" placeholder="标题" class="input-field">
      <textarea v-model="newDiary.content" placeholder="内容" class="textarea-field"></textarea>
      <input type="date" v-model="newDiary.date" placeholder="日期" class="input-field">
      
      <input type="text" v-model="newDiary.location" placeholder="地点" class="input-field"
             @input="validateAndSuggestLocation" @focus="clearError">
      <ul v-if="locationSuggestions.length" class="suggestions">
        <li v-for="suggestion in locationSuggestions" :key="suggestion" @click="selectSuggestion(suggestion)">
          {{ suggestion }}
        </li>
      </ul>
      
      <button type="submit" class="btn-create">创建日记</button>
    </form>
   
    <!-- 提示用户创建失败 -->
    <p v-if="createError" class="error-message">{{ createError }}</p>
    
    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue'; // 导入 Navbar 组件
import { validLocations } from './locations.js'; // 导入合法的地点名称

const router = useRouter();

const newDiary = ref({
  title: '',
  content: '',
  date: '',
  location: ''
});

const createError = ref(''); // 用于存储创建日记失败时的错误信息

const locationSuggestions = ref([]); // 存储地点建议

const validateAndSuggestLocation = () => {
  const inputLocation = newDiary.value.location.toLowerCase();
  locationSuggestions.value = validLocations.filter(location =>
    location.toLowerCase().includes(inputLocation)
  );
  if (!validLocations.includes(newDiary.value.location)) {
    createError.value = '请输入合法的地点名称';
  } else {
    createError.value = '';
  }
};

const selectSuggestion = (suggestion) => {
  newDiary.value.location = suggestion;
  locationSuggestions.value = [];
};

const clearError = () => {
  createError.value = '';
};

const createDiary = async () => {
  try {
    const token = localStorage.getItem('token');

    if (!token) {
      console.error('用户未登录或登录状态已过期');
      router.push('Login/');
      return;
    }

    // 自动生成当前系统时间
    const currentDate = new Date().toISOString().split('T')[0];

    const response = await axios.post('http://localhost:8000/api/diaries/create/', {
      title: newDiary.value.title,
      content: newDiary.value.content,
      date: currentDate, // 使用当前系统时间
      location: newDiary.value.location,
      userId: 'userUniqueId' // 你可能需要从某个地方获取用户ID
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.status === 201) {
      console.log(response.data.message);
      // 清空表单
      newDiary.value = {
        title: '',
        content: '',
        date: '',
        location: ''
      };
      // 创建成功后，导航到 Diary.vue 页面
      router.push('/diary');
    }
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        console.error('缺少或无效的日记信息。');
        createError.value = '缺少或无效的日记信息，请重新填写。';
      } else if (error.response.status === 401) {
        console.error('未经授权的访问。');
        router.push('Login/');
      } else if (error.response.status === 404) {
        console.error('未找到日记。');
        createError.value = '未找到日记，请稍后重试。';
      }
    } else {
      console.error('创建日记失败：', error);
      createError.value = '创建日记失败，请稍后重试。';
    }
  }
};
</script>

<style scoped>
.create-diary {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.diary-form {
  margin-bottom: 20px;
}

.input-field,
.textarea-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

.btn-create {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #28a745; /* 绿色背景 */
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-weight: bold; /* 加粗字体 */
}

.btn-create:hover {
  background-color: #218838; /* 深绿色背景 */
}

.error-message {
  color: #ff0000;
}
</style>
