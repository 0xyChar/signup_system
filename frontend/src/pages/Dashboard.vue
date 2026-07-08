<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="navbar-brand">My App</div>
      <div class="navbar-user">
        <span style="color:#374151;">{{ user?.username }}</span>
        <button @click="logout" class="btn btn-danger">Logout</button>
      </div>
    </nav>
    
    <div class="container" style="padding:24px;">
      <h2 style="font-size:24px; font-weight:bold; color:#1f2937; margin-bottom:24px;">Dashboard</h2>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Total Users</div>
          <div class="stat-value">{{ stats.total_users || 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">New Today</div>
          <div class="stat-value" style="color:#16a34a;">{{ stats.new_users_today || 0 }}</div>
        </div>
      </div>
      
      <div class="card" style="margin-top:24px;">
        <h3 style="font-size:18px; font-weight:600; color:#1f2937; margin-bottom:16px;">Recent Signups</h3>
        <div v-if="stats.recent_users?.length">
          <div v-for="user in stats.recent_users" :key="user.email" style="padding:12px 0; border-bottom:1px solid #e5e7eb;">
            <p style="font-weight:500; color:#1f2937;">{{ user.username }}</p>
            <p style="font-size:14px; color:#6b7280;">{{ user.email }} - {{ user.date_joined }}</p>
          </div>
        </div>
        <p v-else style="color:#6b7280;">No recent signups</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const user = authStore.user

const stats = ref({
  total_users: 0,
  new_users_today: 0,
  recent_users: []
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  try {
    const response = await api.get('dashboard/stats/')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
})
</script>