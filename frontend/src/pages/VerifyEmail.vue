<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="auth-title">Email Verification</h2>
      
      <div v-if="loading" class="loading">
        Verifying your email...
      </div>
      
      <div v-if="verified" class="success">
         Email verified successfully!
        <br>
        <router-link to="/login" style="color: #2563eb; text-decoration: none;">
          Click here to login
        </router-link>
      </div>
      
      <div v-if="error" class="error-message">
         {{ error }}
        <br>
        <router-link to="/login" style="color: #2563eb; text-decoration: none;">
          Go to login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const loading = ref(true)
const verified = ref(false)
const error = ref('')

onMounted(async () => {
  const token = route.query.token
  
  if (!token) {
    error.value = 'No verification token found'
    loading.value = false
    return
  }
  
  try {
    const response = await api.post('auth/verify-email/', { token })
    verified.value = true
    loading.value = false
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Verification failed'
    loading.value = false
  }
})
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
}
.auth-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}
.auth-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 24px;
}
.success {
  color: #16a34a;
  padding: 16px;
  background: #dcfce7;
  border-radius: 6px;
}
.error-message {
  color: #dc2626;
  padding: 16px;
  background: #fee2e2;
  border-radius: 6px;
}
.loading {
  color: #2563eb;
  padding: 16px;
}
</style>