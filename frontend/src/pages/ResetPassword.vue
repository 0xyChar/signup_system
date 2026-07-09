<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="auth-title">Set New Password</h2>
      <p class="auth-subtitle">Enter your new password below</p>

      <form @submit.prevent="handleResetPassword">
        <div class="form-group">
          <label>New password</label>
          <input 
            v-model="form.new_password" 
            type="password" 
            required 
            placeholder="Minimum 8 characters"
          />
        </div>

        <div class="form-group">
          <label>Confirm password</label>
          <input 
            v-model="form.confirm_password" 
            type="password" 
            required 
            placeholder="Re-enter new password"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
          <span class="dismiss-btn" @click="errorMessage = ''">✕</span>
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
          <router-link to="/login" class="success-link">Sign in</router-link>
        </div>

        <button 
          type="submit" 
          class="btn-submit" 
          :disabled="isLoading"
          v-if="!successMessage"
        >
          {{ isLoading ? 'Saving...' : 'Save new password' }}
        </button>

        <p class="back-link">
          <router-link to="/login">← Back to sign in</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const form = reactive({
  new_password: '',
  confirm_password: ''
})

const isLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const token = ref('')

onMounted(() => {
  token.value = route.query.token as string || ''
  
  if (!token.value) {
    errorMessage.value = 'This link is invalid or has expired. Please request a new one.'
  }
})

const handleResetPassword = async () => {
  if (!token.value) {
    errorMessage.value = 'Invalid reset link. Please request a new one.'
    return
  }

  if (form.new_password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters.'
    return
  }

  if (form.new_password !== form.confirm_password) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  isLoading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await api.post('auth/reset-password/', {
      token: token.value,
      new_password: form.new_password,
      confirm_password: form.confirm_password
    })

    successMessage.value = 'Password updated. You can now sign in with your new password.'
    form.new_password = ''
    form.confirm_password = ''
    
    setTimeout(() => {
      router.push('/login')
    }, 3000)
    
  } catch (error: any) {
    const data = error.response?.data
    errorMessage.value = data?.message || 'Something went wrong. Please try again.'
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
}

.auth-box {
  background: white;
  padding: 48px 40px;
  border-radius: 12px;
  max-width: 380px;
  width: 100%;
}

.auth-title {
  font-size: 22px;
  font-weight: 500;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  letter-spacing: -0.3px;
}

.auth-subtitle {
  color: #6b7280;
  font-size: 14px;
  margin: 0 0 32px 0;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 15px;
  background: #fafbfc;
  transition: border 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #000;
  background: white;
}

.form-group input::placeholder {
  color: #9ca3af;
  font-size: 14px;
}

.btn-submit {
  width: 100%;
  padding: 12px;
  background: #1a1a1a;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 6px;
}

.btn-submit:hover {
  background: #333;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  background: #fef2f2;
  color: #991b1b;
  padding: 12px 14px;
  border-radius: 6px;
  font-size: 14px;
  margin: 16px 0 4px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dismiss-btn {
  cursor: pointer;
  color: #7f1d1d;
  font-size: 14px;
  padding: 0 4px;
}

.success-message {
  background: #f0fdf4;
  color: #166534;
  padding: 12px 14px;
  border-radius: 6px;
  font-size: 14px;
  margin: 16px 0 4px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.success-link {
  color: #166534;
  text-decoration: none;
  font-weight: 500;
  margin-left: 8px;
}

.success-link:hover {
  text-decoration: underline;
}

.back-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.back-link a {
  color: #6b7280;
  text-decoration: none;
}

.back-link a:hover {
  color: #1a1a1a;
}
</style>