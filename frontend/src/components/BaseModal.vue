<template>
  <div
    v-if="modelValue"
    @click.self="handleClose"
    class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] flex items-end lg:items-center justify-center p-0 lg:p-4"
  >
    <div
      :class="[
        'bg-[#1a1a1a] w-full lg:rounded-2xl rounded-t-[30px] overflow-hidden flex flex-col',
        maxWidth,
        maxHeight
      ]"
    >
      <!-- Header -->
      <div v-if="title || $slots.header" class="flex items-center justify-between p-6 border-b border-[#2a2a2a] flex-shrink-0">
        <slot name="header">
          <h2 class="text-2xl font-bold">{{ title }}</h2>
        </slot>
        <button
          v-if="showClose"
          @click="handleClose"
          class="text-gray-500 hover:text-white transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div :class="['flex-1 overflow-y-auto', contentPadding]">
        <slot />
      </div>

      <!-- Footer -->
      <div v-if="$slots.footer" class="border-t border-[#2a2a2a] flex-shrink-0">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  showClose: {
    type: Boolean,
    default: true
  },
  maxWidth: {
    type: String,
    default: 'lg:max-w-2xl'
  },
  maxHeight: {
    type: String,
    default: 'max-h-[85vh] lg:max-h-[90vh]'
  },
  contentPadding: {
    type: String,
    default: 'p-6'
  }
})

const emit = defineEmits(['update:modelValue'])

const handleClose = () => {
  emit('update:modelValue', false)
}
</script>
