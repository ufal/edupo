
'use client'

import { usePoemStore } from '@/stores/poem-store'
import { DesktopSettingsPanel } from '@/components/layout/desktop/desktop-settings-panel'
import { DashboardHero } from './dashboard-hero'
import { DashboardTabs } from './dashboard-tabs'
import { DashboardCard } from './dashboard-card'

export function DashboardScreen() {
  const mode = usePoemStore((state) => state.mode)
  const setMode = usePoemStore((state) => state.setMode)

  const showAnalysisPanel = mode === 'analysis'

  return (
    <div className="flex grow flex-col px-5 py-5 desktop:mx-auto desktop:h-full desktop:min-h-0 desktop:w-full desktop:overflow-hidden desktop:px-0 desktop:py-0">

      <div className="desktop:hidden">
        <DashboardHero />
      </div>

      <div
        className={[
          'flex min-w-0 grow flex-col gap-4',
          'desktop:h-full desktop:min-h-0',
          showAnalysisPanel
            ? 'desktop:grid desktop:grid-cols-[minmax(0,1fr)_300px] desktop:items-stretch desktop:gap-6'
            : '',
        ].join(' ')}
      >
        {/* Hlavní pracovní oblast */}
        <div className="flex min-h-0 min-w-0 flex-col gap-4">
          <div className="shrink-0">
            <DashboardTabs value={mode} onChange={setMode} />
          </div>

          <DashboardCard mode={mode} />
        </div>

        {/* Pravý panel pouze v Analýze */}
        {showAnalysisPanel && (
          <div className="hidden h-full min-h-0 min-w-0 overflow-hidden desktop:block">
            <DesktopSettingsPanel />
          </div>
        )}
      </div>
    </div>
  )
}
