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


export type AnalysisVerse = {
  text: string

  rhymeletter?: string | null
  rhymeclass?: number | null

  stanza?: number

  metre?: string
  metrum?: string
  pattern?: string
  rythm?: string

  clause?: string
  foot?: number
}

export type AnalysisResponse = {
  id: string

  verses?: AnalysisVerse[]

  title?: string | null
  author_name?: string | null
  plaintext?: string | null

  form?: string | null
  mood?: string | null
  motives?: string[] | null
  present_metres?: string[]

  geninput?: {
    modelspec?: string | null
    collection_style?: string | null
    [key: string]: unknown
  }
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