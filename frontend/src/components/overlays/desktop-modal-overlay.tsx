'use client'

import { X } from 'lucide-react'
import { cn } from '@/libs/utils'

type DesktopModalOverlayProps = {
  children: React.ReactNode
  onClose: () => void
  className?: string
  contentClassName?: string
  closeClassName?: string
}

export function DesktopModalOverlay({
  children,
  onClose,
  className,
  contentClassName,
  closeClassName,
}: DesktopModalOverlayProps) {
  return (
    <div
      className={cn(
        'fixed inset-0 z-[80] hidden items-center justify-center bg-primary/80 desktop:flex',
        className,
      )}
    >
      <div className={cn('relative', contentClassName)}>
        <button
          type="button"
          aria-label="Zavřít"
          onClick={onClose}
          className={cn(
            'absolute right-0 top-0 z-10 flex h-8 w-8 translate-x-[42px] -translate-y-[42px] items-center justify-center text-white cursor-pointer',
            closeClassName,
          )}
        >
          <X size={26} strokeWidth={2.2} />
        </button>

        {children}
      </div>
    </div>
  )
}