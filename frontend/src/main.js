import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index.js';

import '@/assets/parser.css';
import '@/assets/parse-list.css';
import '@/assets/parse-input.css';
import '@/assets/parse-config.css';
import '@/assets/parse-buttons.css';

//createApp(App).use(router).mount('#app');
createApp(App).mount('#app');
