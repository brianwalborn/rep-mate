import { ref } from 'vue'
import api from '../services/api'

export function useWorkouts() {
  const workouts = ref([])
  const currentWorkout = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchWorkouts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getWorkouts()
      workouts.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to load workouts'
      console.error('Failed to fetch workouts:', err)
      throw err
    } finally {
      loading.value = false
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
    error,
    fetchWorkouts,
    fetchWorkout,
    createWorkout,
    updateWorkout,
    deleteWorkout
  }
}
