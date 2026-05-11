'use client'

import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'

type GeneratePoemActionOptions = {
  requireParams?: boolean
}

export function useGeneratePoemAction() {
  const router = useRouter()

  const params = usePoemStore((state) => state.params)
  const generatePoem = usePoemStore((state) => state.generatePoem)

  const openOverlay = useUiStore((state) => state.openOverlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  const hasParams = Object.keys(params).length > 0

  async function runGeneratePoemAction({
    requireParams = true,
  }: GeneratePoemActionOptions = {}) {
    if (requireParams && !hasParams) {
      openOverlay('missing-params')
      return
    }

    openOverlay('generation')

    try {
      const poem = await generatePoem()

      if (!poem) {
        toast.error('Nepodařilo se vygenerovat báseň. Zkuste to prosím znovu.')
        closeOverlay()
        return
      }

      router.push(`/dashboard?poemId=${encodeURIComponent(poem.id)}`)
      closeOverlay()
    } catch (error) {
      console.error(error)
      toast.error('Nepodařilo se vygenerovat báseň. Zkuste to prosím znovu.')
      closeOverlay()
    }
  }

  return {
    hasParams,
    runGeneratePoemAction,
  }
}