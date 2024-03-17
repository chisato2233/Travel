import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 确保路径正确
import Vuesax from 'vuesax3'

import 'vuesax3/dist/vuesax.css' //Vuesax styles // Vuesax styles
import 'material-icons/iconfont/material-icons.css';
document.body.style.margin = "0";
document.body.style.padding = "0";

const app = createApp(App);

app.use(Vuesax,{}).use(router)
  
app.mount('#app');
