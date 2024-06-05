<template>
  <div class="diaries">
    <h2>日记推荐</h2>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    <ul v-if="diaries.length" class="diary-list">
      <li v-for="diary in diaries" :key="diary.id" class="diary-item">
        <h3>{{ diary.title }}</h3>
        <p>{{ diary.content }}</p>
        <p><strong>作者:</strong> {{ diary.author }}</p>
        <p><strong>发布日期:</strong> {{ diary.date }}</p>
        <p><strong>总评分:</strong> {{ diary.rating }}</p>
        <div class="rating">
          <button @click="rateDiary(diary.id, 1)" class="rating-btn upvote" :class="{ active: diary.userRating === 1 }">▲</button>
          <span class="rating-score">{{ diary.rating }}</span>
          <button @click="rateDiary(diary.id, -1)" class="rating-btn downvote" :class="{ active: diary.userRating === -1 }">▼</button>
        </div>
      </li>
    </ul>
    <div v-else>
      <p>没有推荐日记可显示。</p>
    </div>
    <router-link to="/all-diaries" class="view-all-btn">
      查看全部日记
    </router-link>
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';

const diaries = ref([]);
const errorMessage = ref('');

// 获取推荐日记的方法
const fetchRecommendedDiaries = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/recommendations/diaries', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    diaries.value = response.data; // 假设响应数据是日记列表
  } catch (error) {
    console.error('获取推荐日记失败:', error);
    errorMessage.value = '获取推荐日记失败，请稍后重试。';
  }
};

// 组件挂载时获取推荐日记
onMounted(fetchRecommendedDiaries);

// 评分功能
const rateDiary = async (diaryId, rating) => {
  try {
    const response = await axios.post('http://localhost:8000/api/diaries/rate', {
      id: diaryId,
      my_rating: rating
    }, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    const updatedDiary = response.data;
    const index = diaries.value.findIndex(diary => diary.id === diaryId);
    if (index !== -1) {
      diaries.value[index].rating = updatedDiary.rating;
      diaries.value[index].userRating = rating;
    }
  } catch (error) {
    console.error('评分失败:', error);
    errorMessage.value = '评分失败，请稍后重试。';
  }
};
</script>

<style scoped>
.diaries {
  padding: 20px;
  background-color: #f0fff0; /* 浅绿色背景 */
  color: #333; /* 深色字体 */
  border-radius: 8px; /* 圆角 */
  max-width: 800px;
  margin: 0 auto; /* 居中 */
}

.diaries h2 {
  color: #000; /* 深绿色标题 */
  text-align: center;
}

.error {
  color: red;
  text-align: center;
  margin-bottom: 20px;
}

.diary-list {
  list-style-type: none; /* 无列表样式 */
  padding: 0;
}

.diary-item {
  background-color: #e6ffe6; /* 更浅的绿色背景 */
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ccc; /* 灰色边框 */
  border-radius: 5px;
  text-align: left; /* 左对齐 */
}

.diary-item h3 {
  color: #008000; /* 绿色标题 */
  margin-bottom: 5px;
}

.diary-item p {
  margin: 5px 0;
}

.rating {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.rating-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
}

.rating-btn.upvote:hover {
  color: green;
}

.rating-btn.downvote:hover {
  color: red;
}

.rating-score {
  margin: 0 10px;
  font-size: 1.2em;
}

.rating-btn.active {
  font-weight: bold;
}

.view-all-btn {
  position: fixed;
  bottom: 45px;
  right: 20px;
  background-color: #008000; /* 绿色背景色 */
  color: #fff; /* 白色字体 */
  border-radius: 30px; /* 胶囊形状 */
  padding: 10px 20px;
  font-size: 1em;
  text-decoration: none; /* 去除链接默认下划线 */
  transition: background-color 0.3s ease; /* 添加过渡效果 */
}

.view-all-btn:hover {
  background-color: #005200; /* 悬停颜色加深 */
}
</style>
