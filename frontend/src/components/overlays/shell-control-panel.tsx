'use client'

import { useState } from 'react'
import { InfoIcon, X } from 'lucide-react'

import { AppIcon, IconName } from "@/components/icons/app-icon"
import { InfoPopup } from '../ui/info-popup'

type ShellControlPanelProps = {
  iconName: IconName
  title: string
  onClose: () => void
  infoText?: string
}

export function ShellControlPanel({
  iconName,
  title,
  onClose,
  infoText
}: ShellControlPanelProps) {
  const [isInfoOpen, setIsInfoOpen] = useState(false)

  return (
    <>
      <header className="flex h-20 items-center justify-between bg-purple-700 px-5 text-white">
        <div className="flex items-center gap-4">
          <AppIcon name={iconName} className="h-8 w-8 text-white" />

          <h2 className="typo-h4 font-regular">
            {title}
          </h2>
        </div>

        <div className="flex items-center gap-7">
          {
            infoText &&
              <button
                type="button"
                aria-label="Informace"
                onClick={() => setIsInfoOpen(true)}
                className="grid size-8 place-items-center"
              >
                <InfoIcon size={24} className="text-white" />
              </button>
          }

          <button
            type="button"
            aria-label="Zavřít"
            onClick={onClose}
            className="grid size-8 place-items-center"
          >
            <X size={28} strokeWidth={2.2} />
          </button>
        </div>
      </header>

      {isInfoOpen && infoText && (
        <InfoPopup
          text={infoText}
          onClose={() => setIsInfoOpen(false)}
          mode="overlay"
        />
      )}
    </>
  )
}