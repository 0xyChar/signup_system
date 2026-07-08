import { defineStore } from 'pinia'
import api from '../services/api'

interface User {
    id: number
    email: string
    username: string
    is_email_verified: boolean
    date_joined: string
}

interface AuthState {
    user: User | null
    token: string | null
    isLoading: boolean
    error: any
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        token: localStorage.getItem('access_token') || null,
        isLoading: false,
        error: null
    }),
    
    getters: {
        isAuthenticated: (state): boolean => !!state.token,
        getError: (state): any => state.error
    },
    
    actions: {
        async signup(userData: any) {
            this.isLoading = true
            this.error = null
            
            try {
                const response = await api.post('auth/signup/', userData)
                this.isLoading = false
                return response.data
            } catch (error: any) {
                this.isLoading = false
                this.error = error.response?.data || { message: 'Signup failed' }
                throw this.error
            }
        },
        
        async login(credentials: { email: string; password: string }) {
            this.isLoading = true
            this.error = null
            
            try {
                const response = await api.post('auth/login/', credentials)
                this.token = response.data.access
                this.user = response.data.user
                localStorage.setItem('access_token', response.data.access)
                this.isLoading = false
                return response.data
            } catch (error: any) {
                this.isLoading = false
                this.error = error.response?.data || { message: 'Login failed' }
                throw this.error
            }
        },
        
        async logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('access_token')
        }
    }
})