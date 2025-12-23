<template>
  <div class="min-h-screen bg-black text-white pb-20 lg:pb-8 lg:pl-64">
    <!-- Top Bar -->
    <div class="px-5 lg:px-8 pt-6 lg:pt-12 pb-2 mb-6">
      <div class="flex items-center gap-3 mb-2">
        <div class="w-2 h-8 bg-primary rounded-full"></div>
        <div>
          <div class="text-[28px] lg:text-4xl font-bold leading-tight">{{ greeting }} {{ userName }}</div>
        </div>
      </div>
      <div class="text-xs lg:text-base text-gray-500 pl-5">{{ currentDate }}</div>
    </div>

    <!-- Progress Rings -->
    <div class="flex justify-around lg:justify-center lg:gap-12 px-5 lg:px-8 mb-5">
      <div class="text-center">
        <div class="relative w-20 h-20 mx-auto mb-2">
          <svg class="transform -rotate-90 w-20 h-20">
            <circle cx="40" cy="40" r="32" stroke="#2a2a2a" stroke-width="8" fill="none" />
            <circle
              cx="40"
              cy="40"
              r="32"
              stroke="#FF6B6B"
              stroke-width="8"
              fill="none"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="exerciseRingOffset"
              class="transition-all duration-500"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center text-xl font-bold">
            {{ exercisesCompleted }}/{{ totalExercises }}
          </div>
        </div>
        <div class="text-xs text-gray-500">Exercises</div>
      </div>

      <div class="text-center">
        <div class="relative w-20 h-20 mx-auto mb-2">
          <svg class="transform -rotate-90 w-20 h-20">
            <circle cx="40" cy="40" r="32" stroke="#2a2a2a" stroke-width="8" fill="none" />
            <circle
              cx="40"
              cy="40"
              r="32"
              stroke="#FF8E53"
              stroke-width="8"
              fill="none"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="setsRingOffset"
              class="transition-all duration-500"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center text-xl font-bold">
            {{ setsCompleted }}
          </div>
        </div>
        <div class="text-xs text-gray-500">Sets Done</div>
      </div>

      <div class="text-center">
        <div class="relative w-20 h-20 mx-auto mb-2">
          <svg class="transform -rotate-90 w-20 h-20">
            <circle cx="40" cy="40" r="32" stroke="#2a2a2a" stroke-width="8" fill="none" />
            <circle
              cx="40"
              cy="40"
              r="32"
              stroke="#FFA07A"
              stroke-width="8"
              fill="none"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="durationRingOffset"
              class="transition-all duration-500"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center text-sm font-bold">
            {{ formattedDuration }}
          </div>
        </div>
        <div class="text-xs text-gray-500">Duration</div>
      </div>
    </div>

    <!-- Workout Summary -->
    <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-[20px] p-5 mx-5 lg:mx-8 mb-5">
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <h4 class="text-2xl text-primary mb-1">{{ totalSets }}</h4>
          <p class="text-xs text-gray-500">Total Sets</p>
        </div>
        <div>
          <h4 class="text-2xl text-primary mb-1">{{ formatVolume(totalVolume) }}</h4>
          <p class="text-xs text-gray-500">Volume (lbs)</p>
        </div>
        <div>
          <h4 class="text-2xl text-primary mb-1">{{ totalReps }}</h4>
          <p class="text-xs text-gray-500">Total Reps</p>
        </div>
      </div>
    </div>

    <!-- Section Header -->
    <div class="flex justify-between items-center px-5 lg:px-8 pb-4">
      <div class="text-[22px] lg:text-2xl font-bold">Current Workout</div>
      <router-link to="/progress" class="text-primary text-sm lg:text-base">History →</router-link>
    </div>

    <!-- Exercise List -->
    <div class="px-5 lg:px-8 space-y-4">
      <div class="lg:grid lg:grid-cols-2 lg:gap-6 lg:space-y-0 space-y-4">
      <div
        v-for="(exercise, index) in workoutExercises"
        :key="exercise.id"
        class="bg-[#1a1a1a] rounded-[20px] p-5 border-2 transition-all"
        :class="isExerciseCompleted(exercise) ? 'border-primary bg-primary/5' : 'border-[#2a2a2a]'"
      >
        <!-- Exercise Header -->
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <h3 class="text-lg font-semibold mb-1">{{ exercise.name }}</h3>
            <div class="text-sm text-gray-500">
              {{ exercise.muscles.join(', ') }} • {{ exercise.equipment }}
            </div>
          </div>
          <button
            @click="removeExercise(exercise.id)"
            class="text-gray-500 hover:text-red-500 transition-colors p-2"
            title="Remove exercise"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

        <!-- Sets List -->
        <div class="space-y-2">
          <div
            v-for="(set, index) in exercise.sets"
            :key="index"
            class="flex items-center gap-3 bg-[#2a2a2a] rounded-xl p-3 border-2 transition-all"
            :class="set.completed ? 'border-primary bg-primary/5' : 'border-transparent'"
          >
            <!-- Checkbox -->
            <button
              @click="toggleSet(exercise.id, index)"
              class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all flex-shrink-0"
              :class="set.completed ? 'bg-primary border-primary' : 'border-gray-600'"
            >
              <svg v-if="set.completed" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </button>

            <!-- Weight Input -->
            <div v-if="exercise.equipment !== 'Bodyweight'" class="flex-1 flex items-center gap-2">
              <input
                v-model="set.weight"
                type="number"
                inputmode="decimal"
                class="w-full bg-[#1a1a1a] rounded-lg px-3 py-2 text-center font-semibold focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="0"
              />
              <span class="text-xs text-gray-500 whitespace-nowrap">lbs</span>
            </div>

            <!-- Bodyweight placeholder -->
            <div v-else class="flex-1 flex items-center justify-center">
              <span class="text-sm text-gray-600">Bodyweight</span>
            </div>

            <!-- Multiplication Symbol -->
            <span v-if="exercise.equipment !== 'Bodyweight'" class="text-gray-600 text-lg flex-shrink-0">×</span>

            <!-- Reps Input -->
            <div class="flex-1 flex items-center gap-2">
              <input
                v-model="set.reps"
                type="number"
                inputmode="numeric"
                class="w-full bg-[#1a1a1a] rounded-lg px-3 py-2 text-center font-semibold focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="0"
              />
              <span class="text-xs text-gray-500 whitespace-nowrap">reps</span>
            </div>

            <!-- Delete Set Button -->
            <button
              @click="removeSet(exercise.id, index)"
              class="text-gray-600 hover:text-red-500 transition-colors p-1 flex-shrink-0"
              title="Remove set"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Add Set Button -->
          <button
            @click="addSet(exercise.id)"
            class="w-full bg-[#2a2a2a] border-2 border-dashed border-[#444] rounded-xl py-3 flex items-center justify-center gap-2 text-sm text-gray-500 hover:border-primary hover:text-primary transition-all"
          >
            <span class="text-lg">+</span>
            <span>Add Set</span>
          </button>
        </div>
      </div>

      </div>

      <!-- Empty State -->
      <div v-if="workoutExercises.length === 0" class="text-center py-16 text-gray-500 lg:col-span-2">
        <div class="text-lg lg:text-xl">No exercises yet</div>
        <div class="text-sm lg:text-base mt-2">Tap the + button to start your workout</div>
      </div>

      <!-- Bottom Padding -->
      <div class="h-4"></div>
    </div>

    <!-- Split Pill FAB -->
    <FloatingActionButton>
      <template #buttons>
        <!-- Finish Workout Button -->
        <button
          v-if="workoutExercises.length > 0"
          @click="showFinishModal = true"
          class="w-14 h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-full text-white shadow-lg hover:scale-105 active:scale-95 transition-transform flex items-center justify-center"
          title="Finish Workout"
        >
          <svg class="w-6 h-6 lg:w-7 lg:h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
        </button>

        <!-- Add Exercise Button -->
        <button
          @click="showAddExercise = true"
          class="w-14 h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-primary to-primary-light rounded-full text-white shadow-lg hover:scale-105 active:scale-95 transition-transform flex items-center justify-center text-3xl lg:text-4xl"
          title="Add Exercise"
        >
          +
        </button>
      </template>
    </FloatingActionButton>

    <!-- Add Exercise Modal -->
    <BaseModal
      v-model="showAddExercise"
      title="Add Exercise"
      max-width="lg:w-[600px]"
      content-padding="p-6 pb-24 lg:pb-6"
    >
      <!-- Search -->
      <div class="mb-4">
        <input
          v-model="exerciseSearch"
          type="text"
          placeholder="Search exercises..."
          class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
        />
      </div>

      <!-- Exercise Library List -->
      <div class="space-y-2 max-h-[50vh] overflow-y-auto">
        <button
          v-for="exercise in filteredLibraryExercises"
          :key="exercise.id"
          @click="addExerciseFromLibrary(exercise)"
          class="w-full bg-[#2a2a2a] hover:bg-[#3a3a3a] border border-[#3a3a3a] rounded-xl p-4 text-left transition-colors"
        >
          <div class="font-semibold mb-1">{{ exercise.name }}</div>
          <div class="text-sm text-gray-500">
            {{ exercise.muscles.join(', ') }} • {{ exercise.equipment }}
          </div>
        </button>
      </div>

      <div v-if="filteredLibraryExercises.length === 0" class="text-center py-8 text-gray-500">
        <div class="text-sm">No exercises found</div>
      </div>
    </BaseModal>

    <!-- Finish Workout Confirmation Modal -->
    <BaseModal
      v-model="showFinishModal"
      title="Finish Workout?"
    >
      <p class="text-gray-400">
        This will save your workout with {{ setsCompleted }} completed sets and {{ formatVolume(totalVolume) }} lbs total volume.
      </p>

      <template #footer>
        <div class="p-6 pb-24 lg:pb-6">
          <div class="flex gap-3">
            <button
              @click="showFinishModal = false"
              class="flex-1 bg-[#2a2a2a] text-white font-semibold py-3 rounded-xl hover:bg-[#3a3a3a] transition-colors"
            >
              Cancel
            </button>
            <button
              @click="finishWorkout"
              :disabled="saving"
              class="flex-1 bg-gradient-to-r from-primary to-primary-light text-white font-semibold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Finish' }}
            </button>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import BaseModal from '../components/BaseModal.vue'
import FloatingActionButton from '../components/FloatingActionButton.vue'
import { useExercises } from '../composables/useExercises'
import { useToast } from '../composables/useToast'
import { useWorkouts } from '../composables/useWorkouts'
import api from '../services/api'
import { formatVolume } from '../utils/formatters'

// Use composables
const { exercises: exerciseLibrary, fetchExercises } = useExercises()
const { createWorkout, loading: workoutLoading } = useWorkouts()
const { success, error } = useToast()

const currentDate = new Date().toLocaleDateString('en-US', {
  weekday: 'long',
  month: 'long',
  day: 'numeric',
  year: 'numeric'
})

const userName = ref('User')
const circumference = 2 * Math.PI * 32

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning,'
  if (hour < 18) return 'Good afternoon,'
  return 'Good evening,'
})

const showAddExercise = ref(false)
const showFinishModal = ref(false)
const exerciseSearch = ref('')

// Timer state
const duration = ref(0) // Duration in minutes
const workoutStartTime = ref(null)
const timerInterval = ref(null)

// Current workout exercises (local state - different from exerciseLibrary)
const workoutExercises = ref([])

const saving = computed(() => workoutLoading.value)

// LocalStorage key for workout persistence
const WORKOUT_STORAGE_KEY = 'rep-mate-active-workout'

// Save workout to localStorage
const saveWorkoutToStorage = () => {
  const workoutState = {
    exercises: workoutExercises.value,
    duration: duration.value,
    startTime: workoutStartTime.value
  }
  localStorage.setItem(WORKOUT_STORAGE_KEY, JSON.stringify(workoutState))
}

// Load workout from localStorage
const loadWorkoutFromStorage = () => {
  const stored = localStorage.getItem(WORKOUT_STORAGE_KEY)
  if (stored) {
    try {
      const workoutState = JSON.parse(stored)
      workoutExercises.value = workoutState.exercises || []
      duration.value = workoutState.duration || 0
      workoutStartTime.value = workoutState.startTime

      // Resume timer if workout was in progress
      if (workoutStartTime.value && workoutExercises.value.length > 0) {
        // Recalculate duration based on stored start time
        duration.value = (Date.now() - workoutStartTime.value) / 60000
        startTimer()
      }
    } catch (err) {
      console.error('Failed to load workout from storage:', err)
      clearWorkoutStorage()
    }
  }
}

// Clear workout from localStorage
const clearWorkoutStorage = () => {
  localStorage.removeItem(WORKOUT_STORAGE_KEY)
}

// Watch for changes and save to localStorage
watch([workoutExercises, duration], () => {
  if (workoutExercises.value.length > 0) {
    saveWorkoutToStorage()
  }
}, { deep: true })

// Timer computed properties
const formattedDuration = computed(() => {
  const mins = Math.floor(duration.value)
  const secs = Math.floor((duration.value % 1) * 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
})

const filteredLibraryExercises = computed(() => {
  if (!exerciseSearch.value) return exerciseLibrary.value

  const query = exerciseSearch.value.toLowerCase()
  return exerciseLibrary.value.filter(ex =>
    ex.name.toLowerCase().includes(query) ||
    ex.muscles.some(m => m.toLowerCase().includes(query)) ||
    ex.equipment.toLowerCase().includes(query)
  )
})

const totalExercises = computed(() => workoutExercises.value.length)
const exercisesCompleted = computed(() => {
  return workoutExercises.value.filter(ex => ex.sets.every(set => set.completed)).length
})

const totalSets = computed(() => {
  return workoutExercises.value.reduce((sum, ex) => sum + ex.sets.length, 0)
})

const setsCompleted = computed(() => {
  return workoutExercises.value.reduce((sum, ex) => {
    return sum + ex.sets.filter(set => set.completed).length
  }, 0)
})

const totalVolume = computed(() => {
  return workoutExercises.value.reduce((sum, ex) => {
    return sum + ex.sets.reduce((setSum, set) => {
      return setSum + (set.completed ? set.weight * set.reps : 0)
    }, 0)
  }, 0)
})

const totalReps = computed(() => {
  return workoutExercises.value.reduce((sum, ex) => {
    return sum + ex.sets.reduce((setSum, set) => {
      return setSum + (set.completed ? set.reps : 0)
    }, 0)
  }, 0)
})

const isExerciseCompleted = (exercise) => {
  return exercise.sets.length > 0 && exercise.sets.every(set => set.completed)
}

// Progress ring computed properties
const exerciseRingOffset = computed(() => {
  if (totalExercises.value === 0) return circumference
  return circumference - (exercisesCompleted.value / totalExercises.value) * circumference
})

const setsRingOffset = computed(() => {
  if (totalSets.value === 0) return circumference
  return circumference - (setsCompleted.value / totalSets.value) * circumference
})

const durationRingOffset = computed(() => {
  const maxDuration = 60 // 60 minutes max for the ring
  const progress = Math.min(duration.value / maxDuration, 1)
  return circumference - progress * circumference
})

const toggleSet = (exerciseId, setIndex) => {
  const exercise = workoutExercises.value.find(ex => ex.id === exerciseId)
  if (exercise) {
    exercise.sets[setIndex].completed = !exercise.sets[setIndex].completed
  }
}

const addSet = (exerciseId) => {
  const exercise = workoutExercises.value.find(ex => ex.id === exerciseId)
  if (exercise && exercise.sets.length > 0) {
    const lastSet = exercise.sets[exercise.sets.length - 1]
    exercise.sets.push({
      weight: lastSet.weight,
      reps: lastSet.reps,
      completed: false
    })
  } else if (exercise) {
    exercise.sets.push({
      weight: 0,
      reps: 0,
      completed: false
    })
  }
}

const removeSet = (exerciseId, setIndex) => {
  const exercise = workoutExercises.value.find(ex => ex.id === exerciseId)
  if (exercise && exercise.sets.length > 1) {
    exercise.sets.splice(setIndex, 1)
  }
}

const removeExercise = (exerciseId) => {
  const index = workoutExercises.value.findIndex(ex => ex.id === exerciseId)
  if (index !== -1) {
    workoutExercises.value.splice(index, 1)

    // Reset timer and clear storage if all exercises are removed
    if (workoutExercises.value.length === 0) {
      resetTimer()
      clearWorkoutStorage()
    }
  }
}

// Timer functions
const startTimer = () => {
  // If timer is already running, don't start another
  if (timerInterval.value) return

  // If no start time, set it now
  if (!workoutStartTime.value) {
    workoutStartTime.value = Date.now()
  }

  // Start interval to update duration
  timerInterval.value = setInterval(() => {
    const elapsed = Date.now() - workoutStartTime.value
    duration.value = elapsed / 60000 // Convert to minutes with decimal
  }, 1000) // Update every second
}

const stopTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const resetTimer = () => {
  stopTimer()
  duration.value = 0
  workoutStartTime.value = null
}

const addExerciseFromLibrary = (libraryExercise) => {
  const newExercise = {
    id: Date.now(), // Temporary ID for local tracking
    exerciseId: libraryExercise.id, // Real exercise ID from database
    name: libraryExercise.name,
    equipment: libraryExercise.equipment,
    muscles: libraryExercise.muscles,
    sets: [
      { weight: 0, reps: 0, completed: false }
    ]
  }

  // Start timer when first exercise is added
  if (workoutExercises.value.length === 0) {
    startTimer()
  }

  workoutExercises.value.push(newExercise)
  showAddExercise.value = false
  exerciseSearch.value = ''
}

const finishWorkout = async () => {
  try {
    // Stop the timer and get final duration
    stopTimer()
    const finalDuration = Math.ceil(duration.value) // Round up to nearest minute

    const workoutData = {
      date: new Date().toISOString(),
      duration: finalDuration,
      exercises: workoutExercises.value.map(ex => ({
        exercise_id: ex.exerciseId, // Use the real exercise ID from database
        name: ex.name,
        sets: ex.sets.map(set => ({
          weight: parseFloat(set.weight) || 0,
          reps: parseInt(set.reps) || 0,
          completed: set.completed
        }))
      }))
    }

    await createWorkout(workoutData)

    // Reset workout and clear storage
    workoutExercises.value = []
    resetTimer()
    clearWorkoutStorage()
    showFinishModal.value = false

    // Show success message
    success('Workout saved successfully')
  } catch (err) {
    console.error('Failed to save workout:', err)
    error('Failed to save workout. Please try again.')
  }
}
// Load exercise library and user data on mount
onMounted(async () => {
  try {
    // Load saved workout from localStorage first
    loadWorkoutFromStorage()

    // Fetch exercise library from backend
    await fetchExercises()

    // Fetch user profile
    try {
      console.log('Fetching user profile...')
      const response = await api.getProfile()
      console.log('Profile response:', response.data)
      userName.value = response.data.name || 'User'
    } catch (error) {
      console.error('Failed to load user profile:', error)
      console.error('Error details:', error.response?.data)
      userName.value = 'User'
    }
  } catch (error) {
    console.error('Failed to initialize home view:', error)
  }
})

// Cleanup timer on component unmount
onBeforeUnmount(() => {
  stopTimer()
})
</script>
