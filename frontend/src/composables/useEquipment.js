import { ref } from 'vue'
import api from '../services/api'

export function useEquipment() {
  const equipment = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchEquipment = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getEquipment()
      equipment.value = response.data
    } catch (err) {
      error.value = err.message || 'Failed to fetch equipment'
      console.error('Failed to fetch equipment:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createEquipment = async (equipmentData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.createEquipment(equipmentData)
      equipment.value.push(response.data)
      equipment.value.sort((a, b) => a.name.localeCompare(b.name))
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to create equipment'
      console.error('Failed to create equipment:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateEquipment = async (id, equipmentData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateEquipment(id, equipmentData)
      const index = equipment.value.findIndex(eq => eq.id === id)
      if (index !== -1) {
        equipment.value[index] = response.data
      }
      equipment.value.sort((a, b) => a.name.localeCompare(b.name))
      return response.data
    } catch (err) {
      error.value = err.message || 'Failed to update equipment'
      console.error('Failed to update equipment:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteEquipment = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteEquipment(id)
      const index = equipment.value.findIndex(eq => eq.id === id)
      if (index !== -1) {
        equipment.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err.message || 'Failed to delete equipment'
      console.error('Failed to delete equipment:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    equipment,
    loading,
    error,
    fetchEquipment,
    createEquipment,
    updateEquipment,
    deleteEquipment
  }
}
