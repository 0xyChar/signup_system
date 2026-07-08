<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="auth-title">Create Account</h2>
      
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" required />
          <p v-if="errors.email" class="error-message">{{ errors.email[0] }}</p>
        </div>
        
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" type="text" required />
          <p v-if="errors.username" class="error-message">{{ errors.username[0] }}</p>
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" required />
          <p v-if="errors.password" class="error-message">{{ errors.password[0] }}</p>
        </div>
        
        <div class="form-group">
          <label>Confirm Password</label>
          <input v-model="form.confirm_password" type="password" required />
          <p v-if="errors.confirm_password" class="error-message">{{ errors.confirm_password[0] }}</p>
        </div>
        
        <div v-if="formError" class="error-message" style="background:#fee2e2;padding:12px;border-radius:6px;">
          {{ formError }}
        </div>
        
        <button type="submit" class="btn btn-primary" style="width:100%;" :disabled="isLoading">
          {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
        </button>
        
        <p style="text-align:center; margin-top:16px; font-size:14px; color:#6b7280;">
          Already have an account? 
          <router-link to="/login" style="color:#2563eb; text-decoration:none;">Login</router-link>
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

const form = reactive({
  email: '',
  username: '',
  password: '',
  confirm_password: ''
})

const errors = ref<any>({})
const formError = ref('')
const isLoading = ref(false)

const handleSignup = async () => {
  isLoading.value = true
  errors.value = {}
  formError.value = ''
  console.log("Signup button clicked") 
  console.log("Form data:", form)       
  
  isLoading.value = true
  
  try {
    await authStore.signup(form)
    router.push('/login?registered=true')
  } catch (error: any) {
    if (error.errors) {
      errors.value = error.errors
    } else if (error.message) {
      formError.value = error.message
    }
  } finally {
    isLoading.value = false
  }
}
</script>