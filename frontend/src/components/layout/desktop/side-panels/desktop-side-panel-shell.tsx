'use client'

import { useState, type ReactNode } from 'react'
import { InfoIcon, X } from 'lucide-react'
import { InfoPopup } from '@/components/ui/info-popup'

type DesktopSidePanelShellProps = {
  title: string
  onClose: () => void
  children: ReactNode
  infoText?: string
}

export function DesktopSidePanelShell({
  title,
  onClose,
  children,
  infoText,
}: DesktopSidePanelShellProps) {
  const [isInfoOpen, setIsInfoOpen] = useState(false)

  return (
    <section
      className={[
        'relative flex min-h-0 flex-col overflow-y-auto',
        'bg-purple-600 px-[50px] py-[60px]',
        'text-primary-foreground',
      ].join(' ')}
    >
      <header className="flex shrink-0 items-start justify-between gap-4">
        <button
          type="button"
          aria-label="Informace"
          aria-expanded={isInfoOpen}
          disabled={!infoText}
          onClick={() => setIsInfoOpen((open) => !open)}
          className={[
            'grid size-6 shrink-0 place-items-center rounded',
            'cursor-pointer focus-visible:outline-none',
            'focus-visible:ring-2 focus-visible:ring-white',
            'disabled:invisible',
          ].join(' ')}
        >
          <InfoIcon size={22} />
        </button>

        <h2 className="typo-body font-bold">
          {title}
        </h2>

        <button
          type="button"
          aria-label="Zavřít"
          onClick={onClose}
          className={[
            'grid size-6 shrink-0 place-items-center rounded',
            'cursor-pointer focus-visible:outline-none',
            'focus-visible:ring-2 focus-visible:ring-white',
          ].join(' ')}
        >
          <X size={24} />
        </button>
      </header>

      {isInfoOpen && infoText && (
        <div className="mt-20">
          <InfoPopup
            text={infoText}
            onClose={() => setIsInfoOpen(false)}
            mode="inline"
          />
        </div>
      )}

      <div className="mt-20">
        {children}
      </div>
    </section>
  )
}