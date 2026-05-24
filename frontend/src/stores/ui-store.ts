import { create } from 'zustand'

type OverlayType =
  | null
  | 'missing-params'
  | 'mobile-menu'
  | 'generation'
  | 'poetry-sample'
  | 'author-style'

  | 'setting-param-title-motifs'
  | 'setting-param-form'
  | 'setting-param-verse-count'
  | 'setting-param-rhyme-scheme'
  | 'setting-param-metrum'
  | 'setting-param-first-verse-length'
  | 'setting-param-temperature'

  | 'share'

type UiState = {
  overlay: OverlayType
  openOverlay: (overlay: Exclude<OverlayType, null>) => void
  closeOverlay: () => void
}

export const useUiStore = create<UiState>((set) => ({
  overlay: null,
  openOverlay: (overlay) => set({ overlay }),
  closeOverlay: () => set({ overlay: null }),
}))