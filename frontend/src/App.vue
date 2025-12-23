<script setup>
import { useRoute } from 'vue-router'
import BottomNav from './components/BottomNav.vue'
import ToastContainer from './components/ToastContainer.vue'

const route = useRoute()

const showNav = () => {
  return route.path !== '/login'
}
</script>

<template>
  <div class="lg:max-w-7xl mx-auto min-h-screen bg-black">
    <router-view />
    <BottomNav v-if="showNav()" />
    <ToastContainer />
  </div>
</template>

<style>
/* Global styles are in style.css */
</style>
