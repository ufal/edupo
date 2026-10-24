'use client'

import { useUiStore } from '@/stores/ui-store'
import { usePoemStore } from '@/stores/poem-store'
import { SettingsCard } from './settings-card'
import { DEFAULT_MAX_STROPHES } from '@/config/poem-param-max-strophes'
import { usePoemModels } from '@/hooks/use-poem-models'

const FORM_LABELS = {
  haiku: 'Haiku',
  limerik: 'Limerik',
  sonet: 'Sonet'
} as const

const METRUM_LABELS = {
  daktyl: 'Daktyl',
  jamb: 'Jamb',
  trochej: 'Trochej',
  volný: 'Volný verš',
} as const

export function SettingsOverview() {
  const { modelLabel } = usePoemModels()
  const openOverlay = useUiStore((state) => state.openOverlay)
  const params = usePoemStore((state) => state.params)

  const titleLabel = params.title ?? 'Nenastaveno'

  const motifsLabel = params.motifs && params.motifs.length > 0
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

  const maxStrophesLabel =
    typeof params.maxStrophes === 'number'
      ? `${params.maxStrophes}`
      : 'Nenastaveno'

  const modelSpecLabel = modelLabel

    const moodLabel =
      params.mood === 'veselá'
        ? 'Veselá'
        : params.mood === 'smutná'
          ? 'Smutná'
          : 'Nenastaveno'

  return (
    <div className="flex flex-col gap-6 px-5 py-5">
      <h1 className="text-center text-lg text-zinc-700">
        Nastavení básně
      </h1>

      <SettingsCard
        iconName="book"
        title="Název a motiv"
        value={
          <>
            Název: {titleLabel}
            <br />
            Motiv: {motifsLabel}
            <br />
            Nálada: {moodLabel}
          </>
        }
        onClick={() => openOverlay('setting-param-title-motifs')}
      />

      <div className="grid grid-cols-2 gap-4">
        <SettingsCard
          iconName="geometry"
          title="Pevná forma"
          value={formLabel}
          onClick={() => openOverlay('setting-param-form')}
        />

        <SettingsCard
          iconName="verseList"
          title="Počet veršů a slok"
          value={
            <>
              Počet veršů: {versesCountLabel}
              <br />
              Maximum slok: {maxStrophesLabel}
            </>
          }
          onClick={() => openOverlay('setting-param-verse-count')}
        />

        <SettingsCard
          iconName="verseGroups"
          title="Rýmové schéma"
          value={rhymeSchemeLabel}
          onClick={() => openOverlay('setting-param-rhyme-scheme')}
        />

        <SettingsCard
          iconName="ruler"
          title="Délka prvního verše"
          value={firstVerseLengthLabel}
          onClick={() => openOverlay('setting-param-first-verse-length')}
        />

        <SettingsCard
          iconName="metrum"
          title="Metrum"
          value={metrumLabel}
          onClick={() => openOverlay('setting-param-metrum')}
        />

        <SettingsCard
          iconName="thermometer"
          title="Temperature"
          value={
            <>
              Temperature: {temperatureLabel}
              <br />
              Model: {modelSpecLabel}
            </>
          }
          onClick={() => openOverlay('setting-param-temperature')}
        />
      </div>
    </div>
  )
}