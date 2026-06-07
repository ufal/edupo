'use client'

import { useState, type ReactNode } from 'react'
import { DesktopSideMenu } from '@/components/layout/desktop/desktop-side-menu'
import { DesktopSettingsPanel } from '@/components/layout/desktop/desktop-settings-panel'
import { DesktopFooter } from '@/components/layout/desktop/desktop-footer'
import { OverlayRenderer } from '@/components/overlays/overlay-renderer'
import { DesktopTitleMotifsPanel } from '@/components/layout/desktop/side-panels/desktop-title-motifs-panel'
import type { DesktopSidePanel } from '@/components/layout/desktop/desktop-side-panel-types'
import { DesktopFormPanel } from './desktop/side-panels/desktop-form-panel'
import { DesktopMetrePanel } from './desktop/side-panels/desktop-metre-panel'
import { DesktopTemperaturePanel } from './desktop/side-panels/desktop-temperature-panel'
import { DesktopVerseCountPanel } from './desktop/side-panels/desktop-verse-count-panel'
import { DesktopFirstVerseLengthPanel } from './desktop/side-panels/desktop-first-verse-length-panel'

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
          ? 'grid-cols-[320px_320px_minmax(0,1fr)]'
          : 'grid-cols-[320px_minmax(0,1fr)]',
      ].join(' ')}
    >
      <DesktopSideMenu activePanel={activePanel} onPanelToggle={togglePanel} />

      {activePanel === 'title-motifs' && (
        <DesktopTitleMotifsPanel onClose={() => setActivePanel(null)} />
      )}

      {activePanel === 'form' && (
        <DesktopFormPanel onClose={() => setActivePanel(null)} />
      )}

      {activePanel === 'metrum' && (
        <DesktopMetrePanel onClose={() => setActivePanel(null)} />
      )}

      {activePanel === 'temperature' && (
        <DesktopTemperaturePanel onClose={() => setActivePanel(null)} />
      )}

      {activePanel === 'verse-count' && (
        <DesktopVerseCountPanel onClose={() => setActivePanel(null)} />
      )}

      {activePanel === 'first-verse-length' && (
        <DesktopFirstVerseLengthPanel onClose={() => setActivePanel(null)} />
      )}

      <div className="relative grid min-w-0 grid-rows-[1fr_auto] overflow-hidden">
        <div className="grid min-h-0 grid-cols-[minmax(0,1fr)_290px] gap-12 px-[50px] pt-[60px]">
          <main className="relative min-h-0 overflow-y-auto">
            {children}
            <OverlayRenderer />
          </main>

          <DesktopSettingsPanel />
        </div>

        <DesktopFooter />
      </div>
    </div>
  )
}