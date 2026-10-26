
'use client'

import { useState, type ReactNode } from 'react'
import { DesktopSideMenu } from '@/components/layout/desktop/desktop-side-menu'
import { DesktopHeader } from '@/components/layout/desktop/desktop-header'
import { PartnerLogos } from '@/components/brand/partner-logos'
import { OverlayRenderer } from '@/components/overlays/overlay-renderer'
import { DesktopTitleMotifsPanel } from '@/components/layout/desktop/side-panels/desktop-title-motifs-panel'
import type { DesktopSidePanel } from '@/components/layout/desktop/desktop-side-panel-types'
import { DesktopFormPanel } from './desktop/side-panels/desktop-form-panel'
import { DesktopMetrePanel } from './desktop/side-panels/desktop-metre-panel'
import { DesktopTemperaturePanel } from './desktop/side-panels/desktop-temperature-panel'
import { DesktopVerseCountPanel } from './desktop/side-panels/desktop-verse-count-panel'
import { DesktopFirstVerseLengthPanel } from './desktop/side-panels/desktop-first-verse-length-panel'
import { DesktopRhymeSchemePanel } from './desktop/side-panels/desktop-rhyme-panel-scheme'
import { DesktopAuthorStylePanel } from './desktop/side-panels/desktop-author-style-panel'

type DesktopShellProps = {
  children: ReactNode
}

export function DesktopShell({ children }: DesktopShellProps) {
  const [activePanel, setActivePanel] = useState<DesktopSidePanel>(null)

  const togglePanel = (panel: Exclude<DesktopSidePanel, null>) => {
    setActivePanel((current) => (current === panel ? null : panel))
  }

  return (
    <div
      className={[
        'fixed inset-0 grid bg-yellow-50 text-foreground',
        activePanel
          ? 'grid-cols-[410px_410px_minmax(0,1fr)]'
          : 'grid-cols-[410px_minmax(0,1fr)]',
      ].join(' ')}
    >
      <DesktopSideMenu
        activePanel={activePanel}
        onPanelToggle={togglePanel}
      />

      {activePanel === 'author-style' && (
        <DesktopAuthorStylePanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'title-motifs' && (
        <DesktopTitleMotifsPanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'form' && (
        <DesktopFormPanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'metrum' && (
        <DesktopMetrePanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'temperature' && (
        <DesktopTemperaturePanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'verse-count' && (
        <DesktopVerseCountPanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'rhyme-scheme' && (
        <DesktopRhymeSchemePanel
          onClose={() => setActivePanel(null)}
        />
      )}

      {activePanel === 'first-verse-length' && (
        <DesktopFirstVerseLengthPanel
          onClose={() => setActivePanel(null)}
        />
      )}

      <div className="relative flex min-w-0 min-h-0 flex-col overflow-hidden">

        {/* Horní navigace */}
        <DesktopHeader />

        {/* Hlavní pracovní oblast */}
        <div className="relative min-h-0 flex-1 px-10">
          <main className="relative h-full min-h-0 overflow-y-auto">
            {children}
            <OverlayRenderer />
          </main>
        </div>

        {/* Spodní loga institucí */}
        <footer className="flex h-[88px] shrink-0 items-center justify-end px-10">
          <PartnerLogos
            variant="horizontal"
            set="reduced"
            color="gray"
          />
        </footer>

      </div>
    </div>
  )
}
