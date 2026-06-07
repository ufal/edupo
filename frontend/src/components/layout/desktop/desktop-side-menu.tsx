'use client'

import Link from 'next/link'
import { EdupoLogo } from '@/components/brand/edupo-logo'
import { PartnerLogos } from '@/components/brand/partner-logos'
import { AppIcon, type IconName } from '@/components/icons/app-icon'
import { Button } from '@/components/ui/button'
import { useGeneratePoemAction } from '@/hooks/use-generate-poem-action'
import type { DesktopSidePanel } from './desktop-side-panel-types'

type DesktopMenuItem = {
  id: Exclude<DesktopSidePanel, null>
  icon: IconName
  label: string
}

const menuItems: DesktopMenuItem[] = [
  { id: 'title-motifs', icon: 'book', label: 'Název a motiv' },
  { id: 'form', icon: 'geometry', label: 'Forma' },
  { id: 'verse-count', icon: 'verseList', label: 'Počet veršů' },
  { id: 'first-verse-length', icon: 'ruler', label: 'Délka prvního verše' },
  { id: 'metrum', icon: 'metrum', label: 'Metrum' },
  { id: 'temperature', icon: 'thermometer', label: 'Temperature' },
]

function DesktopSideMenuItem({
  icon,
  label,
  active,
  onClick,
}: DesktopMenuItem & {
  active?: boolean
  onClick?: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex items-center gap-4 text-left typo-body font-medium cursor-pointer"
    >
      <span
        className={[
          'grid size-12 place-items-center rounded-2xl',
          active ? 'bg-subtle text-subtle-foreground' : 'bg-white/15',
        ].join(' ')}
      >
        <AppIcon name={icon} size={23} />
      </span>
      <span>{label}</span>
    </button>
  )
}

type DesktopSideMenuProps = {
  activePanel: DesktopSidePanel
  onPanelToggle: (panel: Exclude<DesktopSidePanel, null>) => void
}

export function DesktopSideMenu({
  activePanel,
  onPanelToggle,
}: DesktopSideMenuProps) {
  const { runGeneratePoemAction } = useGeneratePoemAction()

  return (
    <aside className="relative z-30 flex min-h-0 flex-col bg-primary px-[50px] py-[60px] text-primary-foreground">
      <div>
        <Link href={(process.env.NEXT_PUBLIC_LINK_BASE || '/') + 'dashboard'} className="mr-auto inline-flex">
          <EdupoLogo />
        </Link>
      </div>

      <nav className="mt-20 flex flex-col gap-5" aria-label="Nastavení básně">
        {
            menuItems.map((item) => (
                <DesktopSideMenuItem
                    key={item.id}
                    id={item.id}
                    icon={item.icon}
                    label={item.label}
                    active={activePanel === item.id}
                    onClick={() => onPanelToggle(item.id)}
                />
            ))
        }
      </nav>

      <Button
        variant="subtle"
        size="md"
        onClick={() => runGeneratePoemAction({ requireParams: true })}
        className="mt-16"
      >
        <AppIcon name="stars" size={28} className="text-subtle-foreground" />
        Generování
      </Button>

      <div className="mt-auto">
        <PartnerLogos set="reduced" variant="horizontal" className="justify-start" />
      </div>
    </aside>
  )
}