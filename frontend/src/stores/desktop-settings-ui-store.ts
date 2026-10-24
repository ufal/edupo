import { create } from 'zustand'
import type { PoemGenerationParams } from '@/types/poem'

export type DesktopSettingId =
  | 'author-style'
  | 'title-motifs'
  | 'form'
  | 'verse-count'
  | 'first-verse-length'
  | 'rhyme-scheme'
  | 'metrum'
  | 'temperature'

export type DesktopUnsetParam =
  | Exclude<keyof PoemGenerationParams, 'firstWords'>
  | 'collectionId'

type SettingsVisibility = Record<DesktopSettingId, boolean>
type UnsetParams = Record<DesktopUnsetParam, boolean>

function createDefaultVisibility(): SettingsVisibility {
  return {
    'author-style': true,
    'title-motifs': true,
    form: true,
    'verse-count': true,
    'first-verse-length': true,
    'rhyme-scheme': true,
    metrum: true,
    temperature: true,
  }
}

function createDefaultUnset(): UnsetParams {
  return {
    title: true,
    motifs: true,
    mood: true,
    form: true,
    verseCount: true,
    maxStrophes: true,
    firstVerseLength: true,
    rhymeScheme: true,
    metrum: true,
    temperature: true,
    modelSpec: false,
    authorStyleId: true,
    collectionId: true
  }
}

type DesktopSettingsUiState = {
  visibility: SettingsVisibility
  unset: UnsetParams
  selectedCollectionId: string | null
  toggleVisibility: (id: DesktopSettingId) => void
  setUnset: (param: DesktopUnsetParam, unset: boolean) => void
  resetVisibility: () => void
  resetUnset: () => void
  setSelectedCollectionId: (id: string | null) => void
}

export const useDesktopSettingsUiStore =
  create<DesktopSettingsUiState>((set) => ({
    visibility: createDefaultVisibility(),
    unset: createDefaultUnset(),
    selectedCollectionId: null,

    setSelectedCollectionId: (id) =>
      set({ selectedCollectionId: id }),

    toggleVisibility: (id) =>
      set((state) => ({
        visibility: {
          ...state.visibility,
          [id]: !state.visibility[id],
        },
      })),

    setUnset: (param, unset) =>
      set((state) => ({
        unset: {
          ...state.unset,
          [param]: unset,
        },
      })),

    resetVisibility: () =>
      set({ visibility: createDefaultVisibility() }),

    resetUnset: () =>
      set({ unset: createDefaultUnset() }),
  }))