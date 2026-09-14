export const MIN_STROPHES = 1
export const MAX_STROPHES = 5
export const STROPHE_COUNT_STEP = 1
export const DEFAULT_MAX_STROPHES = 1

export function isValidMaxStrophes(value: number) {
  return (
    Number.isInteger(value) &&
    value >= MIN_STROPHES &&
    value <= MAX_STROPHES
  )
}

export function getRandomMaxStrophes() {
  return (
    Math.floor(
      Math.random() * (MAX_STROPHES - MIN_STROPHES + 1),
    ) + MIN_STROPHES
  )
}