import { ref } from 'vue'
import api from '../services/api'

export function useMuscles() {
  const muscles = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchMuscles = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getMuscles()
      muscles.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to load muscles'
      console.error('Failed to fetch muscles:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createMuscle = async (muscleData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.createMuscle(muscleData)
      muscles.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to create muscle'
      console.error('Failed to create muscle:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateMuscle = async (id, muscleData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateMuscle(id, muscleData)
      const index = muscles.value.findIndex(m => m.id === id)
      if (index !== -1) {
        muscles.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to update muscle'
      console.error('Failed to update muscle:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteMuscle = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteMuscle(id)
      const index = muscles.value.findIndex(m => m.id === id)
      if (index !== -1) {
        muscles.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err.message || 'Failed to delete muscle'
      console.error('Failed to delete muscle:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    muscles,
    loading,
    error,
    fetchMuscles,
    createMuscle,
    updateMuscle,
    deleteMuscle
  }
}
