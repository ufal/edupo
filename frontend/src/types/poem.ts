export type PoemMode = 'reading' | 'analysis' | 'editing'

export const POEM_MODES: PoemMode[] = ['reading', 'analysis', 'editing']

export function isPoemMode(value: string | null): value is PoemMode {
  return value !== null && POEM_MODES.includes(value as PoemMode)
}

export type PoemForm = 'haiku' | 'limerik' | 'sonet'
export type PoemMetrum = 'daktyl' | 'jamb' | 'trochej' | 'volný'
export type PoemMood = 'veselá' | 'smutná'

export type PoemModelSpec = string

export type PoemGenerationParams = {
  title?: string
  motifs?: string[]
  form?: PoemForm
  verseCount?: number
  maxStrophes?: number
  rhymeScheme?: string
  firstVerseLength?: number
  metrum?: PoemMetrum
  temperature?: number
  mood?: PoemMood
  modelSpec?: PoemModelSpec
  firstWords?: string[]
  authorStyleId?: string
}

export type PoemLineGroup = 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'X'

export type PoemLine = {
  id: string
  text: string
  originalText?: string
  group?: PoemLineGroup
  stanzaStart?: boolean
}


export type Poem = {
  id: string
  title?: string
  authorName?: string
  text: string
  originalText?: string
  lines?: PoemLine[]
  createdAt?: string
  source?: 'backend' | 'local'
}