import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

type ShellOverlayVariant = 'popup' | 'menu'

type ShellOverlayProps = {
  children: React.ReactNode
  onClose?: () => void
  variant?: ShellOverlayVariant
  className?: string
  panelClassName?: string
}

export function ShellOverlay({
  children,
  onClose,
  variant = 'popup',
  className,
  panelClassName,
}: ShellOverlayProps) {
  if (variant === 'menu') {
    return (
      <div className={cn('absolute inset-0 z-40 bg-purple-700', className)}>
        {children}
      </div>
    )
  }

  return (
    <div
      className={cn(
        'absolute inset-0 z-40 bg-primary px-5 pt-28',
        className,
      )}
    >
      {onClose && (
        <button
          type="button"
          aria-label="Zavřít"
          onClick={onClose}
          className="absolute right-8 top-10 flex h-8 w-8 items-center justify-center text-white"
        >
          <X size={26} strokeWidth={2.2} />
        </button>
      )}

      <div
        className={cn(
          'mx-auto rounded-3xl bg-white px-6 py-11 text-center text-foreground',
          panelClassName,
        )}
      >
        {children}
      </div>
    </div>
  )
}