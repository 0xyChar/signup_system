<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="header-right">
          <button @click="logout" class="logout-btn">Exit</button>
        </div>
      </div>
    </header>
    <!-- Main Content -->
    <main class="main-content">
      <div class="content-container">

        <!--Title-->
        <div class="header-center">
          <h2 class="header-tagline">Museum of Articles</h2>
          <p class="header-subtitle">A collection of favourites :)</p>
        </div>
        

        <!-- Welcome Section -->
        <section class="welcome-section">
          <h4 class="welcome-title">
            Hello {{ user?.username }}
          </h4>
        </section>

        

        
       

        

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


</style>

