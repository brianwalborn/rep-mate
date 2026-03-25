<template>
  <div class="min-h-screen bg-black text-white pb-20 lg:pb-8 lg:pl-64 px-5 lg:px-8 pt-6 lg:pt-12">
    <PageHeader title="Progress" />

    <!-- Loading State -->
    <EmptyState
      v-if="loading && workouts.length === 0"
      title="Loading workouts..."
    />

    <!-- Empty State -->
    <EmptyState
      v-else-if="!loading && workouts.length === 0"
      :icon="ChartBarIcon"
      title="No workouts yet"
      description="Complete your first workout to see your progress here"
    />

    <!-- Workout List -->
    <div v-else class="space-y-4 lg:max-w-4xl pb-8">
      <div
        v-for="workout in sortedWorkouts"
        :key="workout.id"
        @click="viewWorkout(workout)"
        class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-5 hover:border-primary/50 transition-colors cursor-pointer"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold mb-1">{{ formatDate(workout.date) }}</h3>
            <div class="text-sm text-gray-500">{{ formatTime(workout.date) }}</div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-bold text-primary">{{ workout.duration }}m</div>
            <div class="text-xs text-gray-500">Duration</div>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4 text-center mb-4">
          <div>
            <div class="text-xl font-semibold text-primary">{{ workout.exercises.length }}</div>
            <div class="text-xs text-gray-500">Exercises</div>
          </div>
          <div>
            <div class="text-xl font-semibold text-primary">{{ getTotalSets(workout) }}</div>
            <div class="text-xs text-gray-500">Sets</div>
          </div>
          <div>
            <div class="text-xl font-semibold text-primary">{{ formatVolume(getTotalVolumeInUserUnit(workout), userWeightUnit) }}</div>
            <div class="text-xs text-gray-500">Volume ({{ userWeightUnit }})</div>
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <div
            v-for="muscle in getUniqueMuscles(workout)"
            :key="muscle"
            class="text-xs bg-primary/10 border border-primary/30 px-3 py-1 rounded-full text-primary"
          >
            {{ muscle }}
          </div>
        </div>
      </div>
    </div>

    <!-- Workout Detail Modal -->
    <BaseModal
      v-model="selectedWorkout"
      :show-close="true"
      content-padding="p-0"
    >
      <template #header>
        <div>
          <h2 class="text-2xl font-bold">{{ formatDate(selectedWorkout.date) }}</h2>
          <div class="text-sm text-gray-500 mt-1">{{ formatTime(selectedWorkout.date) }}</div>
        </div>
      </template>

      <!-- Modal Stats -->
      <div class="grid grid-cols-4 gap-4 p-6 border-b border-[#2a2a2a]">
        <div class="text-center">
          <div class="text-2xl font-bold text-primary">{{ selectedWorkout.duration }}m</div>
          <div class="text-xs text-gray-500 mt-1">Duration</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-primary">{{ selectedWorkout.exercises.length }}</div>
          <div class="text-xs text-gray-500 mt-1">Exercises</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-primary">{{ getTotalSets(selectedWorkout) }}</div>
          <div class="text-xs text-gray-500 mt-1">Sets</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-primary">{{ formatVolume(getTotalVolumeInUserUnit(selectedWorkout), userWeightUnit) }}</div>
          <div class="text-xs text-gray-500 mt-1">Volume ({{ userWeightUnit }})</div>
        </div>
      </div>

      <div class="p-6 border-b border-[#2a2a2a] space-y-3">
        <div class="flex items-center justify-between">
          <div class="text-sm font-semibold text-white">Workout Time</div>
          <button
            v-if="!isEditingTimes"
            @click.stop="startEditingTimes"
            class="text-sm text-primary hover:text-primary-light transition-colors"
          >
            Edit
          </button>
        </div>

        <div v-if="!isEditingTimes" class="text-sm text-gray-400">
          {{ formatDate(getWorkoutStartTime(selectedWorkout)) }} · {{ formatTime(getWorkoutStartTime(selectedWorkout)) }} - {{ formatTime(getWorkoutEndTime(selectedWorkout)) }}
        </div>

        <div v-else class="space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block text-xs text-gray-500 mb-2">Date</label>
              <input
                v-model="editDate"
                type="date"
                class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-3 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-2">Start Time</label>
              <input
                v-model="editStartTime"
                type="time"
                class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-3 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-2">End Time</label>
              <input
                v-model="editEndTime"
                type="time"
                class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-3 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>
          </div>

          <div class="flex gap-3">
            <button
              @click.stop="cancelEditingTimes"
              class="flex-1 bg-[#2a2a2a] text-white font-semibold py-2 rounded-xl hover:bg-[#3a3a3a] transition-colors"
            >
              Cancel
            </button>
            <button
              @click.stop="saveWorkoutTimes"
              :disabled="savingTimes"
              class="flex-1 bg-primary text-white font-semibold py-2 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ savingTimes ? 'Saving...' : 'Save Time' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal Exercise List -->
      <div class="p-6 pb-20 lg:pb-8 space-y-4">
        <div
          v-for="exercise in selectedWorkout.exercises"
          :key="exercise.id"
          class="bg-[#0a0a0a] border border-[#2a2a2a] rounded-xl p-4"
        >
          <div class="mb-3">
            <h3 class="font-semibold text-lg">{{ exercise.exercise_name }}</h3>
            <div v-if="exercise.equipment" class="text-sm text-gray-500 mt-1">{{ exercise.equipment }}</div>
          </div>

          <!-- Exercise Notes -->
          <div v-if="exercise.notes" class="mb-3 p-3 bg-primary/5 border border-primary/20 rounded-lg">
            <div class="flex items-start gap-2">
              <svg class="w-4 h-4 text-primary flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <div class="text-sm text-gray-300">{{ exercise.notes }}</div>
            </div>
          </div>

          <div class="space-y-2">
            <div
              v-for="(set, index) in exercise.sets"
              :key="set.id"
              class="flex items-center justify-between text-sm"
            >
              <div class="text-gray-500">Set {{ index + 1 }}</div>
              <div class="flex items-center gap-4">
                <div v-if="set.weight > 0" class="text-gray-300">
                  <span class="font-semibold">{{ formatWeight(getDisplayWeight(set).weight, getDisplayWeight(set).unit) }}</span> {{ getDisplayWeight(set).unit }}
                </div>
                <div class="text-gray-300">
                  <span class="font-semibold">{{ set.reps }}</span> reps
                </div>
                <div
                  class="w-5 h-5 rounded border-2 flex items-center justify-center"
                  :class="set.completed ? 'bg-primary border-primary' : 'border-gray-600'"
                >
                  <svg v-if="set.completed" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="p-6 pb-24 lg:pb-6">
          <button
            v-if="!showDeleteConfirm"
            @click.stop="showDeleteConfirm = true"
            class="w-full bg-red-600/10 border border-red-600/30 text-red-500 font-semibold py-3 rounded-xl hover:bg-red-600/20 transition-colors"
          >
            Delete Workout
          </button>
          <div v-else class="space-y-3">
            <p class="text-sm text-gray-400 text-center">Are you sure you want to delete this workout?</p>
            <div class="flex gap-3">
              <button
                @click.stop="showDeleteConfirm = false"
                class="flex-1 bg-[#2a2a2a] text-white font-semibold py-3 rounded-xl hover:bg-[#3a3a3a] transition-colors"
              >
                Cancel
              </button>
              <button
                @click.stop="handleDeleteWorkout"
                :disabled="loading"
                class="flex-1 bg-red-600 text-white font-semibold py-3 rounded-xl hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {{ loading ? 'Deleting...' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'
import BaseModal from '../components/BaseModal.vue'
import EmptyState from '../components/EmptyState.vue'
import PageHeader from '../components/PageHeader.vue'
import { useToast } from '../composables/useToast'
import { useWorkouts } from '../composables/useWorkouts'
import api from '../services/api'
import { convertWeight, formatDate, formatTime, formatVolume, formatWeight, getTotalSets, getTotalVolume, getUniqueMuscles } from '../utils/formatters'

const { workouts, loading, fetchWorkouts, updateWorkout, deleteWorkout } = useWorkouts()
const { success, error } = useToast()
const selectedWorkout = ref(null)
const showDeleteConfirm = ref(false)
const userWeightUnit = ref('lbs')
const isEditingTimes = ref(false)
const editDate = ref('')
const editStartTime = ref('')
const editEndTime = ref('')
const savingTimes = ref(false)

const sortedWorkouts = computed(() => {
  return [...workouts.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const viewWorkout = (workout) => {
  selectedWorkout.value = workout
  showDeleteConfirm.value = false
  isEditingTimes.value = false
}

const getWorkoutStartTime = (workout) => {
  return workout.start_time || workout.date
}

const getWorkoutEndTime = (workout) => {
  if (workout.end_time) return workout.end_time
  const start = new Date(getWorkoutStartTime(workout))
  return new Date(start.getTime() + (workout.duration || 0) * 60000).toISOString()
}

const toDateInputValue = (dateValue) => {
  const date = new Date(dateValue)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const toTimeInputValue = (dateValue) => {
  const date = new Date(dateValue)
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

const combineDateAndTime = (dateString, timeString) => {
  const [year, month, day] = dateString.split('-').map(Number)
  const [hours, minutes] = timeString.split(':').map(Number)
  return new Date(year, month - 1, day, hours, minutes)
}

const startEditingTimes = () => {
  if (!selectedWorkout.value) return
  const startDateTime = new Date(getWorkoutStartTime(selectedWorkout.value))
  const endDateTime = new Date(getWorkoutEndTime(selectedWorkout.value))

  editDate.value = toDateInputValue(startDateTime)
  editStartTime.value = toTimeInputValue(startDateTime)
  editEndTime.value = toTimeInputValue(endDateTime)
  isEditingTimes.value = true
}

const cancelEditingTimes = () => {
  isEditingTimes.value = false
}

const saveWorkoutTimes = async () => {
  if (!selectedWorkout.value) return

  const startDateTime = combineDateAndTime(editDate.value, editStartTime.value)
  const endDateTime = combineDateAndTime(editDate.value, editEndTime.value)

  if (endDateTime <= startDateTime) {
    error('End time must be after start time.')
    return
  }

  try {
    savingTimes.value = true
    const duration = Math.ceil((endDateTime.getTime() - startDateTime.getTime()) / 60000)
    const updatedWorkout = await updateWorkout(selectedWorkout.value.id, {
      date: startDateTime.toISOString(),
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString(),
      duration
    })

    selectedWorkout.value = updatedWorkout
    isEditingTimes.value = false
    success('Workout time updated successfully')
  } catch (err) {
    console.error('Failed to update workout time:', err)
    error('Failed to update workout time. Please try again.')
  } finally {
    savingTimes.value = false
  }
}

const getTotalVolumeInUserUnit = (workout) => {
  return workout.exercises.reduce((total, exercise) => {
    return total + exercise.sets.reduce((sum, set) => {
      if (!set.completed) return sum
      // Weight is stored in lbs, convert to user's preferred unit
      const weightInUserUnit = convertWeight(set.weight, 'lbs', userWeightUnit.value)
      return sum + (weightInUserUnit * set.reps)
    }, 0)
  }, 0)
}

const getDisplayWeight = (set) => {
  // Weight is stored in lbs in database
  // If set has a unit recorded, show it in that unit, otherwise use user preference
  const displayUnit = set.unit || userWeightUnit.value
  const weight = convertWeight(set.weight, 'lbs', displayUnit)
  return { weight, unit: displayUnit }
}

const handleDeleteWorkout = async () => {
  if (!selectedWorkout.value) return

  try {
    await deleteWorkout(selectedWorkout.value.id)
    selectedWorkout.value = null
    showDeleteConfirm.value = false
    success('Workout deleted successfully')
  } catch (err) {
    console.error('Failed to delete workout:', err)
    error('Failed to delete workout. Please try again.')
  }
}

onMounted(async () => {
  fetchWorkouts()

  // Load user profile to get weight unit preference
  try {
    const response = await api.getProfile()
    userWeightUnit.value = response.data.weight_unit || 'lbs'
  } catch (err) {
    console.error('Failed to load user profile:', err)
    userWeightUnit.value = 'lbs'
  }
})
</script>
