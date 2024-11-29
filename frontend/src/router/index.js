import { createRouter, createWebHistory } from 'vue-router'
import HomePage1 from '../components/HomePage1.vue'
import ProfilePage from '../components/ProfilePage.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import HomePage from '@/components/HomePage.vue'
import CompleteProfile from '@/components/CompleteProfile.vue'
import StockMarketPage from '@/components/StockMarketPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage1',
      component: HomePage1,
    },
    {
      path:'/profile',
      name:'ProfilePage',
      component: ProfilePage,
    },
    {
      path:'/login',
      name:'Login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup,
    },
    {
      path:'/home-page',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path:'/complete-profile',
      name: 'CompleteProfile',
      component: CompleteProfile
    },
    {
      path:'/stock-market',
      name: 'StockMarketPage',
      component: StockMarketPage,
    },
  ],
})

export default router
