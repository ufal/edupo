import { create } from 'zustand'
import type {
  Poem,
  PoemGenerationParams,
  PoemLineGroup,
  PoemMode,
} from '@/types/poem'
import { getPoetrySampleById } from '@/services/poetry-samples-service'
import { mapPoemResponseToPoem } from '@/services/api/poem-response-mapper'
import {
  fetchAnalysisApi,
  fetchPoemApi,
  generatePoemApi,
  sendLikeApi
} from '@/services/api/edupo-api'
import type { AnalysisResponse, GeneratePoemParams } from '@/types/edupo-api'

export const MAX_POEM_LINES = 10

type GenerationStatus = 'idle' | 'loading' | 'success' | 'error'
type AnalysisStatus = 'idle' | 'loading' | 'success' | 'error'

const demoLines = [
  { id: 'line-1', text: 'Co zbývá mně, než volat: Všecko jest v Bohu a bez viny?', group: 'A' as const },
  { id: 'line-2', text: 'Jdu mlhavou, tmy spjatou cestou, za svědkem, jenž nevěří', group: 'A' as const },
  { id: 'line-3', text: 'si připjal k plášti rudý prapor, hřímáje v mé hlubiny:', group: 'B' as const },
  { id: 'line-4', text: 'Jak mohou dál jít bez křiku, bez hrozby, v klid a důvěry?', group: 'B' as const },
  { id: 'line-5', text: 'Je pravda, věk že minul, plný vzletu, síly', group: 'C' as const },
]

const demoPoem: Poem = {
  id: 'demo-poem-1',
  title: 'Nač ještě vzpomínat',
  text: demoLines.map((line) => line.text).join('\n'),
  lines: demoLines,
  createdAt: new Date().toISOString(),
}

function parseRhymeLetter(value: string | null | undefined): PoemLineGroup {
  const letter = value?.trim().toUpperCase()

  if (
    letter === 'A' ||
    letter === 'B' ||
    letter === 'C' ||
    letter === 'D' ||
    letter === 'E' ||
    letter === 'F' ||
    letter === 'G' ||
    letter === 'X'
  ) {
    return letter
  }

  return 'X'
}

function applyAnalysisToPoem(poem: Poem, analysis: AnalysisResponse): Poem {
  const analysisVerses = analysis.verses ?? []

  const currentLines =
    poem.lines?.length
      ? poem.lines
      : poem.text
          .split('\n')
          .map((lineText, index) => ({
            id: `line-${index + 1}`,
            text: lineText,
          }))

  const lines = currentLines.map((line, index) => ({
    ...line,
    group: parseRhymeLetter(analysisVerses[index]?.rhymeletter),
  }))

  return {
    ...poem,
    lines,
  }
}

function getPoemLinesText(poem: Poem) {
  if (poem.lines?.length) {
    return poem.lines.map((line) => line.text)
  }

  return poem.text.split('\n')
}

function getLastEditedCharIndex(original: string, current: string) {
  if (original === current) return null

  let prefixLength = 0

  while (
    prefixLength < original.length &&
    prefixLength < current.length &&
    original[prefixLength] === current[prefixLength]
  ) {
    prefixLength += 1
  }

  let suffixLength = 0

  while (
    suffixLength < original.length - prefixLength &&
    suffixLength < current.length - prefixLength &&
    original[original.length - 1 - suffixLength] ===
      current[current.length - 1 - suffixLength]
  ) {
    suffixLength += 1
  }

  return Math.max(current.length - suffixLength - 1, prefixLength - 1)
}

function buildFirstWordsFromEditedPoem(poem: Poem) {
  if (!poem.originalText) return undefined

  const originalLines = poem.originalText.split('\n')
  const currentLines = getPoemLinesText(poem)

  for (let lineIndex = currentLines.length - 1; lineIndex >= 0; lineIndex -= 1) {
    const originalLine = originalLines[lineIndex] ?? ''
    const currentLine = currentLines[lineIndex] ?? ''

    const boundaryIndex = getLastEditedCharIndex(originalLine, currentLine)

    if (boundaryIndex === null) continue

    return currentLines
      .slice(0, lineIndex + 1)
      .map((line, index) => {
        if (index < lineIndex) return line

        return line.slice(0, boundaryIndex + 1)
      })
      .join('\n')
  }

  return undefined
}

type PoemState = {
  poem: Poem | null
  params: PoemGenerationParams
  status: GenerationStatus
  error: string | null
  analysisStatus: AnalysisStatus
  analysisError: string | null
  mode: PoemMode
  selectedAuthorStyleId: string | null
  likedPoemIds: Record<string, true>
  likingPoemIds: Record<string, true>

  likePoem: (poemId: string) => Promise<void>
  setPoem: (poem: Poem) => void
  setParams: (params: PoemGenerationParams) => void
  updateParams: (params: Partial<PoemGenerationParams>) => void
  setStatus: (status: GenerationStatus) => void
  setError: (error: string | null) => void
  setMode: (mode: PoemMode) => void
  resetPoem: () => void
  loadPoemById: (poemId: string) => Promise<Poem>
  loadPoemAnalysis: (poemId: string) => Promise<void>
  generatePoem: () => Promise<Poem>
  updatePoemLine: (lineId: string, text: string) => void
  addPoemLine: () => string | null
  removePoemLine: (lineId: string) => void
  generateDemoPoem: () => Promise<void>
  loadPoetrySample: (id: string) => Promise<void>
  setSelectedAuthorStyleId: (authorStyleId: string) => void
}

export const usePoemStore = create<PoemState>((set, get) => ({
  poem: null,
  params: {},
  status: 'idle',
  error: null,
  analysisStatus: 'idle',
  analysisError: null,
  mode: 'reading',
  selectedAuthorStyleId: null,
  likedPoemIds: {},
  likingPoemIds: {},

  likePoem: async (poemId) => {
    const state = get()

    if (state.likedPoemIds[poemId] || state.likingPoemIds[poemId]) {
      return
    }

    set((state) => ({
      likingPoemIds: {
        ...state.likingPoemIds,
        [poemId]: true,
      },
    }))

    try {
      await sendLikeApi(poemId)

      set((state) => {
        const { [poemId]: _removed, ...restLikingPoemIds } = state.likingPoemIds

        return {
          likedPoemIds: {
            ...state.likedPoemIds,
            [poemId]: true,
          },
          likingPoemIds: restLikingPoemIds,
        }
      })
    } catch (error) {
      console.error(error)

      set((state) => {
        const { [poemId]: _removed, ...restLikingPoemIds } = state.likingPoemIds

        return {
          likingPoemIds: restLikingPoemIds,
        }
      })
    }
  },

  setPoem: (poem) =>
    set({
      poem,
      status: 'success',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    }),

  setParams: (params) => set({ params }),

  updateParams: (params) =>
    set((state) => ({
      params: {
        ...state.params,
        ...params,
      },
    })),

  setStatus: (status) => set({ status }),

  setError: (error) =>
    set({
      error,
      status: error ? 'error' : 'idle',
    }),

  setMode: (mode) => set({ mode }),

  resetPoem: () =>
    set({
      poem: null,
      status: 'idle',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    }),

  loadPoemById: async (poemId: string) => {
    set({
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    })

    try {
      const response = await fetchPoemApi(poemId)
      const poem = mapPoemResponseToPoem(response)

      set({
        poem,
        status: 'success',
        error: null,
      })

      void get().loadPoemAnalysis(poem.id)

      return poem
    } catch (error) {
      console.error(error)

      set({
        status: 'error',
        error: 'Nepodařilo se načíst báseň.',
      })

      throw error
    }
  },

  loadPoemAnalysis: async (poemId: string) => {
    set({
      analysisStatus: 'loading',
      analysisError: null,
    })

    try {
      const analysis = await fetchAnalysisApi(poemId)

      set((state) => {
        if (!state.poem || state.poem.id !== poemId) {
          return state
        }

        return {
          poem: applyAnalysisToPoem(state.poem, analysis),
          analysisStatus: 'success',
          analysisError: null,
        }
      })
    } catch (error) {
      console.error(error)

      if (get().poem?.id !== poemId) return

      set({
        analysisStatus: 'error',
        analysisError: 'Nepodařilo se načíst analýzu básně.',
      })
    }
  },

  generatePoem: async () => {
    set({
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    })

    const params = get().params

    const poem = get().poem
    const firstWords = poem ? buildFirstWordsFromEditedPoem(poem) : undefined

    const generationParams: GeneratePoemParams = {
      title: params.title ?? undefined,

      motifs:
        params.motifs && params.motifs.length > 0
          ? params.motifs
          : undefined,

      form:
        params.form === 'free'
          ? undefined
          : params.form ?? undefined,

      verseCount: params.verseCount ?? undefined,

      rhymeScheme:
        !params.form || params.form === 'free' || params.form === 'epigram'
          ? params.rhymeScheme ?? undefined
          : undefined,

      firstVerseLength: params.firstVerseLength ?? undefined,

      metrum: params.metrum ?? undefined,

      temperature: params.temperature ?? undefined,

      first_words: firstWords ? [firstWords] : undefined,

      authorStyleId: params.authorStyleId ?? undefined,
    }

    try {
      const response = await generatePoemApi(generationParams)
      const poem = mapPoemResponseToPoem(response)

      set({
        poem,
        status: 'success',
        error: null,
        mode: 'reading',
      })

      void get().loadPoemAnalysis(poem.id)

      return poem
    } catch (error) {
      console.error(error)

      set({
        status: 'error',
        error: 'Nepodařilo se vygenerovat báseň.',
      })

      throw error
    }
  },

  updatePoemLine: (lineId, text) =>
    set((state) => {
      if (!state.poem) return state

      const currentLines =
        state.poem.lines?.length
          ? state.poem.lines
          : state.poem.text
              .split('\n')
              .map((lineText, index) => ({
                id: `line-${index + 1}`,
                text: lineText,
              }))

      const lines = currentLines.map((line) =>
        line.id === lineId ? { ...line, text } : line,
      )

      return {
        poem: {
          ...state.poem,
          lines,
          text: lines.map((line) => line.text).join('\n'),
        },
      }
    }),

  addPoemLine: () => {
    const newLineId = `line-${Date.now()}`

    set((state) => {
      if (!state.poem) return state

      const currentLines =
        state.poem.lines?.length
          ? state.poem.lines
          : state.poem.text
              .split('\n')
              .map((lineText, index) => ({
                id: `line-${index + 1}`,
                text: lineText,
              }))

      if (currentLines.length >= MAX_POEM_LINES) {
        return state
      }

      const lines = [
        ...currentLines,
        {
          id: newLineId,
          text: '',
        },
      ]

      return {
        poem: {
          ...state.poem,
          lines,
          text: lines.map((line) => line.text).join('\n'),
        },
      }
    })

    return newLineId
  },

  removePoemLine: (lineId) =>
    set((state) => {
      if (!state.poem) return state

      const currentLines =
        state.poem.lines?.length
          ? state.poem.lines
          : state.poem.text
              .split('\n')
              .map((lineText, index) => ({
                id: `line-${index + 1}`,
                text: lineText,
              }))

      const lines = currentLines.filter((line) => line.id !== lineId)

      return {
        poem: {
          ...state.poem,
          lines,
          text: lines.map((line) => line.text).join('\n'),
        },
      }
    }),

  generateDemoPoem: async () => {
    set({
      poem: null,
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    })

    await new Promise((resolve) => setTimeout(resolve, 4600))

    set({
      poem: {
        ...demoPoem,
        createdAt: new Date().toISOString(),
      },
      status: 'success',
      error: null,
      analysisStatus: 'success',
      analysisError: null,
    })
  },

  loadPoetrySample: async (id) => {
    set({
      poem: null,
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
    })

    await new Promise((resolve) => setTimeout(resolve, 1200))

    const sample = getPoetrySampleById(id)

    if (!sample) {
      set({
        status: 'error',
        error: 'Nepodařilo se načíst ukázku.',
      })
      return
    }

    set({
      poem: {
        ...sample.poem,
        createdAt: new Date().toISOString(),
      },
      status: 'success',
      analysisStatus: 'success',
      analysisError: null,
    })
  },

  setSelectedAuthorStyleId: (authorStyleId) =>
    set((state) => ({
      selectedAuthorStyleId: authorStyleId,
      params: {
        ...state.params,
        authorStyleId,
      },
    })),
}))