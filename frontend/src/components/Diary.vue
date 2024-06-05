<template>
  <div class="diary">
    <h2>我的日记</h2>

    <!-- 添加日记按钮 -->
    <router-link :to="{ name: 'CreateDiary' }" class="btn-add">+</router-link>

    <!-- 展示用户日记列表 -->
    <div v-if="diaries.length > 0">
      <ul class="diary-list">
        <li v-for="diary in sortedDiaries" :key="diary.id" class="diary-item" @mouseover="hover = diary.id"
          @mouseleave="hover = null">
          <h3>{{ diary.title }}</h3>
          <p>{{ diary.content }}</p>
          <p>日期: {{ diary.date }}</p>
          <p>地点: {{ diary.location }}</p>
          <p>评分: {{ diary.userRating }}</p>
          <!-- 评分按钮 -->
          <div class="rating" :class="{ active: hover === diary.id }">
            <button @click="rateDiary(diary, 1)" class="rating-btn upvote"
              :class="{ active: diary.userRating === 1 }">▲</button>
            <span class="rating-score" :class="{ positive: diary.rating > 0, negative: diary.rating < 0 }">{{
              diary.rating }}</span>
            <button @click="rateDiary(diary, -1)" class="rating-btn downvote"
              :class="{ active: diary.userRating === -1 }">▼</button>
          </div>
          <!-- 更新日记按钮 -->
          <button @click="updateDiary(diary)" class="btn-update">
            <i class="fas fa-pencil-alt"></i> 🖊️
          </button>

          <!-- 删除日记按钮 -->
          <button @click="deleteDiary(diary.id)" class="btn-delete">🗑️</button>
        </li>
      </ul>
    </div>
    <p v-else class="no-diaries">暂无日记。</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const diaries = ref([]); // 存储用户日记列表
const router = useRouter();
const hover = ref(null);

// 获取用户日记列表的方法
const fetchDiaries = async () => {
  const token = localStorage.getItem('token'); // 从 localStorage 获取 token
  if (!token) {
    console.error('Token not found');
    return;
  }
  console.log('Using token:', token);
  try {
    const response = await axios.get('http://localhost:8000/api/diaries/my-diaries/', {
      headers: {
        'Authorization': `Bearer ${token}` // 在请求头中添加 Authorization
      }
    });
    diaries.value = response.data; // 将获取到的日记列表存储到 diaries 变量中
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // 跳转到登录页面
      console.error('未经授权的访问。');
      router.push('Login/');
    } else {
      console.error('获取用户日记失败：', error);
    }
  };
}

// 在组件加载时调用 fetchDiaries 函数，获取用户日记列表
onMounted(fetchDiaries);

// 计算属性：按日期排序的日记列表
const sortedDiaries = computed(() => {
  return diaries.value.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
});

// 更新日记
const updateDiary = (diary) => {
  // 导航到UpdateDiary路由时，传递diaryData和id参数
  router.push({
    name: 'UpdateDiary',
    params: {
      diaryData: diary,
      id: diary.id // 传递id参数
    }
  });
}

// 删除日记
const deleteDiary = async (diaryId) => {
  const token = localStorage.getItem('token');
  if (!token) {
    console.error('Token not found');
    return;
  }
  try {
    const response = await axios.delete(`http://localhost:8000/api/diaries/delete/${diaryId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log(response.data.message); // 输出删除成功的消息
    // 删除成功后，重新获取日记列表以更新界面
    await fetchDiaries();
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.error('日记未找到。');
    } else {
      console.error('删除日记失败：', error);
    }
  }
}

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
    diary.rating = updatedDiary.rating;
    diary.userRating = newRating;
    animateRating(diary.id, rating);
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
</script>

<style scoped>
.diary {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.diary-list {
  list-style: none;
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

.no-diaries {
  color: #888;
}

.btn-add {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #28a745;
  color: #fff;
  font-size: 24px;
  border: none;
  cursor: pointer;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.btn-update {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #25dc44;
  /* 蓝色背景 */
  color: #fff;
  /* 白色字体 */
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
}

.btn-delete {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #dc3545;
  /* 红色背景 */
  color: #fff;
  /* 白色字体 */
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
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
