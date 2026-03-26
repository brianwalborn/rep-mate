<template>
  <div class="min-h-screen bg-black text-white pb-20 lg:pb-8 lg:pl-64">
    <!-- Top Bar -->
    <div class="px-5 lg:px-8 pt-6 lg:pt-12 pb-2 mb-6">
      <div class="flex items-center gap-3 mb-4">
        <button @click="goBack" class="text-gray-500 hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="w-2 h-8 bg-primary rounded-full"></div>
        <div class="text-[28px] lg:text-4xl font-bold leading-tight">
          {{ isEditMode ? 'Edit Template' : 'New Template' }}
        </div>
      </div>
    </div>

    <!-- Template Info -->
    <div class="px-5 lg:px-8 mb-6">
      <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-[20px] p-5 space-y-4">
        <div>
          <label class="text-sm text-gray-400 mb-2 block">Template Name</label>
          <input
            v-model="templateName"
            type="text"
            placeholder="e.g., Push Day, Leg Day"
            class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
          />
        </div>
        <div>
          <label class="text-sm text-gray-400 mb-2 block">Description (Optional)</label>
          <textarea
            v-model="templateDescription"
            placeholder="Add notes about this template..."
            rows="2"
            class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary resize-none"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Section Header -->
    <div class="px-5 lg:px-8 pb-4">
      <div class="text-[22px] lg:text-2xl font-bold">Exercises</div>
    </div>

    <!-- Exercise List -->
    <div class="px-5 lg:px-8 pb-24">
      <div v-if="templateExercises.length === 0" class="text-center py-12 text-gray-500">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <p>No exercises added yet</p>
        <p class="text-sm mt-1">Click the + button to add exercises</p>
      </div>

      <draggable
        v-model="templateExercises"
        item-key="id"
        handle=".drag-handle"
        :animation="150"
        ghost-class="opacity-30"
      >
        <template #item="{ element: exercise }">
      <div
        :key="exercise.id"
        class="bg-[#1a1a1a] rounded-[20px] p-5 border-2 border-[#2a2a2a] mb-4"
      >
        <!-- Exercise Header -->
        <div class="flex items-start gap-2" :class="{ 'mb-4': !isCollapsed(exercise.id) }">
          <!-- Drag Handle -->
          <div class="drag-handle cursor-grab active:cursor-grabbing text-gray-600 hover:text-gray-400 pt-1.5 flex-shrink-0 touch-none select-none">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 16 16">
              <circle cx="5" cy="3.5" r="1.5"/><circle cx="11" cy="3.5" r="1.5"/>
              <circle cx="5" cy="8" r="1.5"/><circle cx="11" cy="8" r="1.5"/>
              <circle cx="5" cy="12.5" r="1.5"/><circle cx="11" cy="12.5" r="1.5"/>
            </svg>
          </div>
          <button
            @click="toggleCollapse(exercise.id)"
            class="flex-1 text-left"
          >
            <div class="flex items-start gap-2">
              <svg
                class="w-5 h-5 mt-0.5 text-gray-500 transition-transform flex-shrink-0"
                :class="{ 'rotate-180': !isCollapsed(exercise.id) }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              <div class="flex-1">
                <h3 class="text-lg font-semibold mb-1">{{ exercise.name }}</h3>
                <div class="text-sm text-gray-500">
                  {{ exercise.muscles.join(', ') }} • {{ exercise.equipment }}
                </div>
              </div>
            </div>
          </button>
          <div class="flex gap-1">
            <button
              v-if="!isCardioEquipment(exercise.equipment) && exercise.equipment !== 'Bodyweight'"
              @click="toggleExerciseUnit(exercise.id)"
              class="text-gray-500 hover:text-primary transition-colors px-3 py-2 text-sm font-semibold rounded-lg hover:bg-[#2a2a2a]"
              :class="{ 'text-primary bg-primary/10': exercise.unit === 'kg' }"
              title="Switch weight unit"
            >
              {{ exercise.unit || 'lbs' }}
            </button>
            <button
              @click="openNotesModal(exercise)"
              class="text-gray-500 hover:text-primary transition-colors p-2"
              :class="{ 'text-primary': exercise.notes }"
              title="Add notes"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
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
        </div>

        <!-- Notes Display -->
        <div v-if="exercise.notes && !isCollapsed(exercise.id)" class="mb-4 p-3 bg-[#2a2a2a] rounded-lg text-sm text-gray-300">
          {{ exercise.notes }}
        </div>

        <!-- Sets (skip for cardio) -->
        <div v-if="!isCardioEquipment(exercise.equipment) && !isCollapsed(exercise.id)" class="space-y-2">
          <div
            v-for="(set, setIndex) in exercise.sets"
            :key="setIndex"
            class="flex items-center gap-3 bg-[#2a2a2a] rounded-xl p-3"
          >
            <div class="w-8 text-center text-gray-500 font-semibold">{{ setIndex + 1 }}</div>

            <div v-if="exercise.equipment !== 'Bodyweight'" class="flex-1">
              <label class="text-xs text-gray-500 mb-1 block">Weight ({{ exercise.unit || 'lbs' }})</label>
              <input
                v-model.number="set.weight"
                type="number"
                :step="exercise.unit === 'kg' ? '0.5' : '5'"
                placeholder="0"
                class="w-full bg-[#1a1a1a] border border-[#3a3a3a] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>

            <div class="flex-1">
              <label class="text-xs text-gray-500 mb-1 block">Reps</label>
              <input
                v-model.number="set.reps"
                type="number"
                placeholder="0"
                class="w-full bg-[#1a1a1a] border border-[#3a3a3a] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>

            <button
              v-if="exercise.sets.length > 1"
              @click="removeSet(exercise.id, setIndex)"
              class="text-gray-500 hover:text-red-500 transition-colors p-2"
              title="Remove set"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Add Set Button -->
          <button
            @click="addSet(exercise.id)"
            class="w-full py-3 text-primary hover:bg-primary/10 rounded-xl transition-colors text-sm font-semibold"
          >
            + Add Set
          </button>
        </div>
      </div>
        </template>
      </draggable>
    </div>

    <!-- FloatingActionButton for Save/Add -->
    <FloatingActionButton v-if="templateExercises.length === 0">
      <template #default>
        <button
          @click="showAddExercise = true"
          class="w-14 h-14 lg:w-16 lg:h-16 rounded-full bg-gradient-to-br from-primary to-primary-light text-white shadow-lg hover:scale-105 active:scale-95 transition-transform flex items-center justify-center"
        >
          <span class="text-3xl lg:text-4xl">+</span>
        </button>
      </template>
    </FloatingActionButton>

    <FloatingActionButton v-else>
      <template #buttons>
        <!-- Save Template Button -->
        <button
          @click="saveTemplate"
          :disabled="!canSave || saving"
          class="w-14 h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-full text-white shadow-lg hover:scale-105 active:scale-95 transition-transform flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
          title="Save Template"
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
      content-padding="p-6 pb-24 lg:pb-8"
    >
      <div class="mb-4">
        <input
          v-model="exerciseSearch"
          type="text"
          placeholder="Search exercises..."
          class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary"
        />
      </div>

      <div class="space-y-2 max-h-[400px] overflow-y-auto">
        <button
          v-for="exercise in filteredLibraryExercises"
          :key="exercise.id"
          @click="addExerciseFromLibrary(exercise)"
          class="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 hover:border-primary transition-colors text-left"
        >
          <h3 class="font-semibold mb-1">{{ exercise.name }}</h3>
          <div class="text-sm text-gray-500">
            {{ exercise.muscles.join(', ') }} • {{ exercise.equipment }}
          </div>
        </button>
      </div>

      <EmptyState
        v-if="filteredLibraryExercises.length === 0"
        :icon="BookOpenIcon"
        title="No exercises found"
        description="Try a different search term"
      />
    </BaseModal>

    <!-- Notes Modal -->
    <BaseModal
      v-model="showNotesModal"
      title="Exercise Notes"
      max-width="lg:w-[600px]"
      content-padding="p-6 pb-24 lg:pb-8"
    >
      <textarea
        v-model="notesText"
        placeholder="Add notes for this exercise..."
        rows="6"
        class="w-full bg-[#2a2a2a] border border-[#3a3a3a] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary resize-none mb-4"
      ></textarea>

      <div class="flex gap-3">
        <button
          @click="saveNotes"
          class="flex-1 bg-primary hover:bg-primary/90 text-white font-semibold py-3 rounded-xl transition-colors"
        >
          Save
        </button>
        <button
          v-if="editingExerciseForNotes?.notes"
          @click="clearNotes"
          class="px-6 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-gray-400 font-semibold py-3 rounded-xl transition-colors"
        >
          Clear
        </button>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import draggable from 'vuedraggable'
import { useRoute, useRouter } from 'vue-router'
import { BookOpenIcon } from '@heroicons/vue/24/outline'
import BaseModal from '../components/BaseModal.vue'
import EmptyState from '../components/EmptyState.vue'
import FloatingActionButton from '../components/FloatingActionButton.vue'
import { useExercises } from '../composables/useExercises'
import { useTemplates } from '../composables/useTemplates'
import { useToast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const { success, error: showError } = useToast()

const { exercises: exerciseLibrary, fetchExercises } = useExercises()
const { getTemplate, createTemplate, updateTemplate } = useTemplates()

const isEditMode = computed(() => route.params.id && route.params.id !== 'new')
const templateId = computed(() => route.params.id)

// Template data
const templateName = ref('')
const templateDescription = ref('')
const templateExercises = ref([])

// UI state
const showAddExercise = ref(false)
const showNotesModal = ref(false)
const exerciseSearch = ref('')
const editingExerciseForNotes = ref(null)
const notesText = ref('')
const saving = ref(false)
const userWeightUnit = ref('lbs')
const collapsedExercises = ref(new Set())

const canSave = computed(() => {
  const hasValidExercises = templateExercises.value.some(ex => ex.sets.length > 0)
  return templateName.value.trim() && hasValidExercises
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

const isCardioEquipment = (equipment) => {
  return equipment === 'Treadmill' || equipment === 'Bike'
}

const addExerciseFromLibrary = (libraryExercise) => {
  const newExercise = {
    id: Date.now(),
    exerciseId: libraryExercise.id,
    name: libraryExercise.name,
    equipment: libraryExercise.equipment,
    muscles: libraryExercise.muscles,
    notes: '',
    unit: userWeightUnit.value,
    sets: isCardioEquipment(libraryExercise.equipment)
      ? []
      : [{ weight: null, reps: null, unit: userWeightUnit.value }]
  }

  templateExercises.value.push(newExercise)
  showAddExercise.value = false
  exerciseSearch.value = ''
}

const removeExercise = (exerciseId) => {
  const index = templateExercises.value.findIndex(ex => ex.id === exerciseId)
  if (index !== -1) {
    templateExercises.value.splice(index, 1)
  }
}

const addSet = (exerciseId) => {
  const exercise = templateExercises.value.find(ex => ex.id === exerciseId)
  if (exercise && exercise.sets.length > 0) {
    const lastSet = exercise.sets[exercise.sets.length - 1]
    exercise.sets.push({
      weight: lastSet.weight,
      reps: lastSet.reps,
      unit: exercise.unit || userWeightUnit.value
    })
  } else if (exercise) {
    exercise.sets.push({
      weight: null,
      reps: null,
      unit: exercise.unit || userWeightUnit.value
    })
  }
}

const removeSet = (exerciseId, setIndex) => {
  const exercise = templateExercises.value.find(ex => ex.id === exerciseId)
  if (exercise && exercise.sets.length > 1) {
    exercise.sets.splice(setIndex, 1)
  }
}

const toggleExerciseUnit = (exerciseId) => {
  const exercise = templateExercises.value.find(ex => ex.id === exerciseId)
  if (exercise) {
    const newUnit = exercise.unit === 'lbs' ? 'kg' : 'lbs'
    exercise.unit = newUnit
    exercise.sets.forEach(set => {
      set.unit = newUnit
    })
  }
}

const openNotesModal = (exercise) => {
  editingExerciseForNotes.value = exercise
  notesText.value = exercise.notes || ''
  showNotesModal.value = true
}

const saveNotes = () => {
  if (editingExerciseForNotes.value) {
    editingExerciseForNotes.value.notes = notesText.value
  }
  showNotesModal.value = false
  editingExerciseForNotes.value = null
  notesText.value = ''
}

const clearNotes = () => {
  if (editingExerciseForNotes.value) {
    editingExerciseForNotes.value.notes = ''
  }
  showNotesModal.value = false
  editingExerciseForNotes.value = null
  notesText.value = ''
}

const toggleCollapse = (exerciseId) => {
  if (collapsedExercises.value.has(exerciseId)) {
    collapsedExercises.value.delete(exerciseId)
  } else {
    collapsedExercises.value.add(exerciseId)
  }
}

const isCollapsed = (exerciseId) => {
  return collapsedExercises.value.has(exerciseId)
}

const saveTemplate = async () => {
  if (!canSave.value) return

  saving.value = true
  try {
    const templateData = {
      name: templateName.value,
      description: templateDescription.value || null,
      exercises: templateExercises.value
        .filter(ex => ex.sets.length > 0) // Skip exercises with no sets (cardio)
        .map((ex, index) => ({
          exercise_id: ex.exerciseId,
          order: index,
          notes: ex.notes || null,
          sets: ex.sets.map((set, setIndex) => ({
            set_number: setIndex + 1,
            weight: set.weight,
            reps: set.reps,
            unit: set.unit || ex.unit || 'lbs'
          }))
        }))
    }

    if (isEditMode.value) {
      await updateTemplate(templateId.value, templateData)
      success('Template updated successfully!')
    } else {
      await createTemplate(templateData)
      success('Template created successfully!')
    }

    router.push('/library')
  } catch (err) {
    showError('Failed to save template. Please try again.')
    console.error('Error saving template:', err)
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push('/library')
}

const loadTemplate = async () => {
  if (!isEditMode.value) return

  try {
    const template = await getTemplate(templateId.value)
    templateName.value = template.name
    templateDescription.value = template.description || ''

    templateExercises.value = template.exercises.map(ex => ({
      id: Date.now() + Math.random(),
      exerciseId: ex.exercise_id,
      name: ex.exercise_name,
      equipment: ex.equipment,
      muscles: ex.muscles || [],
      notes: ex.notes || '',
      unit: ex.sets[0]?.unit || 'lbs',
      sets: ex.sets.map(set => ({
        weight: set.weight,
        reps: set.reps,
        unit: set.unit
      }))
    }))
  } catch (err) {
    showError('Failed to load template')
    console.error('Error loading template:', err)
    router.push('/library')
  }
}

onMounted(async () => {
  await fetchExercises()
  if (isEditMode.value) {
    await loadTemplate()
  }
})
</script>
