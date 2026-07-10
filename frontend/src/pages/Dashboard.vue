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
        <!-- Quote of the Day -->
        <section class="quote-section">
          <div class="quote-content">
            <span class="quote-mark">"</span>
            <p class="quote-text">{{ currentQuote.text }}</p>
            <span class="quote-author">— {{ currentQuote.author }}</span>
          </div>
          <div class="quote-refresh">
            <span class="quote-day">Day {{ currentQuote.day }}</span>
            <button @click="refreshQuote" class="quote-btn">↻</button>
          </div>
        </section>

        <!-- Welcome Section -->
        <section class="welcome-section">
          <div class="welcome-badge">✦ WELCOME</div>
          <h1 class="welcome-title">
            Hello, <span class="highlight">{{ user?.username }}</span>
          </h1>
          <p class="welcome-message">
            You are one of {{ stats.total_users || 0 }} amazing people in our community.
          </p>
          <div class="welcome-stats">
  <span class="stat-item">New today: {{ stats.new_users_today || 0 }}</span>
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
          </div>

          <div class="stat-card stat-green">
            <div class="stat-header">
              <span class="stat-label">New Today</span>
              <span class="stat-icon">◈</span>
            </div>
            <div class="stat-value">{{ stats.new_users_today || 0 }}</div>
          </div>

          <div class="stat-card stat-purple">
            <div class="stat-header">
              <span class="stat-label">System Status</span>
              <span class="stat-icon">◉</span>
            </div>
            <div class="stat-value">Alive</div>
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

// Quote of the day
const quotes = [
  { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
  { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
  { text: "It does not matter how slowly you go as long as you do not stop.", author: "Confucius" },
  { text: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
  { text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
  { text: "The only impossible journey is the one you never begin.", author: "Tony Robbins" },
  { text: "Great things never come from comfort zones.", author: "Unknown" },
  { text: "The best time to start was yesterday. The next best time is now.", author: "Unknown" },
  { text: "You are capable of amazing things.", author: "Unknown" },
  { text: "Every day is a new beginning. Take a deep breath and start again.", author: "Unknown" },
  { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
  { text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" },
  { text: "The only person you are destined to become is the person you decide to be.", author: "Ralph Waldo Emerson" },
  { text: "It always seems impossible until it's done.", author: "Nelson Mandela" },
  { text: "What you get by achieving your goals is not as important as what you become.", author: "Zig Ziglar" },
  { text: "The way to get started is to quit talking and begin doing.", author: "Walt Disney" },
  { text: "Don't be pushed around by the problems in your life. Lead them.", author: "Unknown" }
]

const currentQuote = ref({
  text: "The only way to do great work is to love what you do.",
  author: "Steve Jobs",
  day: 1
})

const getQuoteOfTheDay = () => {
  const today = new Date()
  const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24))
  const index = dayOfYear % quotes.length
  currentQuote.value = {
    text: quotes[index].text,
    author: quotes[index].author,
    day: dayOfYear
  }
}

const refreshQuote = () => {
  const randomIndex = Math.floor(Math.random() * quotes.length)
  currentQuote.value = {
    text: quotes[randomIndex].text,
    author: quotes[randomIndex].author,
    day: currentQuote.value.day
  }
}

onMounted(async () => {
  try {
    const response = await api.get('dashboard/stats/')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
  
  getQuoteOfTheDay()
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
  background: linear-gradient(135deg, #f0f4ff 0%, #fae8ff 50%, #fce4ec 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #1a1a2e;
}

/* ===== HEADER ===== */
.header {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(108, 92, 231, 0.08);
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

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 40px 60px;
}

/*Quote Section */
.quote-section {
  background: linear-gradient(135deg, #6c5ce7, #4a6cf7);
  border-radius: 16px;
  padding: 28px 40px;
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 8px 32px rgba(108, 92, 231, 0.2);
  animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 8px 32px rgba(108, 92, 231, 0.2); }
  50% { box-shadow: 0 8px 48px rgba(108, 92, 231, 0.35); }
}

.quote-content {
  flex: 1;
}

.quote-mark {
  font-size: 28px;
  color: rgba(255, 255, 255, 0.3);
  font-family: Georgia, serif;
  display: block;
  line-height: 1;
  margin-bottom: -6px;
}

.quote-text {
  font-size: 18px;
  font-weight: 400;
  color: #ffffff;
  line-height: 1.5;
  font-style: italic;
  margin-bottom: 4px;
}

.quote-author {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 300;
}

.quote-refresh {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
  margin-left: 20px;
}

.quote-day {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 2px;
  font-weight: 300;
}

.quote-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quote-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(180deg);
}

/*Welcome section */
.welcome-section {
  margin-bottom: 32px;
  padding: 32px 40px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(108, 92, 231, 0.04);
}

.welcome-badge {
  font-size: 10px;
  color: #6c5ce7;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 8px;
  font-weight: 600;
}

.welcome-title {
  font-size: 30px;
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
  margin-bottom: 12px;
}

.welcome-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #8a8aaa;
}

.stat-item {
  font-weight: 400;
}

.stat-divider {
  color: #d0d0e0;
}

/*Stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 22px 26px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(108, 92, 231, 0.08);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 11px;
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
  font-size: 30px;
  font-weight: 400;
  color: #1a1a2e;
  letter-spacing: -0.5px;
}

.stat-blue .stat-value { color: #4a6cf7; }
.stat-blue .stat-icon { color: #4a6cf7; opacity: 0.6; }
.stat-green .stat-value { color: #22c55e; }
.stat-green .stat-icon { color: #22c55e; opacity: 0.6; }
.stat-purple .stat-value { color: #6c5ce7; }
.stat-purple .stat-icon { color: #6c5ce7; opacity: 0.6; }

/* ===== ACTIVITY SECTION ===== */
.activity-section {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 22px 26px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.02);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
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
  padding: 10px 14px;
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
  background: rgba(108, 92, 231, 0.04);
}

.activity-avatar {
  width: 32px;
  height: 32px;
  background: rgba(108, 92, 231, 0.08);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  font-size: 12px;
  font-weight: 500;
  color: #6c5ce7;
}

.activity-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.activity-name {
  font-size: 13px;
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
  padding: 30px 0;
  color: #a0a0b8;
}

.empty-icon {
  font-size: 24px;
  display: block;
  margin-bottom: 6px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 13px;
  font-weight: 400;
}

/*Responsive */
@media (max-width: 768px) {
  .header-content {
    padding: 0 20px;
  }
  
  .main-content {
    padding: 20px;
  }
  
  .quote-section {
    padding: 20px 24px;
    flex-direction: column;
    text-align: center;
  }
  
  .quote-refresh {
    margin-left: 0;
    margin-top: 12px;
    flex-direction: row;
    gap: 12px;
  }
  
  .quote-text {
    font-size: 16px;
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
    padding-left: 48px;
  }
}
</style>