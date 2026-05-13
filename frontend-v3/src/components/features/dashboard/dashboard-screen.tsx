'use client'

import { usePoemStore } from '@/stores/poem-store'
import { DashboardHero } from './dashboard-hero'
import { DashboardTabs } from './dashboard-tabs'
import { DashboardCard } from './dashboard-card'

export function DashboardScreen() {
  const mode = usePoemStore((state) => state.mode)
  const setMode = usePoemStore((state) => state.setMode)

  return (
    <div className="flex flex-col grow space-y-4 px-5 py-5">
      <DashboardHero />
      <DashboardTabs
        value={mode}
        onChange={setMode}
      />
      <DashboardCard
        mode={mode}
      />
    </div>
  )
}