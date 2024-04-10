import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginUser from '../components/LoginUser.vue';
import RegisterUser from '../components/RegisterUser.vue';
import UserProfile from '../components/UserProfile.vue';
import AdminLogin from '../components/AdminLogin.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import StoreManagerRegister from '../components/StoreManagerRegister.vue';
import StoreManagerLogin from '../components/StoreManagerLogin.vue';
import StoreManagerDashboard from '../components/StoreManagerDashboard.vue';
import AddCategory from '../components/AddCategory.vue';
import AddProduct from '../components/AddProduct.vue';
import EditProduct from '../components/EditProduct.vue';
import CartPage from '../components/CartPage.vue';
import SearchProduct from '../components/SearchProduct.vue';
import PurchaseHistory from '../components/PurchaseHistory.vue';
import SubmitFeedback from '../components/SubmitFeedback.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/LoginUser', component: LoginUser },
  { path: '/RegisterUser', component: RegisterUser },
  { path: '/UserProfile', component: UserProfile },
  { path: '/AdminLogin', component: AdminLogin },
  { path: '/AdminDashboard', component: AdminDashboard },
  { path: '/StoreManagerRegister' , component: StoreManagerRegister},
  { path: '/StoreManagerLogin' , component: StoreManagerLogin},
  { path: '/CartPage' , component: CartPage},
  { path: '/StoreManagerDashboard' , component: StoreManagerDashboard},
  { path:'/AddCategory', component:AddCategory},
  { path:'/AddProduct', component:AddProduct},
  { path:'/SearchProduct', component:SearchProduct},
  {path: '/EditProduct/:productId',component: EditProduct, name: 'EditProduct'},
  { path:'/PurchaseHistory', component:PurchaseHistory},
  { path:'/SubmitFeedback', component:SubmitFeedback},

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

