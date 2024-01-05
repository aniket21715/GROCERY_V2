import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginUser from '../components/LoginUser.vue';
import AdminUserLogout from '../components/AdminUserLogout.vue';
import RegisterUser from '../components/RegisterUser.vue';
import AdminLogin from '../components/AdminLogin.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import StoreManagerRegister from '../components/StoreManagerRegister.vue';
import StoreManagerLogin from '../components/StoreManagerLogin.vue';
import StoreManagerLogout from '../components/StoreManagerLogout.vue';
import StoreManagerDashboard from '../components/StoreManagerDashboard.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/LoginUser', component: LoginUser },
  { path: '/AdminUserLogout', component: AdminUserLogout },
  { path: '/RegisterUser', component: RegisterUser },
  { path: '/AdminLogin', component: AdminLogin },
  { path: '/AdminDashboard', component: AdminDashboard },
  { path: '/StoreManagerRegister' , component: StoreManagerRegister},
  { path: '/StoreManagerLogin' , component: StoreManagerLogin},
  { path: '/StoreManagerLogout' , component: StoreManagerLogout},
  { path: '/StoreManagerDashboard' , component: StoreManagerDashboard},
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

