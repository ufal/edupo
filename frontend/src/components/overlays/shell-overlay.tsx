import { X } from 'lucide-react'
import { cn } from '@/libs/utils'

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
        'desktop:bg-yellow-50 desktop:px-0 desktop:pt-0',
        className,
      )}
    >
      <div
        className={cn(
          'relative mx-auto',
          'desktop:absolute desktop:left-1/2 desktop:top-[290px] desktop:-translate-x-1/2',
        )}
      >
        {onClose && (
          <button
            type="button"
            aria-label="Zavřít"
            onClick={onClose}
            className="
              absolute z-10
              right-0 top-0
              translate-x-[42px] -translate-y-[42px]
              flex h-8 w-8 items-center justify-center
              text-white desktop:text-foreground
              cursor-pointer
            "
          >
            <X size={26} strokeWidth={2.2} />
          </button>
        )}

        <div
          className={cn(
            'rounded-3xl bg-white px-6 py-11 text-center text-foreground',
            panelClassName,
          )}
        >
          {children}
        </div>
      </div>
    </div>
  )
}