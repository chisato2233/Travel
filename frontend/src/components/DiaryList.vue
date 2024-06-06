<template>
  <div class="diaries">
    <h2>日记推荐</h2>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    <ul v-if="diaries.length" class="diary-list">
      <li v-for="diary in diaries" :key="diary.id" class="diary-item" @mouseover="hover = diary.id"
        @mouseleave="hover = null">
        <h3 @click="toggleContent(diary)">{{ diary.title }}</h3>
        <p v-if="diary.showContent" v-html="diary.displayContent"></p>
        <p v-else v-html="abbreviateContent(diary.content)"></p>

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
        <button v-if="diary.showContent" @click="toggleContent(diary)" class="collapse-btn">折叠</button>
      </li>
    </ul>
    <div v-else>
      <p>没有推荐日记可显示。</p>
    </div>
    <Navbar />
    <Sidebar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';
import Sidebar from './Sidebar.vue';


const diaries = ref([]);
const errorMessage = ref('');
const hover = ref(null);

// 获取推荐日记的方法
const fetchRecommendedDiaries = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/recommendations/diaries', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    diaries.value = response.data.map(diary => ({ ...diary, showContent: false })); // 初始情况下折叠所有日记
  } catch (error) {
    console.error('获取推荐日记失败:', error);
    errorMessage.value = '获取推荐日记失败，请稍后重试。';
  }
};

// 组件挂载时获取推荐日记
onMounted(fetchRecommendedDiaries);

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

const toggleContent = (diary) => {
  diary.showContent = !diary.showContent;
  if (diary.showContent) {
    diary.displayContent = diary.content.replace(/\n/g, '<br>');
  }
};

const abbreviateContent = (content) => {
  const abbreviated = content.length > 100 ? content.substring(0, 100) + '...' : content;
  return abbreviated.replace(/\n/g, '<br>');
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
.diaries {
  padding: 20px;
  background-color: #f8f9fa;
  /* 更轻的背景色 */
  color: #333;
  border-radius: 8px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.diaries h2 {
  color: #007bff;
  /* 更吸引人的标题颜色 */
  text-align: center;
  margin-bottom: 20px;
}

.error {
  color: #dc3545;
  text-align: center;
  margin-bottom: 20px;
}

.diary-list {
  list-style-type: none;
  padding: 0;
}

.diary-item {
  background-color: #ffffff;
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid #dee2e6;
  border-radius: 5px;
  text-align: left;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.diary-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.diary-item h3 {
  color: #343a40;
  margin-bottom: 10px;
  cursor: pointer;
  font-size: 1.25em;
}

.diary-item p {
  margin: 5px 0;
  color: #6c757d;
}

.rating {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 10px;
}

.rating-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5em;
  transition: transform 0.2s;
  margin: 0 5px;
}

.rating-btn:hover {
  transform: scale(1.2);
}

.rating-btn.upvote.active {
  color: #28a745;
}

.rating-btn.downvote.active {
  color: #dc3545;
}

.rating-score {
  margin: 0 10px;
  font-size: 1.5em;
  transition: color 0.3s;
}

.rating-score.positive {
  color: #28a745;
}

.rating-score.negative {
  color: #dc3545;
}

.collapse-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.collapse-btn:hover {
  background-color: #0056b3;
}

.view-all-btn {
  position: fixed;
  bottom: 45px;
  right: 20px;
  background-color: #007bff;
  color: #fff;
  border-radius: 30px;
  padding: 10px 20px;
  font-size: 1em;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.view-all-btn:hover {
  background-color: #0056b3;
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
    transform: scale(1);
  }
}
</style>
