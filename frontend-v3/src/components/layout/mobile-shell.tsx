import { MobileHeader } from './mobile/mobile-header'
import { MobileBottomNav } from './mobile/mobile-bottom-nav'
import { OverlayRenderer } from '@/components/overlays/overlay-renderer'

type MobileShellProps = {
  type?: 'with-bottom-nav' | 'fullscreen'
  children: React.ReactNode
}

export function MobileShell({ type = 'with-bottom-nav', children }: MobileShellProps) {
  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden bg-yellow-50">
      <MobileHeader />

      <div className="relative min-h-0 flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto">
          <main className="flex flex-col min-h-full">
            {children}
          </main>
        </div>

        <OverlayRenderer />
      </div>

      {type === 'with-bottom-nav' && <MobileBottomNav />}
    </div>
  )
}