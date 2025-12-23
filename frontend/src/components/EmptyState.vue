<template>
  <div class="text-center py-16 lg:py-20 text-gray-500">
    <component
      v-if="icon"
      :is="icon"
      class="w-16 h-16 lg:w-20 lg:h-20 mx-auto mb-4"
    />
    <div class="text-lg lg:text-xl">{{ title }}</div>
    <div v-if="description" class="text-sm lg:text-base mt-2">{{ description }}</div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: Object,
    default: null
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})
</script>
