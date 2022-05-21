import { createRouter, createWebHistory } from 'vue-router';
import PassBuff from '../components/PassBuff.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: PassBuff,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
