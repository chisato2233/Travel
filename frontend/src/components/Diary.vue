<!--  如果未登录，无法进入日记界面-->
<!--  已登录，可以创建日记，获取日记，更新日记，删除日记
      在页面最底下还有一个导航栏       -->

      <template>
        <div class="diary">
          <h2>创建日记</h2>
          <!-- 创建日记表单 -->
          <form @submit.prevent="createDiary" class="diary-form">
            <input type="text" v-model="newDiary.title" placeholder="标题" class="input-field">
            <textarea v-model="newDiary.content" placeholder="内容" class="textarea-field"></textarea>
            <input type="date" v-model="newDiary.date" placeholder="日期" class="input-field">
            <input type="text" v-model="newDiary.location" placeholder="地点" class="input-field">
            <button type="submit" class="btn-create">创建日记</button>
          </form>
      
          <h2>我的日记</h2>
          <!-- 展示用户日记列表 -->
          <div v-if="diaries.length > 0">
            <ul class="diary-list">
              <li v-for="diary in diaries" :key="diary.id" class="diary-item">
                <h3>{{ diary.title }}</h3>
                <p>{{ diary.content }}</p>
                <p>日期: {{ diary.date }}</p>
                <p>地点: {{ diary.location }}</p>
                <!-- 更新日记按钮 -->
                <button @click="updateDiary(diary.id)" class="btn-update">更新日记</button>
                <!-- 删除日记按钮 -->
                <button @click="deleteDiary(diary.id)" class="btn-delete">删除日记</button>
              </li>
            </ul>
          </div>
          <p v-else class="no-diaries">暂无日记。</p>
      
          <!-- 导航栏组件 -->
          <Navbar />
        </div>
      </template>
      
      <script setup>
      import { ref, onMounted } from 'vue';
      import axios from 'axios';
      import Navbar from './Navbar.vue'; // 导入底部导航栏组件
      
      const diaries = ref([]); // 存储用户日记列表
      const newDiary = ref({
        title: '',
        content: '',
        date: '',
        location: ''
      }); // 用于存储新日记的数据
      
      // 在页面加载时获取用户日记列表
      onMounted(async () => {
        await fetchDiaries();
      });
      
      // 创建日记的方法
      const createDiary = async () => {
        try {
          const response = await axios.post('http://localhost:8000/api/diaries/', newDiary.value);
          console.log(response.data.message); // 打印成功创建日记的消息
          await fetchDiaries(); // 创建日记后刷新日记列表
          // 清空新日记数据
          newDiary.value = {
            title: '',
            content: '',
            date: '',
            location: ''
          };
        } catch (error) {
          console.error('创建日记失败:', error);
        }
      };
      
      // 更新日记的方法
      const updateDiary = async (diaryId) => {
        try {
          const response = await axios.put(`http://localhost:8000/api/diaries/${diaryId}`, {
            title: 'Updated Title',
            content: 'Updated content...',
            date: '2023-07-22',
            location: 'LocationB'
          });
          console.log(response.data.message); // 打印成功更新日记的消息
          await fetchDiaries(); // 更新日记后刷新日记列表
        } catch (error) {
          console.error('更新日记失败:', error);
        }
      };
      
      // 删除日记的方法
      const deleteDiary = async (diaryId) => {
        try {
          const response = await axios.delete(`http://localhost:8000/api/diaries/${diaryId}/delete`);
          console.log(response.data.message); // 打印成功删除日记的消息
          await fetchDiaries(); // 删除日记后刷新日记列表
        } catch (error) {
          console.error('删除日记失败:', error);
        }
      };
      
      // 获取用户日记列表的方法
      const fetchDiaries = async () => {
        try {
          const response = await axios.get('http://localhost:8000/api/diaries/my-diaries');
          diaries.value = response.data; // 将获取到的日记列表存储到 diaries 变量中
        } catch (error) {
          console.error('获取用户日记失败:', error);
        }
      };
      </script>
      
      <style scoped>
      .diary {
        max-width: 800px;
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
      
      .btn-create,
      .btn-update,
      .btn-delete {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        margin-right: 10px;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
      }
      
      .btn-create:hover,
      .btn-update:hover,
      .btn-delete:hover {
        background-color: #0056b3;
      }
      
      .diary-list {
        list-style: none;
        padding: 0;
      }
      
      .diary-item {
        margin-bottom: 20px;
      }
      
      .no-diaries {
        color: #888;
      }
      </style>
      
          
          