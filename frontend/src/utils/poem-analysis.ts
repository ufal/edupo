
import type { AnalysisResponse } from '@/types/edupo-api'

export function formatPercentage(value: number): string {
  return `${Math.round(value * 100)} %`
}

export function formatAnalysisMetre(value: string): string {
  const name = value.trim()

  if (!name) return 'Neurčeno'

  return name.charAt(0).toLocaleUpperCase('cs-CZ') + name.slice(1)
}

export function getAnalysisVerseCounts(
  analysis: AnalysisResponse,
): string {
  return analysis.measures.verses_in_stanzas.join(' ') || '—'
}

export function getAnalysisVerseLengths(
  analysis: AnalysisResponse,
): string[] {
  return analysis.measures.syllables_in_verses.map(
    (stanza) => stanza.join(' '),
  )
}

export function getAnalysisRhymeScheme(
  analysis: AnalysisResponse,
): string {
  return analysis.measures.rhyme_scheme
    .map((stanza) => stanza.join(''))
    .join(' ') || '—'
}
