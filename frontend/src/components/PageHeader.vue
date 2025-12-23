<template>
  <div class="flex items-center gap-3 mb-6 lg:mb-8">
    <div class="w-2 h-8 lg:h-10 bg-primary rounded-full"></div>
    <h1 class="text-[28px] lg:text-4xl font-bold leading-tight">{{ title }}</h1>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>
