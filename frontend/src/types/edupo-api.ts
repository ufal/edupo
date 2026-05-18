import type { PoemForm, PoemMetrum } from '@/types/poem'

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
  rhymeScheme?: string
  firstVerseLength?: number
  metrum?: PoemMetrum
  temperature?: number
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
}

export type AnalysisResponse = {
  id: string
  verses?: AnalysisVerse[]
}

export type AddLikeResponse = number | string

export type TTSResponse = {
  url: string
}
export type MotivesResponse = unknown
export type ImageResponse = unknown
