'use client'

import { usePathname } from 'next/navigation'
import { BottomNavItem } from '@/components/ui/bottom-nav-item'
import { MobileGenerateButton } from '@/components/layout/mobile/mobile-generate-button'

export function MobileBottomNav() {
  const pathname = usePathname()

  return (
    <nav
      aria-label="Hlavní mobilní navigace"
      className="border-t border-yellow-300 bg-white px-8 py-3"
    >
      <div className="flex items-center justify-evenly">
        <BottomNavItem
          icon="home"
          label="Dashboard"
          href="/dashboard"
          active={pathname === '/dashboard'}
        />
        <MobileGenerateButton />
        <BottomNavItem
          icon="settings"
          label="Nastavení"
          href="/settings"
          active={pathname === '/settings'}
        />
      </div>
    </nav>
  )
}