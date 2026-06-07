export const MIN_VERSES = 2
export const MAX_VERSES = 10
export const VERSE_COUNT_STEP = 2
export const DEFAULT_VERSE_COUNT = 6

export function isValidVerseCount(value: number) {
  return (
    Number.isInteger(value) &&
    value >= MIN_VERSES &&
    value <= MAX_VERSES &&
    (value - MIN_VERSES) % VERSE_COUNT_STEP === 0
  )
}

export function getRandomVerseCount() {
  const allowedValues = Array.from(
    { length: Math.floor((MAX_VERSES - MIN_VERSES) / VERSE_COUNT_STEP) + 1 },
    (_, index) => MIN_VERSES + index * VERSE_COUNT_STEP,
  )

  return allowedValues[Math.floor(Math.random() * allowedValues.length)]
}