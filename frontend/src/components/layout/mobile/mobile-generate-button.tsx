'use client'

import { AppIcon } from '@/components/icons/app-icon'
import { useGeneratePoemAction } from '@/hooks/use-generate-poem-action'

export function MobileGenerateButton() {
  const { runGeneratePoemAction } = useGeneratePoemAction()

  return (
    <button
      type="button"
      aria-label="Generovat báseň"
      onClick={() => runGeneratePoemAction({ requireParams: true })}
      className="flex h-14 w-14 items-center justify-center rounded-full bg-teal-700 text-white transition-transform active:scale-95"
    >
      <AppIcon name="stars" size={44} />
    </button>
  )
}