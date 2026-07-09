import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Signup from '../pages/Signup.vue'
import ForgotPassword from '../pages/ForgotPassword.vue'
import ResetPassword from '../pages/ResetPassword.vue'
import Dashboard from '../pages/Dashboard.vue'
import VerifyEmail from '../pages/VerifyEmail.vue'

const routes = [
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    { path: '/forgot-password', component: ForgotPassword },
    { path: '/reset-password', component: ResetPassword },
    { path: '/verify-email', component: VerifyEmail }, 
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/', redirect: '/login' }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Auth Guard
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')
    
    if (to.meta.requiresAuth && !token) {
        next('/login')
    } else if ((to.path === '/login' || to.path === '/signup') && token) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router