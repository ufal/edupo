
import type { AnalysisResponse } from '@/types/edupo-api'

export function getAnalysisAuthor(
  analysis: AnalysisResponse,
): string | null {
  return (
    analysis.author_name
      ?.replace(/\s*\[(?:vygenerováno|vloženo uživatelem)\]\s*$/i, '')
      .trim() || null
  )
}

export function getAnalysisStanzaCount(
  analysis: AnalysisResponse,
): number | null {
  const verses = analysis.verses

  if (!verses?.length) return null

  // Vyžadujeme údaje o strofě pro všechny verše.
  if (
    !verses.every(
      (verse) =>
        typeof verse.stanza === 'number' &&
        Number.isInteger(verse.stanza) &&
        verse.stanza >= 0,
    )
  ) {
    return null
  }

  return new Set(verses.map((verse) => verse.stanza)).size
}

export function getAnalysisMetre(
  analysis: AnalysisResponse,
): string | null {
  const verses = analysis.verses

  if (!verses?.length) return null

  const metres = [
    ...new Set(
      verses
        .map((verse) => verse.metrum?.trim().toLowerCase())
        .filter(
          (value): value is string =>
            Boolean(value) && value !== 'neurčeno',
        ),
    ),
  ]

  if (metres.length === 0) {
    return 'Neurčeno'
  }

  // Část veršů má určené jiné nebo neznámé metrum.
  if (
    metres.length > 1 ||
    verses.some(
      (verse) =>
        !verse.metrum?.trim() ||
        verse.metrum.trim().toLowerCase() === 'neurčeno',
    )
  ) {
    return 'Smíšené metrum'
  }

  const name = metres[0]

  return name.charAt(0).toUpperCase() + name.slice(1)
}

export function getAnalysisRhymeScheme(
  analysis: AnalysisResponse,
): string | null {
  if (!analysis.verses?.length) return null

  return analysis.verses
    .map((verse) => verse.rhymeletter?.trim() || '–')
    .join(' ')
}

export function getAnalysisModel(
  analysis: AnalysisResponse,
): string | null {
  return analysis.geninput?.modelspec?.trim() || null
}

export function getAnalysisCollection(
  analysis: AnalysisResponse,
): string | null {
  return analysis.geninput?.collection_style?.trim() || null
}
