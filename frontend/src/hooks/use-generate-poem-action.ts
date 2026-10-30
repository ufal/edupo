'use client'

import { useSyncExternalStore } from 'react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import { buildGenerationParams } from '@/services/poem-generation-params'

const DESKTOP_QUERY = '(min-width: 1024px)'

function subscribeDesktopChange(onChange: () => void) {
  const mediaQuery = window.matchMedia(DESKTOP_QUERY)

  mediaQuery.addEventListener('change', onChange)

  return () => {
    mediaQuery.removeEventListener('change', onChange)
  }
}

function getDesktopSnapshot() {
  return window.matchMedia(DESKTOP_QUERY).matches
}

function getServerSnapshot() {
  return false
}

type GeneratePoemActionOptions = {
  requireParams?: boolean
}

export function useGeneratePoemAction() {
  const router = useRouter()

  const isDesktop = useSyncExternalStore(
    subscribeDesktopChange,
    getDesktopSnapshot,
    getServerSnapshot,
  )

  const params = usePoemStore((state) => state.params)
  const generatePoem = usePoemStore((state) => state.generatePoem)

  const unset = useDesktopSettingsUiStore(
    (state) => state.unset,
  )

  const openOverlay = useUiStore((state) => state.openOverlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  const selectedCollectionId = useDesktopSettingsUiStore(
    (state) => state.selectedCollectionId,
  )

  const activeParams = buildGenerationParams(
    params,
    isDesktop ? unset : undefined,
    isDesktop ? selectedCollectionId : undefined,
  )

  const hasParams = Object.values(activeParams).some(
    (value) =>
      value !== undefined &&
      value !== null &&
      value !== '' &&
      (!Array.isArray(value) || value.length > 0),
  )

  async function runGeneratePoemAction({
    requireParams = true,
  }: GeneratePoemActionOptions = {}) {
    if (requireParams && !hasParams) {
      openOverlay('missing-params')
      return
    }

    openOverlay('generation')

    try {
      const poem = await generatePoem({
        respectDesktopUnset: isDesktop,
      })

      const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

      router.push(
        `${base}dashboard?poemId=${encodeURIComponent(poem.id)}`,
      )

      closeOverlay()
    } catch (error) {
      console.error(error)

      toast.error(
        'Nepodařilo se vygenerovat báseň. Zkuste to prosím znovu.',
      )

      closeOverlay()
    }
  }

  return {
    hasParams,
    runGeneratePoemAction,
  }
}