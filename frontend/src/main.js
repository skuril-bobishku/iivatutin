import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index.js';

import '@/assets/parser.css';
import '@/assets/parse-list.css';
import '@/assets/parse-input.css';
import '@/assets/parse-config.css';
import '@/assets/parse-buttons.css';

const app = createApp(App);
app.use(router);
app.mount('#app')
