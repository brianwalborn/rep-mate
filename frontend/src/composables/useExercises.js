import { ref } from 'vue'
import api from '../services/api'

export function useExercises() {
  const exercises = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchExercises = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getExercises()
      exercises.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to load exercises'
      console.error('Failed to fetch exercises:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createExercise = async (exerciseData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.createExercise(exerciseData)
      exercises.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to create exercise'
      console.error('Failed to create exercise:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateExercise = async (id, exerciseData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateExercise(id, exerciseData)
      const index = exercises.value.findIndex(ex => ex.id === id)
      if (index !== -1) {
        exercises.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to update exercise'
      console.error('Failed to update exercise:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteExercise = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteExercise(id)
      const index = exercises.value.findIndex(ex => ex.id === id)
      if (index !== -1) {
        exercises.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err.message || 'Failed to delete exercise'
      console.error('Failed to delete exercise:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    exercises,
    loading,
    error,
    fetchExercises,
    createExercise,
    updateExercise,
    deleteExercise
  }
}
