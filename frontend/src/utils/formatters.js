/**
 * Format a date string to a readable format
 * Shows "Today", "Yesterday", or full date
 */
export function formatDate(dateString) {
  const date = new Date(dateString)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday'
  } else {
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    })
  }
}

/**
 * Format a date string to time (e.g., "2:30 PM")
 * Handles timezone-less datetime strings by appending 'Z'
 */
export function formatTime(dateString) {
  let date
  if (typeof dateString === 'string' && !dateString.includes('Z') && !dateString.match(/[+-]\d{2}:\d{2}$/)) {
    // Append 'Z' to treat as UTC if no timezone info present
    date = new Date(dateString + 'Z')
  } else {
    date = new Date(dateString)
  }

  return date.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

/**
 * Format volume (lbs) - shows "K" for thousands
 */
export function formatVolume(volume) {
  if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`
  }
  return volume.toString()
}

/**
 * Calculate total number of sets in a workout
 */
export function getTotalSets(workout) {
  return workout.exercises.reduce((total, exercise) => total + exercise.sets.length, 0)
}

/**
 * Calculate total volume (weight × reps) for completed sets in a workout
 */
export function getTotalVolume(workout) {
  return workout.exercises.reduce((total, exercise) => {
    return total + exercise.sets.reduce((sum, set) => {
      return sum + (set.completed ? set.weight * set.reps : 0)
    }, 0)
  }, 0)
}

/**
 * Get unique list of muscles from a workout's exercises
 */
export function getUniqueMuscles(workout) {
  const musclesSet = new Set()
  workout.exercises.forEach(exercise => {
    if (exercise.muscles && Array.isArray(exercise.muscles)) {
      exercise.muscles.forEach(muscle => musclesSet.add(muscle))
    }
  })
  return Array.from(musclesSet).sort()
}
