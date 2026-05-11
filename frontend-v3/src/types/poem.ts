export type PoemMode = 'reading' | 'analysis' | 'editing'

export const POEM_MODES: PoemMode[] = ['reading', 'analysis', 'editing']

export function isPoemMode(value: string | null): value is PoemMode {
  return value !== null && POEM_MODES.includes(value as PoemMode)
}

export type PoemForm = 'free' | 'sonet' | 'limerik' | 'haiku' | 'epigram'
export type PoemMetrum = 'trochej' | 'jamb' | 'daktyl' | 'volný'

export type PoemGenerationParams = {
  title?: string
  motifs?: string[]
  form?: PoemForm
  verseCount?: number
  rhymeScheme?: string
  firstVerseLength?: number
  metrum?: PoemMetrum
  temperature?: number
  firstWords?: string[]
  authorStyleId?: string
}

export type PoemLineGroup = 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'X'

export type PoemLine = {
  id: string
  text: string
  group?: PoemLineGroup
}

export type Poem = {
  id: string
  title?: string
  text: string
  originalText?: string
  lines?: PoemLine[]
  createdAt?: string
}