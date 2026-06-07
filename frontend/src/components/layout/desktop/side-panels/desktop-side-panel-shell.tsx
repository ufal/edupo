'use client'

import { useState } from 'react'
import { InfoIcon, X } from 'lucide-react'
import { AppIcon } from '@/components/icons/app-icon'
import { InfoPopup } from '@/components/ui/info-popup'

type DesktopSidePanelShellProps = {
  title: string
  onClose: () => void
  children: React.ReactNode
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
    <section className="relative flex min-h-0 flex-col bg-purple-600 px-[50px] py-[60px] text-primary-foreground">
      <header className="flex items-start justify-between gap-4">
        <button
          type="button"
          aria-label="Informace"
          onClick={() => infoText && setIsInfoOpen(!isInfoOpen)}
          className="grid size-6 place-items-center cursor-pointer"
        >
          <InfoIcon size={22} className="text-white" />
        </button>

        <h2 className="typo-body font-medium uppercase tracking-wide">
          {title}
        </h2>

        <button
          type="button"
          aria-label="Zavřít"
          onClick={onClose}
          className="grid size-6 place-items-center cursor-pointer"
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