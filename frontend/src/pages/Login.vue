<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="auth-title">Login</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="credentials.email" type="email" required />
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input v-model="credentials.password" type="password" required />
        </div>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <button type="submit" class="btn btn-primary" style="width:100%;" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
        
        <p style="text-align:center; margin-top:16px; font-size:14px; color:#6b7280;">
          Don't have an account? 
          <router-link to="/signup" style="color:#2563eb; text-decoration:none;">Sign Up</router-link>
        </p>
        <p style="text-align:center; margin-top:8px; font-size:14px;">
          <router-link to="/forgot-password" style="color:#2563eb; text-decoration:none;">Forgot Password?</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const credentials = reactive({
  email: '',
  password: ''
})

const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    await authStore.login(credentials)
    router.push('/dashboard')
  } catch (error: any) {
    errorMessage.value = error.message || 'Login failed'
  } finally {
    isLoading.value = false
  }
}
</script>