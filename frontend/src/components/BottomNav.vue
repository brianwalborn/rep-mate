<template>
  <nav class="fixed bottom-0 left-0 right-0 lg:left-0 lg:top-0 lg:bottom-0 lg:w-64 lg:right-auto bg-[#1a1a1a] border-t lg:border-t-0 lg:border-r border-[#2a2a2a] flex lg:flex-col justify-around lg:justify-start py-3 lg:py-8 lg:px-4 z-50" style="padding-bottom: max(0.75rem, env(safe-area-inset-bottom))">
    <router-link
      v-for="item in navItems"
      :key="item.name"
      :to="item.path"
      class="flex flex-col lg:flex-row items-center gap-1 lg:gap-4 px-5 lg:px-6 py-2 lg:py-4 rounded-xl transition-all lg:w-full lg:mb-2"
      :class="isActive(item.path) ? 'bg-primary/10 text-primary' : 'text-gray-400'"
    >
      <component :is="item.icon" class="w-6 h-6" />
      <span class="text-[11px] lg:text-base">{{ item.label }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { BookOpenIcon, ChartBarIcon, HomeIcon, UserIcon } from '@heroicons/vue/24/outline'

const route = useRoute()

const navItems = [
  { name: 'home', path: '/', icon: HomeIcon, label: 'Home' },
  { name: 'progress', path: '/progress', icon: ChartBarIcon, label: 'Progress' },
  { name: 'library', path: '/library', icon: BookOpenIcon, label: 'Library' },
  { name: 'profile', path: '/profile', icon: UserIcon, label: 'Profile' }
]

const isActive = (path) => {
  return route.path === path
}
</script>
