'use client'

import { useState } from 'react'
import { X } from 'lucide-react'

import { AppIcon, IconName } from "@/components/icons/app-icon"
import { Button } from '@/components/ui/button'

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
                <AppIcon name="alertCircle" size={24} className="text-white" />
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

      {isInfoOpen && (
        <div className="fixed inset-0 z-100 flex items-center justify-center bg-purple-500/90 px-6">
          
          <button
            type="button"
            aria-label="Zavřít nápovědu"
            onClick={() => setIsInfoOpen(false)}
            className="absolute right-6 top-56 grid size-8 place-items-center text-white"
          >
            <X size={28} strokeWidth={2.2} />
          </button>

          <div className="flex flex-col gap-3 items-center w-full max-w-[320px] rounded-3xl bg-white px-8 py-7 text-center">
            
            <AppIcon name="alertCircle" size={36} className="text-grey-900" />

            <p className="typo-small text-grey-900">
              {infoText}
            </p>

            <Button
              type="button"
              variant="primary"
              size="md"
              className="mx-auto px-10"
              onClick={() => setIsInfoOpen(false)}
            >
              Zavřít
            </Button>
          </div>
        </div>
      )}
    </>
  )
}