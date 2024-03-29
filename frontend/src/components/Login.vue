<!--  登陆界面中，有登录和注册两个按钮
      登陆成功后，会跳到用户页面（ProfilePage.vue）
      按下注册按钮后，会跳到注册界面（Register.vue） 
      在页面最底下还有一个导航栏                    -->


      <template>
        <div class="login-container">
          <div class="login-form">
            <h2>用户登录</h2>
            <form @submit.prevent="login">
              <div class="form-group">
                <label for="username">用户名：</label>
                <input type="text" id="username" v-model="username" placeholder="请输入用户名">
              </div>
              <div class="form-group">
                <label for="password">密码：</label>
                <input type="password" id="password" v-model="password" placeholder="请输入密码">
              </div>
              <div class="button-group">
                <button type="submit" class="login-button">登录</button>
              </div>
            </form>
          </div>
          <div class="forgot-password">
            <button type="button" class="forgot-password-button" @click="register">注册</button>
          </div>
        </div>
        
        <!-- Insert Navbar component -->
        <Navbar />
      </template>
      
      <script setup>
      import { ref } from 'vue';
      import axios from 'axios';
      import { useRouter } from 'vue-router'; // Import useRouter
      
      // Define useRouter
      const router = useRouter();
      
      // 定义响应式变量
      const username = ref('');
      const password = ref('');
      
      // 登录函数
      const login = async () => {
        try {
          const response = await axios.post('http://localhost:8000/api/users/login', {
            username: username.value,
            password: password.value
          });
          const data = response.data;
          console.log('登录成功:', data);
          // 在这里处理登录成功后的逻辑，例如保存token、跳转页面等
          router.push({ name: 'ProfilePage' }); // Redirect to ProfilePage.vue on successful login
        } catch (error) {
          console.error('登录失败:', error);
          // 在这里处理登录失败后的逻辑，例如提示用户、清除输入等
        }
      };
      
      // 注册函数
      const register = () => {
        router.push({ name: 'Register' }); // Redirect to Register.vue when clicking on Register button
      };
      </script>
      
      <style scoped>
      /* 使用弹性布局使登录界面垂直居中 */
      .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* 将登录界面高度设置为视口高度 */
      }
      
      .login-form {
        width: 300px; /* 设置登录表单的宽度 */
      }
      
      .form-group {
        margin-bottom: 20px; /* 增大表单项之间的垂直间距 */
      }
      
      /* 自适应按钮宽度 */
      .login-button,
      .forgot-password-button {
        width: 100%; /* 设置按钮宽度为父容器宽度 */
      }
      
      /* 鼠标悬停样式 */
      .login-button:hover,
      .forgot-password-button:hover {
        background-color: #0056b3;
      }
      
      /* 响应式调整标题字体大小 */
      h2 {
        font-size: 1.5rem; /* 设置标题字体大小为1.5rem */
      }
      </style>
      
      
      

















