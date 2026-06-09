import type { RhymeValue } from '@/components/ui/rhyme-slot-select'

export const MAX_RHYME_SCHEME_VERSES = 10
export const DEFAULT_RHYME_VALUE: RhymeValue = 'X'

export const RHYME_VALUES: RhymeValue[] = ['A', 'B', 'C', 'X']

export const FAVORITE_RHYME_SCHEMES = [
  'AABB',
  'ABAB',
  'ABBA',
  'XAXA',
  'AAXX',
  'XXXX',
  'AABBCC',
  'ABABCC',
  'ABABXX',
  'XXXXXX',
]

export function normalizeRhymeScheme(
  scheme: string | undefined,
  verseCount: number,
) {
  const chars = (scheme ?? '')
    .toUpperCase()
    .split('')
    .filter((char): char is RhymeValue =>
      RHYME_VALUES.includes(char as RhymeValue),
    )

  return Array.from({ length: MAX_RHYME_SCHEME_VERSES }, (_, index) => {
    if (index >= verseCount) return DEFAULT_RHYME_VALUE
    return chars[index] ?? DEFAULT_RHYME_VALUE
  })
}

export function rhymeSchemeToString(
  values: RhymeValue[],
  verseCount: number,
) {
  return values.slice(0, verseCount).join('')
}

export function getDefaultRhymeScheme(verseCount: number) {
  return DEFAULT_RHYME_VALUE.repeat(verseCount)
}

export function getFavoriteRhymeSchemes(verseCount: number) {
  return FAVORITE_RHYME_SCHEMES.filter((scheme) => scheme.length === verseCount)
}

export function getRandomRhymeScheme(verseCount: number) {
  const matching = getFavoriteRhymeSchemes(verseCount)

  if (matching.length > 0) {
    return matching[Math.floor(Math.random() * matching.length)]
  }

  return Array.from({ length: verseCount }, () => {
    return RHYME_VALUES[Math.floor(Math.random() * RHYME_VALUES.length)]
  }).join('')
}

export function getRhymeSchemeOptions(verseCount: number) {
  return getFavoriteRhymeSchemes(verseCount).map((scheme) => ({
    value: scheme,
    label: scheme,
  }))
}