import axios from 'axios'
import config from './config'

const api = axios.create({
  baseURL: config.getApiUrl(),
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth
  login(credentials) {
    return api.post('/auth/login', credentials)
  },
  register(userData) {
    return api.post('/auth/register', userData)
  },
  getProfile() {
    return api.get('/auth/me')
  },
  updateProfile(data) {
    return api.put('/auth/me', data)
  },

  // Workouts
  getWorkouts() {
    return api.get('/workouts')
  },
  getWorkout(id) {
    return api.get(`/workouts/${id}`)
  },
  createWorkout(workout) {
    return api.post('/workouts', workout)
  },
  updateWorkout(id, workout) {
    return api.put(`/workouts/${id}`, workout)
  },
  deleteWorkout(id) {
    return api.delete(`/workouts/${id}`)
  },

  // Exercises
  getExercises() {
    return api.get('/exercises')
  },
  getExercise(id) {
    return api.get(`/exercises/${id}`)
  },
  createExercise(exercise) {
    return api.post('/exercises', exercise)
  },
  updateExercise(id, exercise) {
    return api.put(`/exercises/${id}`, exercise)
  },
  deleteExercise(id) {
    return api.delete(`/exercises/${id}`)
  },

  // Equipment
  getEquipment() {
    return api.get('/equipment')
  },
  createEquipment(equipment) {
    return api.post('/equipment', equipment)
  },
  updateEquipment(id, equipment) {
    return api.put(`/equipment/${id}`, equipment)
  },
  deleteEquipment(id) {
    return api.delete(`/equipment/${id}`)
  },

  // Muscles
  getMuscles() {
    return api.get('/muscles')
  },
  createMuscle(muscle) {
    return api.post('/muscles', muscle)
  },
  updateMuscle(id, muscle) {
    return api.put(`/muscles/${id}`, muscle)
  },
  deleteMuscle(id) {
    return api.delete(`/muscles/${id}`)
  }
}
