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
  regeneratePoemLineApi,
  savePoemApi,
  sendLikeApi,
} from '@/services/api/edupo-api'
import type { AnalysisResponse, GeneratePoemParams } from '@/types/edupo-api'
import { useModelsStore } from '@/stores/models-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import {
  findAvailableModel,
  getDefaultModel,
} from '@/config/poem-param-model'
import { buildGenerationParams } from '@/services/poem-generation-params'
import {
  parsePlaintextToLines,
  serializePoemLines,
  movePoemLine,
} from '@/utils/poem-lines'
import type { PoemLine } from '@/types/poem'

export const MAX_POEM_LINES = 10

type GenerationStatus = 'idle' | 'loading' | 'success' | 'error'
type AnalysisStatus = 'idle' | 'loading' | 'success' | 'error'

const demoLines = [
  { id: 'line-1', text: 'Co zbývá mně, než volat: Všecko jest v Bohu a bez viny?', group: 'A' as const },
  { id: 'line-2', text: 'Jdu mlhavou, tmy spjatou cestou, za svědkem, jenž nevěří', group: 'A' as const },
  { id: 'line-3', text: 'si připjal k plášti rudý prapor, hřímáje v mé hlubiny:', group: 'B' as const },
  { id: 'line-4', text: 'Jak mohou dál jít bez křiku, bez hrozby, v klid a důvěry?', group: 'B' as const },
  { id: 'line-5', text: 'Je pravda, věk že minul, plný vzletu, síly', group: 'C' as const },
].map((line) => ({
  ...line,
  originalText: line.text,
}))

const demoPoem: Poem = {
  id: 'demo-poem-1',
  title: 'Nač ještě vzpomínat',
  text: demoLines.map((line) => line.text).join('\n'),
  originalText: demoLines.map((line) => line.text).join('\n'),
  lines: demoLines,
  createdAt: new Date().toISOString(),
  source: 'local',
}


function parseRhymeLetter(value: string | null | undefined): PoemLineGroup | undefined {

  if (typeof value !== 'string')
    return undefined
  
  const letter = value.trim().toUpperCase()

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

  return undefined
}

function normalizeVerseText(text: string): string {
  return text
    .normalize('NFC')
    .replace(/\s+/g, ' ')
    .trim()
}

function applyAnalysisToPoem(
  poem: Poem,
  analysis: AnalysisResponse,
): Poem | null {
  const currentLines =
    poem.lines?.length
      ? poem.lines
      : parsePlaintextToLines(poem.text)

  const analysisVerses = analysis.verses

  // Analýza musí patřit ke správné básni.
  if (analysis.id !== poem.id) {
    return null
  }

  // Musíme mít skutečné výsledky pro jednotlivé verše.
  if (!Array.isArray(analysisVerses)) {
    return null
  }

  // Počet veršů musí být shodný.
  if (analysisVerses.length !== currentLines.length) {
    return null
  }

  // Ověříme texty všech veršů ve stejném pořadí.
  const textsMatch = currentLines.every((line, index) => {
    const analyzedText = analysisVerses[index]?.text

    return (
      typeof analyzedText === 'string' &&
      normalizeVerseText(line.text) ===
        normalizeVerseText(analyzedText)
    )
  })

  if (!textsMatch) {
    return null
  }

  // Teprve nyní bezpečně přiřadíme rýmové skupiny.
  const lines = currentLines.map((line, index) => ({
    ...line,
    group: parseRhymeLetter(
      analysisVerses[index].rhymeletter,
    ),
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

  const originalLines = parsePlaintextToLines(poem.originalText).map((line) => line.text)
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

type GeneratePoemOptions = {
  respectDesktopUnset?: boolean
}

type PoemState = {
  poem: Poem | null
  params: PoemGenerationParams
  status: GenerationStatus
  error: string | null
  analysisStatus: AnalysisStatus
  analysisError: string | null
  analysisResult: AnalysisResponse | null
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
  generatePoem: (options?: GeneratePoemOptions) => Promise<Poem>
  regeneratePoemLine: (lineId: string) => Promise<Poem>
  updatePoemLine: (lineId: string, text: string) => void
  addPoemLine: () => string | null
  removePoemLine: (lineId: string) => void
  movePoemLine: (
    sourceId: string,
    targetId: string,
  ) => void
  restorePoemLine: (lineId: string) => void
  generateDemoPoem: () => Promise<void>
  loadPoetrySample: (id: string) => Promise<void>
  setSelectedAuthorStyleId: (authorStyleId: string) => void
  ensurePoemSaved: () => Promise<string>
  preparePoemAnalysis: () => Promise<void>
}

let pendingPoemSave: Promise<string> | null = null

function needsPoemSave(poem: Poem): boolean {
  return (
    poem.source !== 'backend' ||
    poem.originalText === undefined ||
    poem.text !== poem.originalText
  )
}

function syncPoemIdInUrl(poemId: string): void {
  if (typeof window === 'undefined') return

  const url = new URL(window.location.href)

  if (url.searchParams.get('poemId') === poemId) {
    return
  }

  url.searchParams.set('poemId', poemId)

  window.history.replaceState(
    window.history.state,
    '',
    `${url.pathname}${url.search}${url.hash}`,
  )
}

export const usePoemStore = create<PoemState>((set, get) => ({
  poem: null,
  params: {},
  status: 'idle',
  error: null,
  analysisStatus: 'idle',
  analysisError: null,
  analysisResult: null,
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
      analysisResult: null
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
  
  setMode: (mode) => {
    set({ mode })

    if (mode === 'analysis' && get().poem) {
      void get().preparePoemAnalysis()
    }
  },

  resetPoem: () =>
    set({
      poem: null,
      status: 'idle',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
      analysisResult: null
    }),

  preparePoemAnalysis: async () => {
    try {
      const poemId = await get().ensurePoemSaved()

      const state = get()

      // Uživatel mezitím mohl přepnout jinam.
      if (
        state.mode !== 'analysis' ||
        state.poem?.id !== poemId
      ) {
        return
      }

      // Pokud už máme platnou analýzu,
      // nemusíme ji stahovat znovu.
      if (
        state.analysisStatus === 'success' &&
        state.analysisResult?.id === poemId &&
        !needsPoemSave(state.poem)
      ) {
        return
      }

      await get().loadPoemAnalysis(poemId)
    } catch (error) {
      console.error(error)

      if (get().mode !== 'analysis') return

      set({
        analysisStatus: 'error',
        analysisResult: null,
        analysisError:
          'Nepodařilo se uložit báseň pro analýzu.',
      })
    }
  },

  ensurePoemSaved: async () => {
    const poem = get().poem

    if (!poem) {
      throw new Error('No poem is loaded.')
    }

    if (!needsPoemSave(poem)) {
      syncPoemIdInUrl(poem.id)
      return poem.id
    }

    // Pokud ukládání už běží, počkáme na něj.
    // Pak znovu ověříme aktuální podobu básně.
    if (pendingPoemSave) {
      await pendingPoemSave
      return get().ensurePoemSaved()
    }

    const snapshot = {
      id: poem.id,
      author: poem.authorName,
      title: poem.title,
      text: poem.text,
    }

    const savePromise = savePoemApi({
      author: snapshot.author,
      title: snapshot.title,
      text: snapshot.text,
    })

    pendingPoemSave = savePromise

    try {
      const savedId = await savePromise

      set((state) => {
        const current = state.poem

        // Během ukládání mohla být načtena jiná báseň.
        if (
          !current ||
          current.id !== snapshot.id ||
          current.title !== snapshot.title ||
          current.authorName !== snapshot.author
        ) {
          return state
        }

        return {
          poem: {
            ...current,
            id: savedId,
            source: 'backend',
            // Uložený je snapshot, nikoli nutně
            // nejnovější pracovní text.
            originalText: snapshot.text,
          },
          analysisResult: null,
          analysisStatus: 'idle',
          analysisError: null,
        }
      })
    } finally {
      if (pendingPoemSave === savePromise) {
        pendingPoemSave = null
      }
    }

    // Pokud uživatel mezitím dál editoval,
    // uložíme i novější pracovní podobu.
    return get().ensurePoemSaved()
  },

  loadPoemById: async (poemId: string) => {
    set({
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
      analysisResult: null
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
      analysisResult: null,
    })

    try {
      const analysis = await fetchAnalysisApi(poemId)

      set((state) => {
        if (
          !state.poem ||
          state.poem.id !== poemId ||
          needsPoemSave(state.poem)
        ) {
          return state
        }

        const analyzedPoem = applyAnalysisToPoem(
          state.poem,
          analysis,
        )

        if (!analyzedPoem) {
          console.warn(
            'Analýza neodpovídá aktuální podobě básně.',
            {
              poemId,
              analysisId: analysis.id,
            },
          )

          return {
            analysisResult: null,
            analysisStatus: 'error',
            analysisError:
              'Výsledky analýzy neodpovídají aktuální podobě básně.',
          }
        }

        return {
          poem: analyzedPoem,
          analysisResult: analysis,
          analysisStatus: 'success',
          analysisError: null,
        }
      })
    } catch (error) {
      console.error(error)

      if (get().poem?.id !== poemId || !get().poem || needsPoemSave(get().poem!))
        return

      set({
        analysisResult: null,
        analysisStatus: 'error',
        analysisError: 'Nepodařilo se načíst analýzu básně.',
      })
    }
  },

  generatePoem: async ({
    respectDesktopUnset = false,
  }: GeneratePoemOptions = {}) => {
    set({
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
      analysisResult: null,
    })

    // Zachytíme parametry a přepínače při zahájení generování.
    const params = get().params

    const unset = respectDesktopUnset
      ? { ...useDesktopSettingsUiStore.getState().unset }
      : undefined

    const currentPoem = get().poem

    const firstWords = currentPoem
      ? buildFirstWordsFromEditedPoem(currentPoem)
      : undefined

    const selectedCollectionId =
      useDesktopSettingsUiStore.getState().selectedCollectionId

    const generationParams: GeneratePoemParams =
      buildGenerationParams(
        params,
        unset,
        respectDesktopUnset ? selectedCollectionId : undefined,
      )

    // Dosavadní chování pokračování básně zatím ponecháváme.
    generationParams.first_words = firstWords
      ? [firstWords]
      : undefined

    try {
      if (unset?.modelSpec === true) {
        // Model není nastavený: backend použije svůj default.
        generationParams.modelSpec = undefined
      } else {
        const models = await useModelsStore.getState().loadModels()

        const selectedModel =
          findAvailableModel(models, generationParams.modelSpec) ??
          getDefaultModel(models)

        if (!selectedModel) {
          throw new Error('Není dostupný žádný výchozí AI model.')
        }

        generationParams.modelSpec =
          selectedModel.generic_identifier
      }

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

  regeneratePoemLine: async (lineId: string) => {
    const poem = get().poem

    if (!poem) {
      throw new Error('No poem is loaded.')
    }

    const line = poem.lines?.find((item) => item.id === lineId)

    if (!line || !line.text.trim()) {
      throw new Error('The selected poem line is empty or missing.')
    }

    set({
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
      analysisResult: null
    })

    try {
      const poemId = await get().ensurePoemSaved()

      const response = await regeneratePoemLineApi(poemId, line.text)
      const regeneratedPoem = mapPoemResponseToPoem(response)

      set({
        poem: regeneratedPoem,
        status: 'success',
        error: null,
        mode: 'editing',
      })

      void get().loadPoemAnalysis(regeneratedPoem.id)

      return regeneratedPoem
    } catch (error) {
      console.error(error)

      set({
        status: 'error',
        error: 'Nepodařilo se navrhnout úpravu verše.',
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
          : parsePlaintextToLines(state.poem.text)

      const lines = currentLines.map((line) =>
        line.id === lineId ? { ...line, text } : line,
      )

      const invalidatedLines = lines.map((line) => ({
        ...line,
        group: undefined,
      }))

      return {
        poem: {
          ...state.poem,
          lines: invalidatedLines,
          text: serializePoemLines(invalidatedLines),
        },
        analysisResult: null,
        analysisStatus: 'idle',
        analysisError: null,
      }
    }),
    
    restorePoemLine: (lineId) =>
      set((state) => {
        const poem = state.poem
        if (!poem) return state

        const currentLines =
          poem.lines?.length
            ? poem.lines
            : parsePlaintextToLines(poem.text)

        const currentLine = currentLines.find(
          (line) => line.id === lineId,
        )

        if (
          !currentLine ||
          currentLine.originalText === undefined ||
          currentLine.text === currentLine.originalText
        ) {
          return state
        }

        const lines = currentLines.map((line) =>
          line.id === lineId
            ? { ...line, text: line.originalText! }
            : line,
        )

        const invalidatedLines = lines.map((line) => ({
          ...line,
          group: undefined,
        }))

        return {
          poem: {
            ...poem,
            lines: invalidatedLines,
            text: serializePoemLines(invalidatedLines),
          },
          analysisResult: null,
          analysisStatus: 'idle',
          analysisError: null,
        }
      }),

    addPoemLine: () => {
      const poem = get().poem
      if (!poem) return null

      const currentLines = poem.lines?.length
        ? poem.lines
        : parsePlaintextToLines(poem.text)

      if (currentLines.length >= MAX_POEM_LINES) {
        return null
      }

      const newLineId = `line-${crypto.randomUUID()}`

      const lines = [
        ...currentLines,
        {
          id: newLineId,
          text: '',
          stanzaStart: false,
        },
      ]

      const invalidatedLines = lines.map((line) => ({
        ...line,
        group: undefined,
      }))

      set({
        poem: {
          ...poem,
          lines: invalidatedLines,
          text: serializePoemLines(invalidatedLines),
        },
        analysisResult: null,
        analysisStatus: 'idle',
        analysisError: null,
      })

      return newLineId
    },


  removePoemLine: (lineId) =>
    set((state) => {
      const poem = state.poem
      if (!poem) return state

      const currentLines = poem.lines?.length
        ? poem.lines
        : parsePlaintextToLines(poem.text)

      // V básni musí zůstat alespoň jeden verš.
      if (currentLines.length <= 1) return state

      const index = currentLines.findIndex(
        (line) => line.id === lineId,
      )

      if (index === -1) return state

      const removedLine = currentLines[index]

      const lines = currentLines
        .filter((line) => line.id !== lineId)
        .map((line) => ({ ...line }))

      // Pokud mažeme začátek sloky, jeho hranici
      // převezme další verš téže sloky.
      if (
        removedLine.stanzaStart &&
        index < lines.length &&
        !lines[index].stanzaStart
      ) {
        lines[index].stanzaStart = true
      }

      // První verš básně nikdy nezačíná
      // oddělením od předchozí sloky.
      lines[0].stanzaStart = false

      return {
        poem: {
          ...poem,
          lines,
          text: serializePoemLines(lines),
        },
        analysisResult: null,
        analysisStatus: 'idle',
        analysisError: null,
      }
    }),

  movePoemLine: (sourceId, targetId) =>
    set((state) => {
      const poem = state.poem
      if (!poem) return state

      const currentLines = poem.lines?.length
        ? poem.lines
        : parsePlaintextToLines(poem.text)

      const lines = movePoemLine(
        currentLines,
        sourceId,
        targetId,
      )

      // Neplatný přesun – nic se nezměnilo.
      if (lines === currentLines) {
        return state
      }

      return {
        poem: {
          ...poem,
          lines,
          text: serializePoemLines(lines),
        },
        analysisResult: null,
        analysisStatus: 'idle',
        analysisError: null,
      }
    }),

  generateDemoPoem: async () => {
    set({
      poem: null,
      status: 'loading',
      error: null,
      analysisStatus: 'idle',
      analysisError: null,
      analysisResult: null
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
      analysisResult: null
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
        authorName: sample.author,
        originalText: sample.poem.text,
        createdAt: new Date().toISOString(),
        source: 'local',
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