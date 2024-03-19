import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
export default defineConfig({
  plugins: [vue()],
  base: '/', // 确保这是正确的，对于根部署，通常是 '/'
  resolve: {  
  } ,
  server: {
    strictPort: true,  // 如果端口已被占用，则直接退出
    fs: {
      // 限制服务的文件范围，以防出现安全问题
      strict: true,
    }// 确保开发服务器对所有路由都返回 index.html
  }
});
