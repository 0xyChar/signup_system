<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="auth-title">Forgot Password</h2>
      <p style="color: #6b7280; text-align: center; margin-bottom: 20px;">
        Enter your email and we'll send you a reset link
      </p>

      <form @submit.prevent="handleForgotPassword">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required />
        </div>

        <div v-if="successMessage" class="success-message">
           {{ successMessage }}
          <br>
          <router-link to="/login" style="color: #2563eb;">Back to Login</router-link>
        </div>

        <div v-if="errorMessage" class="error-message form-error">
           {{ errorMessage }}
        </div>

        <button type="submit" class="btn btn-primary" :disabled="isLoading" style="width:100%;">
          {{ isLoading ? 'Sending...' : 'Send Reset Link' }}
        </button>

        <p class="auth-link">
          <router-link to="/login">Back to Login</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../services/api'

const email = ref('')
const isLoading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const handleForgotPassword = async () => {
  isLoading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await api.post('auth/forgot-password/', { email: email.value })
    successMessage.value = response.data.message || 'Password reset link sent! Check your email.'
    email.value = ''
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
  background: #f3f4f6;
}

.auth-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  max-width: 400px;
  width: 100%;
}

.auth-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 16px;
}

.form-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  padding: 12px;
  background: #fee2e2;
  border-radius: 6px;
  margin-bottom: 16px;
}

.success-message {
  color: #16a34a;
  padding: 12px;
  background: #dcfce7;
  border-radius: 6px;
  margin-bottom: 16px;
}

.auth-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
}

.auth-link a {
  color: #2563eb;
  text-decoration: none;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>git 