<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="brand-section">
        <h1 class="brand-name">Portal</h1>
      </div>

      <h2 class="auth-title">Welcome</h2>
      <p class="auth-subtitle">Sign in to continue</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="credentials.email" 
            type="email" 
            required 
            placeholder="you@example.com"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="credentials.password" 
            type="password" 
            required 
            placeholder="Enter your password"
          />
        </div>

        <div class="form-options">
  <router-link to="/forgot-password" class="forgot-link">Forgot password?</router-link>
</div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="btn-submit" 
          :disabled="isLoading"
        >
          {{ isLoading ? 'Signing in...' : 'Sign in' }}
        </button>

        <p class="auth-link">
          Don't have an account? <router-link to="/signup">Create one</router-link>
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
    errorMessage.value = error.message || 'Invalid credentials. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f6f8;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.auth-box {
  background: white;
  padding: 56px 48px 48px 48px;
  border-radius: 16px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
}

.brand-section {
  text-align: center;
  margin-bottom: 36px;
}

.brand-name {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: 1px;
  margin: 0;
}

.auth-title {
  font-size: 24px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  text-align: center;
}

.auth-subtitle {
  color: #8b8f9c;
  font-size: 15px;
  text-align: center;
  margin: 0 0 32px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #2d2f36;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 15px;
  background: #fafbfc;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #1a1a1a;
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.04);
}

.form-group input::placeholder {
  color: #b0b5c2;
  font-size: 14px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0 24px 0;
}

.remember-me {
  font-size: 14px;
  color: #4b4f5a;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.remember-me input {
  margin-right: 8px;
  accent-color: #1a1a1a;
  width: 16px;
  height: 16px;
}

.forgot-link {
  font-size: 14px;
  color: #6b6f7a;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #1a1a1a;
}

.error-message {
  background: #fef2f2;
  color: #991b1b;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin: 12px 0 16px 0;
  text-align: center;
}

.btn-submit {
  width: 100%;
  padding: 13px;
  background: #1a1a1a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-submit:hover {
  background: #2d2f36;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auth-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: #6b6f7a;
}

.auth-link a {
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 500;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.auth-link a:hover {
  border-bottom-color: #1a1a1a;
}
</style>