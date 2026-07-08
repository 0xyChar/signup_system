<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // Check if user is already authenticated
  const token = localStorage.getItem('access_token')
  if (token) {
    // You could fetch user profile here
  }
})
</script>