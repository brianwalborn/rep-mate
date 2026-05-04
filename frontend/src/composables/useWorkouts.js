import { ref } from 'vue'
import api from '../services/api'

const PAGE_SIZE = 10

export function useWorkouts() {
  const workouts = ref([])
  const currentWorkout = ref(null)
  const loading = ref(false)
  const loadingMore = ref(false)
  const hasMore = ref(true)
  const error = ref(null)

  const fetchWorkouts = async () => {
    loading.value = true
    error.value = null
    workouts.value = []
    hasMore.value = true
    try {
      const response = await api.getWorkouts(0, PAGE_SIZE)
      workouts.value = response.data
      hasMore.value = response.data.length === PAGE_SIZE
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to load workouts'
      console.error('Failed to fetch workouts:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchMoreWorkouts = async () => {
    if (loadingMore.value || !hasMore.value) return
    loadingMore.value = true
    try {
      const response = await api.getWorkouts(workouts.value.length, PAGE_SIZE)
      workouts.value.push(...response.data)
      hasMore.value = response.data.length === PAGE_SIZE
    } catch (err) {
      error.value = err.message || 'Failed to load more workouts'
      console.error('Failed to fetch more workouts:', err)
    } finally {
      loadingMore.value = false
    }
  }

  const fetchWorkout = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getWorkout(id)
      currentWorkout.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to load workout'
      console.error('Failed to fetch workout:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createWorkout = async (workoutData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.createWorkout(workoutData)
      workouts.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to create workout'
      console.error('Failed to create workout:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateWorkout = async (id, workoutData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateWorkout(id, workoutData)
      const index = workouts.value.findIndex(w => w.id === id)
      if (index !== -1) {
        workouts.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to update workout'
      console.error('Failed to update workout:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteWorkout = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteWorkout(id)
      const index = workouts.value.findIndex(w => w.id === id)
      if (index !== -1) {
        workouts.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err.message || 'Failed to delete workout'
      console.error('Failed to delete workout:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    workouts,
    currentWorkout,
    loading,
    loadingMore,
    hasMore,
    error,
    fetchWorkouts,
    fetchMoreWorkouts,
    fetchWorkout,
    createWorkout,
    updateWorkout,
    deleteWorkout
  }
}
