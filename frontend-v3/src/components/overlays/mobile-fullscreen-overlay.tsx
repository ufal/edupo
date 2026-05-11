import { cn } from '@/lib/utils'

type MobileFullscreenOverlayProps = {
  children: React.ReactNode
  className?: string
}

export function MobileFullscreenOverlay({
  children,
  className,
}: MobileFullscreenOverlayProps) {
  return (
    <div
      className={cn(
        'fixed inset-0 z-50 bg-primary text-primary-foreground',
        className,
      )}
    >
      {children}
    </div>
  )
}