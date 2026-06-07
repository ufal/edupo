export const MIN_TEMPERATURE = 0.1
export const MAX_TEMPERATURE = 1
export const TEMPERATURE_STEP = 0.1
export const DEFAULT_TEMPERATURE = 0.7

export function isValidTemperature(value: number) {
  return (
    Number.isFinite(value) &&
    value >= MIN_TEMPERATURE &&
    value <= MAX_TEMPERATURE
  )
}

export function normalizeTemperature(value: number) {
  return Number(value.toFixed(1))
}

export function getRandomTemperature() {
  return normalizeTemperature(
    Math.random() * (MAX_TEMPERATURE - MIN_TEMPERATURE) + MIN_TEMPERATURE,
  )
}