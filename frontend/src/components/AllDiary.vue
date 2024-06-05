<template>
  <div class="all-diaries">
    <h2>所有日记</h2>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    <ul v-if="diaries.length" class="diary-list">
      <li v-for="diary in diaries" :key="diary.id" class="diary-item" @mouseover="hover = diary.id"
        @mouseleave="hover = null">
        <h3 @click="toggleContent(diary)">{{ diary.title }}</h3>
        <p v-if="diary.showContent">{{ diary.content }}</p>
        <p v-else>{{ abbreviateContent(diary.content) }}</p>
        <p><strong>作者:</strong> {{ diary.author }}</p>
        <p><strong>发布日期:</strong> {{ diary.date }}</p>
        <div class="rating" :class="{ active: hover === diary.id }">
          <button @click="rateDiary(diary, 1)" class="rating-btn upvote"
            :class="{ active: diary.userRating === 1 }">▲</button>
          <span class="rating-score" :class="{ positive: diary.rating > 0, negative: diary.rating < 0 }">{{ diary.rating
            }}</span>
          <button @click="rateDiary(diary, -1)" class="rating-btn downvote"
            :class="{ active: diary.userRating === -1 }">▼</button>
        </div>
      </li>
    </ul>
    <div v-else>
      <p>没有日记可显示。</p>
    </div>
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';

const diaries = ref([]);
const errorMessage = ref('');
const hover = ref(null);

// 获取所有日记的方法
const fetchAllDiaries = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/diaries/get_all_diaries/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    diaries.value = response.data.map(diary => ({ ...diary, showContent: false })); // 初始情况下折叠所有日记
  } catch (error) {
    console.error('获取所有日记失败:', error);
    errorMessage.value = '获取所有日记失败，请稍后重试。';
  }
};

// 组件挂载时获取所有日记
onMounted(fetchAllDiaries);

// 评分功能
const rateDiary = async (diary, rating) => {
  const newRating = diary.userRating === rating ? 0 : rating; // 如果再次点击相同按钮则取消评分
  try {
    const response = await axios.post('http://localhost:8000/api/diaries/rate/', {
      id: diary.id,
      my_rating: newRating
    }, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    const updatedDiary = response.data;
    const index = diaries.value.findIndex(d => d.id === diary.id);
    if (index !== -1) {
      diaries.value[index].rating = updatedDiary.rating;
      diaries.value[index].userRating = newRating;
      animateRating(diary.id, rating);
    }
  } catch (error) {
    console.error('评分失败:', error);
    errorMessage.value = '评分失败，请稍后重试。';
  }
};

// 动画效果
const animateRating = (diaryId, rating) => {
  const diary = diaries.value.find(d => d.id === diaryId);
  if (!diary) return;
  const ratingBtn = document.querySelector(`.diary-item[key="${diaryId}"] .rating-btn.${rating === 1 ? 'upvote' : 'downvote'}`);
  if (ratingBtn) {
    ratingBtn.classList.add('rated');
    setTimeout(() => {
      ratingBtn.classList.remove('rated');
    }, 1000);
  }
};

// 切换日记内容显示
const toggleContent = (diary) => {
  diary.showContent = !diary.showContent;
};

// 内容摘要
const abbreviateContent = (content) => {
  return content.length > 100 ? content.substring(0, 100) + '...' : content;
};
</script>

<style scoped>
.all-diaries {
  padding: 20px;
  background-color: #f0fff0;
  /* 浅绿色背景 */
  color: #333;
  /* 深色字体 */
  border-radius: 8px;
  /* 圆角 */
  max-width: 800px;
  margin: 0 auto;
  /* 居中 */
}

.all-diaries h2 {
  color: #008000;
  /* 绿色标题 */
  text-align: center;
}

.error {
  color: red;
  text-align: center;
  margin-bottom: 20px;
}

.diary-list {
  list-style-type: none;
  /* 无列表样式 */
  padding: 0;
}

.diary-item {
  background-color: #e6ffe6;
  /* 更浅的绿色背景 */
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  /* 灰色边框 */
  border-radius: 5px;
  text-align: left;
  /* 左对齐 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.diary-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.diary-item h3 {
  color: #008000;
  /* 绿色标题 */
  margin-bottom: 5px;
  cursor: pointer;
}

.diary-item p {
  margin: 5px 0;
}

.rating {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  /* 右对齐 */
  margin-top: 10px;
}

.rating-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 2em;
  transition: transform 0.2s;
}

.rating-btn:hover {
  transform: scale(1.2);
}

.rating-btn.upvote.active {
  color: green;
}

.rating-btn.downvote.active {
  color: red;
}

.rating-score {
  margin: 0 10px;
  font-size: 2em;
  transition: color 0.3s;
}

.rating-score.positive {
  color: green;
}

.rating-score.negative {
  color: red;
}

.rated {
  animation: rated 0.5s forwards;
}

@keyframes rated {
  0% {
    transform: scale(1.2);
  }

  50% {
    transform: scale(1.5);
  }

  100% {
    transform: scale(1.2);
  }
}
</style>
