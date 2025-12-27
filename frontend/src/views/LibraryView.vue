<template>
  <div class="min-h-screen bg-black text-white pb-20 lg:pb-8 lg:pl-64 px-5 lg:px-8 pt-6 lg:pt-12">
    <PageHeader title="Library" />

    <!-- Tabs -->
    <div class="flex gap-2 mb-6 overflow-x-auto whitespace-nowrap no-scrollbar">
      <button
        @click="activeTab = 'exercises'"
        class="px-6 py-3 rounded-xl font-semibold transition-all flex-shrink-0"
        :class="activeTab === 'exercises' ? 'bg-primary text-white' : 'bg-[#1a1a1a] text-gray-400 hover:text-white'"
      >
        Exercises
      </button>
      <button
        @click="activeTab = 'equipment'"
        class="px-6 py-3 rounded-xl font-semibold transition-all flex-shrink-0"
        :class="activeTab === 'equipment' ? 'bg-primary text-white' : 'bg-[#1a1a1a] text-gray-400 hover:text-white'"
      >
        Equipment
      </button>
      <button
        @click="activeTab = 'muscles'"
        class="px-6 py-3 rounded-xl font-semibold transition-all flex-shrink-0"
        :class="activeTab === 'muscles' ? 'bg-primary text-white' : 'bg-[#1a1a1a] text-gray-400 hover:text-white'"
      >
        Muscles
      </button>
      <button
        @click="activeTab = 'templates'"
        class="px-6 py-3 rounded-xl font-semibold transition-all flex-shrink-0"
        :class="activeTab === 'templates' ? 'bg-primary text-white' : 'bg-[#1a1a1a] text-gray-400 hover:text-white'"
      >
        Templates
      </button>
    </div>

    <!-- Search Bar -->
    <div class="mb-6 lg:max-w-2xl">
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="activeTab === 'exercises' ? 'Search exercises...' : activeTab === 'equipment' ? 'Search equipment...' : activeTab === 'muscles' ? 'Search muscles...' : 'Search templates...'"
        class="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
      />
    </div>

    <!-- Exercises Tab Content -->
    <div v-if="activeTab === 'exercises'">
      <div class="space-y-3 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0 pb-24">
        <button
          v-for="exercise in filteredExercises"
          :key="exercise.id"
          @click="openEditExerciseModal(exercise)"
          class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 hover:border-primary transition-colors text-left w-full"
        >
          <h3 class="font-semibold mb-1">{{ exercise.name }}</h3>
          <div class="text-sm text-gray-500">
            {{ exercise.muscles.join(', ') }} • {{ exercise.equipment }}
          </div>
        </button>
      </div>

      <EmptyState
        v-if="filteredExercises.length === 0"
        :icon="BookOpenIcon"
        title="No exercises found"
        description="Try a different search term"
      />
    </div>

    <!-- Equipment Tab Content -->
    <div v-if="activeTab === 'equipment'">
      <div class="space-y-3 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0 pb-24">
        <button
          v-for="equipmentItem in filteredEquipment"
          :key="equipmentItem.id"
          @click="openEditEquipmentModal(equipmentItem)"
          class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 hover:border-primary transition-colors text-left w-full"
        >
          <h3 class="font-semibold">{{ equipmentItem.name }}</h3>
        </button>
      </div>

      <EmptyState
        v-if="filteredEquipment.length === 0"
        :icon="BookOpenIcon"
        title="No equipment found"
        description="Try a different search term"
      />
    </div>

    <!-- Muscles Tab Content -->
    <div v-if="activeTab === 'muscles'">
      <div class="space-y-3 lg:grid lg:grid-cols-2 lg:gap-4 lg:space-y-0 pb-24">
        <button
          v-for="muscle in filteredMuscles"
          :key="muscle.id"
          @click="openEditMuscleModal(muscle)"
          class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 hover:border-primary transition-colors text-left w-full"
        >
          <h3 class="font-semibold">{{ muscle.name }}</h3>
        </button>
      </div>

      <EmptyState
        v-if="filteredMuscles.length === 0"
        :icon="BookOpenIcon"
        title="No muscles found"
        description="Try a different search term"
      />
    </div>

    <!-- Templates Tab Content -->
    <div v-if="activeTab === 'templates'">
      <EmptyState
        :icon="BookOpenIcon"
        title="Workout Templates"
        description="Coming soon"
      />
    </div>

    <!-- Split Pill FAB -->
    <FloatingActionButton v-if="activeTab !== 'templates'" @click="openCreateModal">
      <template #default>
        <span class="text-3xl lg:text-4xl">+</span>
      </template>
    </FloatingActionButton>

    <!-- Create/Edit Modal (Exercise or Muscle) -->
    <BaseModal
      v-model="showModal"
      :title="modalMode === 'equipment' ? (editingEquipment ? 'Edit Equipment' : 'Add Equipment') : modalMode === 'exercise' ? (editingExercise ? 'Edit Exercise' : 'Add Exercise') : (editingMuscle ? 'Edit Muscle' : 'Add Muscle')"
      max-width="lg:w-[600px]"
      content-padding="p-6 pb-24 lg:pb-8"
    >
      <!-- Exercise Form -->
        <form v-if="modalMode === 'exercise'" @submit.prevent="saveExercise" class="space-y-4">
          <div>
            <label class="text-sm text-gray-400 mb-2 block">Exercise Name</label>
            <input
              v-model="exerciseFormData.name"
              type="text"
              required
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="e.g., Bench Press"
            />
          </div>

          <div>
            <label class="text-sm text-gray-400 mb-2 block">Equipment</label>
            <div class="relative">
              <button
                type="button"
                @click="showEquipmentDropdown = !showEquipmentDropdown"
                class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary text-left flex justify-between items-center"
              >
                <span v-if="!exerciseFormData.equipment_id" class="text-gray-500">Select equipment</span>
                <span v-else>{{ equipment.find(e => e.id === exerciseFormData.equipment_id)?.name }}</span>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div
                v-if="showEquipmentDropdown"
                class="absolute z-[60] w-full mt-2 bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl max-h-60 overflow-y-auto"
              >
                <button
                  v-for="equipmentOption in equipment"
                  :key="equipmentOption.id"
                  type="button"
                  @click="exerciseFormData.equipment_id = equipmentOption.id; showEquipmentDropdown = false"
                  class="w-full text-left px-4 py-3 hover:bg-[#3a3a3a] cursor-pointer transition-colors"
                  :class="{ 'bg-primary/10 text-primary': exerciseFormData.equipment_id === equipmentOption.id }"
                >
                  {{ equipmentOption.name }}
                </button>
              </div>
            </div>
          </div>

          <div>
            <label class="text-sm text-gray-400 mb-2 block">Muscle Groups</label>
            <div class="relative">
              <button
                type="button"
                @click="showMuscleDropdown = !showMuscleDropdown"
                class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary text-left flex justify-between items-center"
              >
                <span v-if="exerciseFormData.muscles.length === 0" class="text-gray-500">Select muscle groups</span>
                <span v-else class="flex flex-wrap gap-1">
                  <span v-for="muscle in exerciseFormData.muscles" :key="muscle" class="bg-primary/20 text-primary px-2 py-0.5 rounded text-sm">
                    {{ muscle }}
                  </span>
                </span>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div
                v-if="showMuscleDropdown"
                class="absolute z-[60] w-full mt-2 bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl max-h-60 overflow-y-auto"
              >
                <label
                  v-for="muscle in muscles"
                  :key="muscle.id"
                  class="flex items-center gap-3 px-4 py-3 hover:bg-[#3a3a3a] cursor-pointer transition-colors"
                >
                  <input
                    type="checkbox"
                    :value="muscle.name"
                    v-model="exerciseFormData.muscles"
                    class="w-4 h-4 rounded border-gray-600 bg-[#1a1a1a] text-primary focus:ring-primary focus:ring-offset-0"
                  />
                  <span>{{ muscle.name }}</span>
                </label>
                <div v-if="muscles.length === 0" class="px-4 py-3 text-gray-500 text-sm">
                  No muscles available. Add them in the Muscles tab.
                </div>
              </div>
            </div>
            <p v-if="exerciseFormData.muscles.length === 0" class="text-red-500 text-sm mt-1 hidden" :class="{'!block': errorMessage && errorMessage.includes('muscle')}">
              Please select at least one muscle group
            </p>
          </div>

          <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>

          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 bg-gradient-to-r from-primary to-primary-light text-white font-semibold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button
              v-if="editingExercise"
              type="button"
              @click="deleteExerciseHandler"
              :disabled="saving"
              class="flex-1 bg-red-600/10 border border-red-600 text-red-600 font-semibold py-3 rounded-xl hover:bg-red-600/20 transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </form>

        <!-- Muscle Form -->
        <form v-if="modalMode === 'muscle'" @submit.prevent="saveMuscle" class="space-y-4">
          <div>
            <label class="text-sm text-gray-400 mb-2 block">Muscle Name</label>
            <input
              v-model="muscleFormData.name"
              type="text"
              required
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="e.g., Chest"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 bg-gradient-to-r from-primary to-primary-light text-white font-semibold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button
              v-if="editingMuscle"
              type="button"
              @click="deleteMuscleHandler"
              :disabled="saving"
              class="flex-1 bg-red-600/10 border border-red-600 text-red-600 font-semibold py-3 rounded-xl hover:bg-red-600/20 transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </form>

        <!-- Equipment Form -->
        <form v-if="modalMode === 'equipment'" @submit.prevent="saveEquipment" class="space-y-4">
          <div>
            <label class="text-sm text-gray-400 mb-2 block">Equipment Name</label>
            <input
              v-model="equipmentFormData.name"
              type="text"
              required
              class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
              placeholder="e.g., Barbell"
            />
          </div>

          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              :disabled="saving"
              class="flex-1 bg-gradient-to-r from-primary to-primary-light text-white font-semibold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button
              v-if="editingEquipment"
              type="button"
              @click="deleteEquipmentHandler"
              :disabled="saving"
              class="flex-1 bg-red-600/10 border border-red-600 text-red-600 font-semibold py-3 rounded-xl hover:bg-red-600/20 transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </form>
      </BaseModal>

    <!-- Delete Confirmation Modal -->
    <BaseModal
      v-model="showDeleteModal"
      :title="`Delete ${deleteMode === 'exercise' ? 'Exercise' : deleteMode === 'equipment' ? 'Equipment' : 'Muscle'}?`"
    >
      <p class="text-gray-400">
        Are you sure you want to delete <span class="text-white font-semibold">{{ deleteMode === 'exercise' ? editingExercise?.name : deleteMode === 'equipment' ? editingEquipment?.name : editingMuscle?.name }}</span>? This action cannot be undone.
      </p>

      <template #footer>
        <div class="p-6 pb-24 lg:pb-6">
          <div class="flex gap-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 bg-[#2a2a2a] text-white font-semibold py-3 rounded-xl hover:bg-[#3a3a3a] transition-colors"
            >
              Cancel
            </button>
            <button
              @click="confirmDelete"
              :disabled="saving"
              class="flex-1 bg-red-600 text-white font-semibold py-3 rounded-xl hover:bg-red-700 transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { BookOpenIcon } from '@heroicons/vue/24/outline'
import BaseModal from '../components/BaseModal.vue'
import EmptyState from '../components/EmptyState.vue'
import FloatingActionButton from '../components/FloatingActionButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { useEquipment } from '../composables/useEquipment'
import { useExercises } from '../composables/useExercises'
import { useMuscles } from '../composables/useMuscles'
import { useToast } from '../composables/useToast'

const { success, error: showError } = useToast()

const activeTab = ref('exercises')
const searchQuery = ref('')
const showModal = ref(false)
const showDeleteModal = ref(false)
const showMuscleDropdown = ref(false)
const showEquipmentDropdown = ref(false)
const modalMode = ref('exercise') // 'exercise', 'equipment', or 'muscle'
const deleteMode = ref('') // 'exercise', 'equipment', or 'muscle'
const editingExercise = ref(null)
const editingEquipment = ref(null)
const editingMuscle = ref(null)
const errorMessage = ref('')

// Use composables for data management
const {
  exercises,
  loading: exercisesLoading,
  fetchExercises,
  createExercise,
  updateExercise,
  deleteExercise
} = useExercises()

const {
  equipment,
  loading: equipmentLoading,
  fetchEquipment,
  createEquipment,
  updateEquipment,
  deleteEquipment
} = useEquipment()

const {
  muscles,
  loading: musclesLoading,
  fetchMuscles,
  createMuscle,
  updateMuscle,
  deleteMuscle
} = useMuscles()

const saving = computed(() => exercisesLoading.value || equipmentLoading.value || musclesLoading.value)

const exerciseFormData = ref({
  name: '',
  equipment_id: '',
  muscles: []
})

const equipmentFormData = ref({
  name: ''
})

const muscleFormData = ref({
  name: ''
})

const filteredExercises = computed(() => {
  if (!searchQuery.value) return exercises.value

  const query = searchQuery.value.toLowerCase()
  return exercises.value.filter(ex =>
    ex.name.toLowerCase().includes(query) ||
    ex.muscles.some(m => m.toLowerCase().includes(query)) ||
    ex.equipment.toLowerCase().includes(query)
  )
})

const filteredMuscles = computed(() => {
  if (!searchQuery.value) return muscles.value

  const query = searchQuery.value.toLowerCase()
  return muscles.value.filter(m =>
    m.name.toLowerCase().includes(query)
  )
})

const filteredEquipment = computed(() => {
  if (!searchQuery.value) return equipment.value

  const query = searchQuery.value.toLowerCase()
  return equipment.value.filter(eq =>
    eq.name.toLowerCase().includes(query)
  )
})

const openCreateModal = () => {
  if (activeTab.value === 'exercises') {
    modalMode.value = 'exercise'
    editingExercise.value = null
    exerciseFormData.value = {
      name: '',
      equipment_id: '',
      muscles: []
    }
    showMuscleDropdown.value = false
  } else if (activeTab.value === 'equipment') {
    modalMode.value = 'equipment'
    editingEquipment.value = null
    equipmentFormData.value = {
      name: ''
    }
  } else {
    modalMode.value = 'muscle'
    editingMuscle.value = null
    muscleFormData.value = {
      name: ''
    }
  }
  errorMessage.value = ''
  showModal.value = true
}

const openEditExerciseModal = (exercise) => {
  modalMode.value = 'exercise'
  editingExercise.value = exercise
  exerciseFormData.value = {
    name: exercise.name,
    equipment_id: equipment.value.find(eq => eq.name === exercise.equipment)?.id || '',
    muscles: [...exercise.muscles]
  }
  showMuscleDropdown.value = false
  errorMessage.value = ''
  showModal.value = true
}

const openEditEquipmentModal = (equipmentItem) => {
  modalMode.value = 'equipment'
  editingEquipment.value = equipmentItem
  equipmentFormData.value = {
    name: equipmentItem.name
  }
  errorMessage.value = ''
  showModal.value = true
}

const openEditMuscleModal = (muscle) => {
  modalMode.value = 'muscle'
  editingMuscle.value = muscle
  muscleFormData.value = {
    name: muscle.name
  }
  errorMessage.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  showMuscleDropdown.value = false
  editingExercise.value = null
  editingEquipment.value = null
  editingMuscle.value = null
  errorMessage.value = ''
}

const saveExercise = async () => {
  errorMessage.value = ''

  try {
    if (exerciseFormData.value.muscles.length === 0) {
      errorMessage.value = 'Please select at least one muscle group'
      return
    }

    const exerciseData = {
      name: exerciseFormData.value.name,
      equipment_id: exerciseFormData.value.equipment_id,
      muscles: exerciseFormData.value.muscles
    }

    if (editingExercise.value) {
      await updateExercise(editingExercise.value.id, exerciseData)
    } else {
      await createExercise(exerciseData)
    }

    closeModal()
  } catch (err) {
    errorMessage.value = err.message || 'Failed to save exercise. Please try again.'
  }
}

const saveMuscle = async () => {
  errorMessage.value = ''

  try {
    const muscleData = {
      name: muscleFormData.value.name
    }

    if (editingMuscle.value) {
      await updateMuscle(editingMuscle.value.id, muscleData)
    } else {
      await createMuscle(muscleData)
    }

    closeModal()
  } catch (err) {
    errorMessage.value = err.message || 'Failed to save muscle. Please try again.'
  }
}

const saveEquipment = async () => {
  errorMessage.value = ''

  try {
    const equipmentData = {
      name: equipmentFormData.value.name
    }

    if (editingEquipment.value) {
      await updateEquipment(editingEquipment.value.id, equipmentData)
    } else {
      await createEquipment(equipmentData)
    }

    closeModal()
  } catch (err) {
    errorMessage.value = err.message || 'Failed to save equipment. Please try again.'
  }
}

const deleteExerciseHandler = async () => {
  deleteMode.value = 'exercise'
  showDeleteModal.value = true
}

const deleteEquipmentHandler = async () => {
  deleteMode.value = 'equipment'
  showDeleteModal.value = true
}

const deleteMuscleHandler = async () => {
  deleteMode.value = 'muscle'
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  errorMessage.value = ''

  try {
    if (deleteMode.value === 'exercise') {
      await deleteExercise(editingExercise.value.id)
      success('Exercise deleted successfully')
    } else if (deleteMode.value === 'equipment') {
      await deleteEquipment(editingEquipment.value.id)
      success('Equipment deleted successfully')
    } else {
      await deleteMuscle(editingMuscle.value.id)
      success('Muscle deleted successfully')
    }
    showDeleteModal.value = false
    closeModal()
  } catch (err) {
    errorMessage.value = err.message || `Failed to delete ${deleteMode.value}. Please try again.`
    showDeleteModal.value = false
  }
}

onMounted(async () => {
  // Fetch exercises, equipment, and muscles from the backend
  try {
    await Promise.all([
      fetchExercises(),
      fetchEquipment(),
      fetchMuscles()
    ])
  } catch (err) {
    console.error('Failed to load data:', err)
  }
})
</script>
