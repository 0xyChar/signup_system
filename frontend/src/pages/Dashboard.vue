<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">◆</span>
          <span class="logo-text">PORTAL</span>
        </div>
        <div class="header-right">
          <span class="user-name">{{ user?.username }}</span>
          <button @click="logout" class="logout-btn">Exit</button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-container">
        <!-- Welcome Section -->
        <section class="welcome-section">
          <div class="welcome-badge">ACCESS GRANTED</div>
          <h1 class="welcome-title">
            Welcome, <span class="highlight">{{ user?.username }}</span>
          </h1>
          <p class="welcome-message">
            You are one of {{ stats.total_users || 0 }} registered members.
          </p>
          <div class="welcome-stats">
            <span class="stat-item">New today: {{ stats.new_users_today || 0 }}</span>
            <span class="stat-divider">|</span>
            <span class="stat-item">Joined: {{ user?.date_joined || 'Recently' }}</span>
          </div>
        </section>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card stat-blue">
            <div class="stat-header">
              <span class="stat-label">Total Members</span>
              <span class="stat-icon">◆</span>
            </div>
            <div class="stat-value">{{ stats.total_users || 0 }}</div>
            <div class="stat-footer">Registered accounts</div>
          </div>

          <div class="stat-card stat-green">
            <div class="stat-header">
              <span class="stat-label">New Today</span>
              <span class="stat-icon">◈</span>
            </div>
            <div class="stat-value">{{ stats.new_users_today || 0 }}</div>
            <div class="stat-footer">Joined in 24 hours</div>
          </div>

          <div class="stat-card stat-purple">
            <div class="stat-header">
              <span class="stat-label">System Status</span>
              <span class="stat-icon">◉</span>
            </div>
            <div class="stat-value">Online</div>
            <div class="stat-footer">All systems nominal</div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="activity-section">
          <div class="section-header">
            <h2 class="section-title">Recent Activity</h2>
            <span class="section-badge">Live</span>
          </div>
          
          <div class="activity-list">
            <div v-if="stats.recent_users?.length">
              <div 
                v-for="(user, index) in stats.recent_users" 
                :key="user.email"
                class="activity-item"
                :style="{ animationDelay: `${index * 0.1}s` }"
              >
                <div class="activity-avatar">
                  <span class="avatar-text">{{ user.username.charAt(0).toUpperCase() }}</span>
                </div>
                <div class="activity-info">
                  <span class="activity-name">{{ user.username }}</span>
                  <span class="activity-email">{{ user.email }}</span>
                </div>
                <div class="activity-time">{{ user.date_joined }}</div>
              </div>
            </div>
            <div v-else class="empty-state">
              <span class="empty-icon">◌</span>
              <p>No recent activity</p>
            </div>
          </div>
        </div>
      </div>
    </main>
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

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #1a1a2e;
}

/* ===== HEADER ===== */
.header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(100, 100, 255, 0.08);
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 18px;
  color: #6c5ce7;
}

.logo-text {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 4px;
  color: #1a1a2e;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-name {
  font-size: 13px;
  color: #4a4a6a;
  font-weight: 500;
}

.logout-btn {
  background: transparent;
  border: 1px solid rgba(100, 100, 200, 0.15);
  color: #4a4a6a;
  padding: 6px 18px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 1px;
}

.logout-btn:hover {
  background: rgba(108, 92, 231, 0.06);
  border-color: rgba(108, 92, 231, 0.3);
  color: #6c5ce7;
}

/* ===== MAIN CONTENT ===== */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 40px 60px;
}

/* ===== WELCOME SECTION ===== */
.welcome-section {
  margin-bottom: 40px;
  padding: 40px 48px;
  background: linear-gradient(135deg, #ffffff, #f8f9ff);
  border: 1px solid rgba(108, 92, 231, 0.08);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(108, 92, 231, 0.04);
}

.welcome-badge {
  font-size: 10px;
  color: #6c5ce7;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 12px;
  font-weight: 600;
}

.welcome-title {
  font-size: 32px;
  font-weight: 300;
  color: #1a1a2e;
  letter-spacing: -0.5px;
  margin-bottom: 6px;
}

.welcome-title .highlight {
  color: #6c5ce7;
  font-weight: 500;
}

.welcome-message {
  font-size: 14px;
  color: #6a6a8a;
  font-weight: 400;
  margin-bottom: 14px;
}

.welcome-stats {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #8a8aaa;
}

.stat-item {
  font-weight: 400;
}

.stat-divider {
  color: #d0d0e0;
}

/* ===== STATS GRID ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid rgba(100, 100, 200, 0.06);
  border-radius: 16px;
  padding: 24px 28px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(108, 92, 231, 0.06);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 12px;
  color: #8a8aaa;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.stat-icon {
  font-size: 16px;
  color: #c0c0d0;
  opacity: 0.5;
}

.stat-value {
  font-size: 32px;
  font-weight: 400;
  color: #1a1a2e;
  letter-spacing: -0.5px;
}

.stat-footer {
  font-size: 11px;
  color: #a0a0b8;
  font-weight: 400;
  margin-top: 4px;
}

/* Color variants */
.stat-blue .stat-value { color: #4a6cf7; }
.stat-blue .stat-icon { color: #4a6cf7; opacity: 0.6; }

.stat-green .stat-value { color: #22c55e; }
.stat-green .stat-icon { color: #22c55e; opacity: 0.6; }

.stat-purple .stat-value { color: #6c5ce7; }
.stat-purple .stat-icon { color: #6c5ce7; opacity: 0.6; }

/* ===== ACTIVITY SECTION ===== */
.activity-section {
  background: #ffffff;
  border: 1px solid rgba(100, 100, 200, 0.06);
  border-radius: 16px;
  padding: 24px 28px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #1a1a2e;
  letter-spacing: 0.3px;
}

.section-badge {
  font-size: 10px;
  color: #6c5ce7;
  background: rgba(108, 92, 231, 0.08);
  padding: 2px 14px;
  border-radius: 12px;
  letter-spacing: 1px;
  font-weight: 500;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: transparent;
  border-radius: 8px;
  animation: fadeInUp 0.4s ease forwards;
  opacity: 0;
  transform: translateY(10px);
  transition: background 0.2s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.activity-item:hover {
  background: rgba(108, 92, 231, 0.03);
}

.activity-avatar {
  width: 34px;
  height: 34px;
  background: rgba(108, 92, 231, 0.08);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  font-size: 13px;
  font-weight: 500;
  color: #6c5ce7;
}

.activity-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.activity-name {
  font-size: 14px;
  color: #1a1a2e;
  font-weight: 500;
}

.activity-email {
  font-size: 12px;
  color: #8a8aaa;
  font-weight: 400;
}

.activity-time {
  font-size: 12px;
  color: #a0a0b8;
  font-weight: 400;
  flex-shrink: 0;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #a0a0b8;
}

.empty-icon {
  font-size: 24px;
  display: block;
  margin-bottom: 8px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 13px;
  font-weight: 400;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .header-content {
    padding: 0 20px;
  }
  
  .main-content {
    padding: 20px;
  }
  
  .welcome-section {
    padding: 24px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .welcome-stats {
    flex-direction: column;
    gap: 4px;
  }
  
  .welcome-stats .stat-divider {
    display: none;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    flex-wrap: wrap;
  }
  
  .activity-time {
    width: 100%;
    padding-left: 52px;
  }
}
</style>