<template>
  <div class="min-h-screen bg-black text-white flex items-center justify-center px-5 lg:px-8">
    <div class="w-full max-w-md lg:max-w-lg">
      <!-- Logo/Header -->
      <div class="text-center mb-10">
        <div class="flex justify-center mb-4">
          <FireIcon class="w-16 h-16 text-primary" />
        </div>
        <h2 class="text-3xl font-bold mb-2">repmate</h2>
        <p class="text-gray-500">Track your workouts, achieve your goals</p>
      </div>

      <!-- Login/Register Form -->
      <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-2xl p-6">
        <form @submit.prevent="isRegistering ? handleRegister() : handleLogin()" class="space-y-4">
          <!-- Name field (only for registration) -->
          <div v-if="isRegistering">
            <label class="text-sm text-gray-400 mb-2 block">Name</label>
            <input
              v-model="name"
              type="text"
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="Your Name"
            />
          </div>

          <div>
            <label class="text-sm text-gray-400 mb-2 block">Email</label>
            <input
              v-model="email"
              type="email"
              required
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label class="text-sm text-gray-400 mb-2 block">Password</label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="••••••••"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm text-center">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-primary to-primary-light text-white font-semibold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {{ loading ? (isRegistering ? 'Creating Account...' : 'Logging in...') : (isRegistering ? 'Create Account' : 'Login') }}
          </button>
        </form>

        <div class="mt-6 text-center text-sm text-gray-500">
          {{ isRegistering ? 'Already have an account?' : "Don't have an account?" }}
          <button @click="toggleMode" class="text-primary hover:underline ml-1">
            {{ isRegistering ? 'Login' : 'Sign up' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FireIcon } from '@heroicons/vue/24/outline'
import api from '../services/api'

const router = useRouter()

const isRegistering = ref(false)
const name = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.login({
      email: email.value,
      password: password.value
    })

    localStorage.setItem('token', response.data.access_token)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.register({
      email: email.value,
      name: name.value || undefined,
      password: password.value
    })

    localStorage.setItem('token', response.data.access_token)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
    console.error('Registration error:', err)
  } finally {
    loading.value = false
  }
}

const toggleMode = () => {
  isRegistering.value = !isRegistering.value
  error.value = ''
}
</script>
