
'use client'

import { usePoemStore } from '@/stores/poem-store'
import { DashboardHero } from './dashboard-hero'
import { DashboardTabs } from './dashboard-tabs'
import { DashboardCard } from './dashboard-card'

export function DashboardScreen() {
  const mode = usePoemStore((state) => state.mode)
  const setMode = usePoemStore((state) => state.setMode)

  return (
    <div className="flex grow flex-col space-y-4 px-5 py-5 desktop:mx-auto desktop:w-full desktop:px-0 desktop:py-0">
      <div className="desktop:hidden">
        <DashboardHero />
      </div>

      <DashboardTabs value={mode} onChange={setMode} />
      <DashboardCard mode={mode} />
    </div>
  )
}
