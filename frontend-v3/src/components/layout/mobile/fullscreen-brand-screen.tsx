import { MobileHeader } from '@/components/layout/mobile/mobile-header'
import { cn } from '@/libs/utils'

type FullscreenBrandScreenProps = {
  children: React.ReactNode
  className?: string
}

export function FullscreenBrandScreen({
  children,
  className,
}: FullscreenBrandScreenProps) {
  return (
    <div
      className={cn(
        'fixed inset-0 flex flex-col',
        className,
      )}
    >
      <MobileHeader mode="logo-only" />

      <main className="flex min-h-0 grow flex-col px-5 pb-24 pt-12 text-center bg-primary text-primary-foreground">
        {children}
      </main>
    </div>
  )
}