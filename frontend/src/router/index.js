import { createRouter, createWebHistory } from 'vue-router';
import Parser from '../views/ParserPhoto.vue';
import HomeView from '../views/HomeView.vue';

const routes = [
    {
        path: '/parser',
        name: 'Parser',
        component: Parser,
    },
    {
        path: '/',
        name: 'Home',
        component: HomeView
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;