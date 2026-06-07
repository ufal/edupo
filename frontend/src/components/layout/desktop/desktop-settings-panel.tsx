'use client'

import type { ReactNode } from 'react'
import { AppIcon, type IconName } from '@/components/icons/app-icon'
import { usePoemStore } from '@/stores/poem-store'

const FORM_LABELS = {
  free: 'Volná forma',
  sonet: 'Sonet',
  limerik: 'Limerik',
  haiku: 'Haiku',
  epigram: 'Epigram',
} as const

const METRUM_LABELS = {
  trochej: 'Trochej',
  jamb: 'Jamb',
  daktyl: 'Daktyl',
  volný: 'Volný',
} as const

type SettingsItem = {
  icon: IconName
  label: string
  value: ReactNode
}

function DesktopSettingsItem({ icon, label, value }: SettingsItem) {
  return (
    <div className="grid grid-cols-[32px_1fr] gap-4">
      <AppIcon name={icon} size={22} className="mt-1 text-purple-500" />

      <div>
        <div className="typo-body font-medium text-foreground">
          {label}
        </div>

        <div className="mt-2 typo-small text-zinc-700">
          {value}
        </div>
      </div>
    </div>
  )
}

export function DesktopSettingsPanel() {
  const params = usePoemStore((state) => state.params)

  const titleLabel = params.title ?? 'Nenastaveno'

  const motifsLabel =
    params.motifs && params.motifs.length > 0
      ? params.motifs.join(', ')
      : 'Nenastaveno'

  const formLabel = params.form
    ? FORM_LABELS[params.form as keyof typeof FORM_LABELS]
    : 'Nenastaveno'

  const versesCountLabel = params.verseCount
    ? `${params.verseCount}`
    : 'Nenastaveno'

  const rhymeSchemeLabel = params.rhymeScheme ?? 'Nenastaveno'

  const firstVerseLengthLabel = params.firstVerseLength
    ? `${params.firstVerseLength}`
    : 'Nenastaveno'

  const metrumLabel = params.metrum
    ? METRUM_LABELS[params.metrum as keyof typeof METRUM_LABELS]
    : 'Nenastaveno'

  const temperatureLabel =
    typeof params.temperature === 'number'
      ? params.temperature.toFixed(1)
      : 'Nenastaveno'

  const settingsItems: SettingsItem[] = [
    {
      icon: 'book',
      label: 'Název a motiv',
      value: (
        <>
          Název: {titleLabel}
          <br />
          Motiv: {motifsLabel}
        </>
      ),
    },
    { icon: 'geometry', label: 'Forma', value: formLabel },
    { icon: 'verseList', label: 'Počet veršů', value: versesCountLabel },
    { icon: 'verseGroups', label: 'Rýmové schéma', value: rhymeSchemeLabel },
    { icon: 'ruler', label: 'Délka prvního verše', value: firstVerseLengthLabel },
    { icon: 'metrum', label: 'Metrum', value: metrumLabel },
    { icon: 'thermometer', label: 'Temperature', value: temperatureLabel },
  ]

  return (
    <aside className="mb-5 rounded-3xl bg-white px-9 py-7">
      <h2 className="typo-large text-foreground">
        Použité nastavení
      </h2>

      <div className="mt-12 flex flex-col gap-9">
        {settingsItems.map((item) => (
          <DesktopSettingsItem
            key={item.label}
            icon={item.icon}
            label={item.label}
            value={item.value}
          />
        ))}
      </div>
    </aside>
  )
}