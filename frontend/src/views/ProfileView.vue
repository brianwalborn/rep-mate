<template>
  <div class="min-h-screen bg-black text-white pb-20 lg:pb-8 lg:pl-64 px-5 lg:px-8 pt-6 lg:pt-12">
    <PageHeader title="Profile" />

    <EmptyState v-if="loading" title="Loading profile..." />

    <EmptyState v-else-if="error" title="Failed to load profile">
      <p class="text-red-500 mt-2">{{ error }}</p>
    </EmptyState>

    <div v-else class="space-y-4 lg:max-w-2xl">
      <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-5">
        <div class="text-gray-500 text-sm mb-1">Name</div>
        <div class="text-lg">{{ userName || 'Not set' }}</div>
      </div>

      <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-5">
        <div class="text-gray-500 text-sm mb-1">Email</div>
        <div class="text-lg">{{ userEmail || 'Not set' }}</div>
      </div>

      <button
        @click="logout"
        class="w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-4 rounded-xl transition-colors mt-8"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import EmptyState from '../components/EmptyState.vue'
import PageHeader from '../components/PageHeader.vue'
import api from '../services/api'

const router = useRouter()

const userName = ref('')
const userEmail = ref('')
const loading = ref(true)
const error = ref(null)

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

// Fetch user profile on mount
onMounted(async () => {
  try {
    loading.value = true
    error.value = null
    const response = await api.getProfile()
    userName.value = response.data.name
    userEmail.value = response.data.email
  } catch (err) {
    console.error('Failed to load user profile:', err)
    error.value = 'Failed to load profile. Please try again.'
  } finally {
    loading.value = false
  }
})
</script>
