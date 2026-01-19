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
 * Format volume - shows "K" for thousands, or 2 decimals for kg
 */
export function formatVolume(volume, unit = 'lbs') {
  if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`
  }
  if (unit === 'kg') {
    // For kg under 1000, round to 2 decimal places
    // If it's a whole number, show without decimals
    const rounded = volume.toFixed(2)
    return parseFloat(rounded).toString()
  }
  return Math.round(volume).toString()
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

/**
 * Convert pounds to kilograms
 */
export function lbsToKg(lbs) {
  return lbs / 2.20462
}

/**
 * Convert kilograms to pounds
 */
export function kgToLbs(kg) {
  return kg * 2.20462
}

/**
 * Convert weight from one unit to another
 */
export function convertWeight(weight, fromUnit, toUnit) {
  if (fromUnit === toUnit) return weight
  if (fromUnit === 'lbs' && toUnit === 'kg') return lbsToKg(weight)
  if (fromUnit === 'kg' && toUnit === 'lbs') return kgToLbs(weight)
  return weight
}

/**
 * Format weight for display with appropriate decimals
 */
export function formatWeight(weight, unit = 'lbs') {
  if (unit === 'kg') {
    return weight.toFixed(1) // Show 1 decimal for kg
  }
  return Math.round(weight).toString() // No decimals for lbs
}

