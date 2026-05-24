'use client'

import Link from 'next/link'
import { ShellOverlay } from './shell-overlay'
import { Button } from '@/components/ui/button'
import { useUiStore } from '@/stores/ui-store'
import { useGeneratePoemAction } from '@/hooks/use-generate-poem-action'

type MissingParamsOverlayProps = {
  onClose: () => void
}

export function MissingParamsOverlay({ onClose }: MissingParamsOverlayProps) {
  const openOverlay = useUiStore((state) => state.openOverlay)
  const { runGeneratePoemAction } = useGeneratePoemAction()

  return (
    <ShellOverlay onClose={onClose} panelClassName="mt-5">
      <div className="space-y-7">
        <div className="space-y-6">
          <h2 className="typo-large">Jak vytvořit báseň?</h2>

          <p className="mx-auto max-w-[270px] text-sm leading-5 text-grey-600">
            Pro vytvoření básně je potřeba zvolit styl autora a nastavení.
          </p>
        </div>

        <div className="flex flex-col items-center gap-5">
          <Button
            type="button"
            variant="primary"
            size="sm"
            className="min-w-[190px]"
            onClick={() => openOverlay('author-style')}
          >
            Změnit styl podle autora
          </Button>

          <Button
            asChild
            variant="primary"
            size="sm"
            className="min-w-[190px]"
          >
            <Link href="/settings" onClick={onClose}>
              Nastavení parametrů
            </Link>
          </Button>

          <Button
            type="button"
            variant="primary"
            size="sm"
            className="min-w-[190px]"
            onClick={() => runGeneratePoemAction({ requireParams: false })}
          >
            Vygenerovat náhodně
          </Button>
        </div>
      </div>
    </ShellOverlay>
  )
}