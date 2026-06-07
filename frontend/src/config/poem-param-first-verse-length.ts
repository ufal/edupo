export const MIN_FIRST_VERSE_LENGTH = 1
export const MAX_FIRST_VERSE_LENGTH = 20
export const FIRST_VERSE_LENGTH_STEP = 1
export const DEFAULT_FIRST_VERSE_LENGTH = 16

export function isValidFirstVerseLength(value: number) {
  return (
    Number.isInteger(value) &&
    value >= MIN_FIRST_VERSE_LENGTH &&
    value <= MAX_FIRST_VERSE_LENGTH
  )
}

export function getRandomFirstVerseLength() {
  return (
    Math.floor(
      Math.random() *
        (MAX_FIRST_VERSE_LENGTH - MIN_FIRST_VERSE_LENGTH + 1),
    ) + MIN_FIRST_VERSE_LENGTH
  )
}