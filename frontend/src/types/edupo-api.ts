import type {
  PoemForm,
  PoemMetrum,
  PoemModelSpec,
  PoemMood,
} from '@/types/poem'

export type Author = string

export type AuthorsListResponse = Author[]

export type PoemListItem = {
  id: number
  title: string
}

export type PoemsListResponse = PoemListItem[]

export type FetchPoemParams = {
  poemid: string | number
  accept?: 'json'
}

export type GeneratePoemParams = {
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
  first_words?: string[]
  authorStyleId?: string
  collectionId?: string
}

export type PoemIdParams = {
  poemid: string | number
}

export type FetchPoemResponse = GeneratePoemResponse

export type GeneratePoemResponse = {
  id: string
  title: string
  author_name: string
  plaintext: string
  rawtext: string
  geninput: Record<string, unknown>
  imgfile: string | null
  imgtitle: string | null
  mood: string | null
  motives: string[] | null
  ttsfile: string | null
}

export type AnalysisMeasures = {
  form: string
  line_repetitions: number
  metre_accuracy: number
  metre_consistency: number
  poem_metre: string
  rhyme_scheme: string[][]
  rhyme_scheme_accuracy: number
  rhyming: number
  rhyming_consistency: number
  syllable_count_entropy: number
  syllables_in_verses: number[][]
  unknown_words: number
  verses_in_stanzas: number[]
  word_repetitions: number
}

export type AnalysisResponse = {
  measures: AnalysisMeasures
}


export type AddLikeResponse = number | string

export type TTSResponse = {
  url: string
}
export type MotivesResponse = unknown
export type ImageResponse = unknown

export type AvailableModel = {
  generic_identifier: string
  human_readable_identifier: string
  precise_identifier: string
  default: boolean
  fallback: boolean
}

export type AvailableModelsResponse = {
  models: AvailableModel[]
}