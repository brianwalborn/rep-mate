<template>
  <div :class="['fixed z-40', position || 'right-5 lg:right-8']" :style="!position ? 'bottom: calc(5.5rem + 0.75rem + env(safe-area-inset-bottom))' : ''">
    <div :class="['flex gap-2', containerClass]">
      <slot name="buttons">
        <button
          @click="$emit('click')"
          :class="[
            'w-14 h-14 lg:w-16 lg:h-16 rounded-full text-white shadow-lg hover:scale-105 active:scale-95 transition-transform flex items-center justify-center',
            buttonClass
          ]"
          :title="title"
        >
          <slot>
            <span class="text-3xl lg:text-4xl">+</span>
          </slot>
        </button>
      </slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  position: {
    type: String,
    default: ''
  },
  buttonClass: {
    type: String,
    default: 'bg-gradient-to-br from-primary to-primary-light'
  },
  containerClass: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  }
})

defineEmits(['click'])
</script>
