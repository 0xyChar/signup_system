<template>
  <div class="auth-container">
    <!-- Background Image -->
    <div class="background-image"></div>
    
    <!-- Login -->
    <div class="auth-box-wrapper">
      <div class="auth-box">
        <div class="brand-section">
          <h1 class="brand-name">Login</h1>
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
  justify-content: flex-end;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: relative;
  padding-right: 80px;
}

/* Background Image */
.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/blue daisys.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
}



.auth-box-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  margin-right: 0;
}

.auth-box {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 56px 48px 48px 48px;
  border-radius: 16px;
  width: 100%;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
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
  justify-content: flex-end;
  margin: 4px 0 24px 0;
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
  background: #f5c542;          
  background: linear-gradient(145deg, #f7cd5a, #efb82c);
  color: #2d2419;               
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(212, 160, 23, 0.3),
              0 2px 0 0 #c49a2b;
  letter-spacing: 0.3px;
}

.btn-submit:hover:not(:disabled) {
  background: #fad15a;
  background: linear-gradient(145deg, #fcdb70, #f2c23e);
  box-shadow: 0 6px 18px rgba(212, 160, 23, 0.4),
              0 2px 0 0 #b38b25;
  transform: translateY(-2px);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(2px);
  box-shadow: 0 2px 8px rgba(212, 160, 23, 0.3),
              0 1px 0 0 #a07d20;
}


.btn-submit:disabled {
  background: #f5c542;
  background: linear-gradient(145deg, #f7cd5a, #efb82c);
  color: #2d2419;
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(212, 160, 23, 0.2);
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

/* Responsive */
@media (max-width: 768px) {
  .auth-container {
    justify-content: center;
    padding-right: 20px;
    padding-left: 20px;
  }
  
  .auth-box-wrapper {
    max-width: 100%;
  }
  
  .auth-box {
    padding: 40px 24px;
  }
}
</style>