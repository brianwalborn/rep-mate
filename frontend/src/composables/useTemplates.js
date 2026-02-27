import { ref } from 'vue'
import api from '../services/api'

export function useTemplates() {
  const templates = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchTemplates = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getTemplates()
      templates.value = response.data
    } catch (err) {
      error.value = err
      console.error('Failed to fetch templates:', err)
    } finally {
      loading.value = false
    }
  }

  const getTemplate = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.getTemplate(id)
      return response.data
    } catch (err) {
      error.value = err
      console.error('Failed to fetch template:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const createTemplate = async (template) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.createTemplate(template)
      templates.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err
      console.error('Failed to create template:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTemplate = async (id, template) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.updateTemplate(id, template)
      const index = templates.value.findIndex(t => t.id === id)
      if (index !== -1) {
        templates.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err
      console.error('Failed to update template:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteTemplate = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.deleteTemplate(id)
      templates.value = templates.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = err
      console.error('Failed to delete template:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    templates,
    loading,
    error,
    fetchTemplates,
    getTemplate,
    createTemplate,
    updateTemplate,
    deleteTemplate
  }
}
