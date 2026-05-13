import type { ReactNode } from 'react'
import { MobileShell } from '@/components/layout/mobile-shell'
import { DesktopShell } from '@/components/layout/desktop-shell'

type ResponsiveLayoutProps = {
  children: ReactNode
}

export default function FullLayout({ children }: ResponsiveLayoutProps) {
  return (
    <>
      <div className="block desktop:hidden">
        <MobileShell type="with-bottom-nav">{children}</MobileShell>
      </div>

      <div className="hidden desktop:block">
        <DesktopShell>{children}</DesktopShell>
      </div>
    </>
  )
}