import type { PoemForm, PoemMetrum } from '@/types/poem'

import { apiGetJson, apiGetText } from './http-client'

import type {
  AddLikeResponse,
  AnalysisResponse,
  AuthorsListResponse,
  FetchPoemParams,
  FetchPoemResponse,
  GeneratePoemParams,
  GeneratePoemResponse,
  ImageResponse,
  MotivesResponse,
  PoemsListResponse,
  TTSResponse,
} from '@/types/edupo-api'

const MAX_AUTHORS = 20
const MAX_POEMS = 20

function parsePoemsList(text: string): PoemsListResponse {
  const poems: PoemsListResponse = []
  const lines = text.split('\n')

  for (const line of lines) {
    const colonIndex = line.indexOf(':')

    if (colonIndex <= 0) continue

    const idPart = line.slice(0, colonIndex).trim()
    const titlePart = line.slice(colonIndex + 1).trim()

    const id = Number.parseInt(idPart, 10)

    if (!Number.isNaN(id) && titlePart.length > 0) {
      poems.push({
        id,
        title: titlePart,
      })
    }

    if (poems.length >= MAX_POEMS) {
      break
    }
  }

  return poems
}

export async function fetchAuthorsListApi(): Promise<AuthorsListResponse> {
  const data = await apiGetJson<unknown>('showlist', {
    accept: 'json',
  })

  return Array.isArray(data)
    ? data.slice(0, MAX_AUTHORS) as AuthorsListResponse
    : []
}

export async function fetchPoemsListApi(
  author: string,
): Promise<PoemsListResponse> {
  const text = await apiGetText('showauthor', {
    author,
    accept: 'txt',
  })

  return parsePoemsList(text)
}

export async function fetchPoemApi(
  poemId: string,
): Promise<FetchPoemResponse> {
  return apiGetJson<FetchPoemResponse>('show', {
    accept: 'json',
    poemid: poemId,
  })
}

const METRUM_TO_BACKEND: Record<PoemMetrum, string> = {
  trochej: 'T',
  jamb: 'J',
  daktyl: 'D',
  volný: 'N',
}

const AUTHOR_STYLE_TO_BACKEND = {
  macha: 'Mácha, Karel Hynek',
  erben: 'Erben, Karel Jaromír',
  neruda: 'Neruda, Jan',
  borovsky: 'Borovský, Karel Havlíček',
  vrchlicky: 'Vrchlický, Jaroslav',
} as const

export async function generatePoemApi(
  params: GeneratePoemParams,
): Promise<GeneratePoemResponse> {

  const shouldSendRhymeScheme = !params.form || params.form === 'free' || params.form === 'epigram'
  const shouldSendVerseCount = !params.form || params.form === 'free' || params.form === 'epigram'
  const shouldSendFirstVerseLength = params.form !== 'haiku'

  return apiGetJson<GeneratePoemResponse>('gen', {
    accept: 'json',
    modelspec: 'tm',
    
    title: params.title,
    motives: params.motifs?.join('\n'),
    form: params.form,
    metre: params.metrum
      ? METRUM_TO_BACKEND[params.metrum]
      : undefined,

    verses_count: shouldSendVerseCount ? params.verseCount : undefined,
    rhyme_scheme: shouldSendRhymeScheme ? params.rhymeScheme : undefined,
    syllables_count: shouldSendFirstVerseLength ? params.firstVerseLength : undefined,
    temperature: params.temperature,
    first_words: params.first_words?.join('\n'),
    author: params.authorStyleId
      ? AUTHOR_STYLE_TO_BACKEND[params.authorStyleId as keyof typeof AUTHOR_STYLE_TO_BACKEND]
      : undefined,
  })
}

export async function fetchAnalysisApi(
  poemId: string | number,
): Promise<AnalysisResponse> {
  return apiGetJson<AnalysisResponse>('analyze', {
    poemid: poemId,
    accept: 'json',
  })
}

export async function fetchMotivesApi(
  poemId: string | number,
): Promise<MotivesResponse> {
  return apiGetJson<MotivesResponse>('genmotives', {
    poemid: poemId,
    accept: 'json',
  })
}

export async function fetchImageApi(
  poemId: string | number,
): Promise<ImageResponse> {
  return apiGetJson<ImageResponse>('genimage', {
    poemid: poemId,
    accept: 'json',
  })
}

export async function fetchTTSApi(
  poemId: string | number,
): Promise<TTSResponse> {
  return apiGetJson<TTSResponse>('gentts', {
    poemid: poemId,
    accept: 'json',
  })
}

export async function sendLikeApi(
  poemId: string | number,
): Promise<AddLikeResponse> {
  return apiGetJson<AddLikeResponse>('add_like', {
    poemid: poemId,
    accept: 'json',
  })
}