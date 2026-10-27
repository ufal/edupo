
'use client'

import type { ReactNode } from 'react'
import { AppIcon, type IconName } from '@/components/icons/app-icon'
import { usePoemStore } from '@/stores/poem-store'

import {
  getAnalysisAuthor,
  getAnalysisCollection,
  getAnalysisStanzaCount,
  getAnalysisMetre,
  getAnalysisRhymeScheme,
  getAnalysisModel,
} from '@/utils/poem-analysis'

type SettingsItem = {
  icon: IconName
  label: string
  value: ReactNode
}

function DesktopSettingsItem({
  icon,
  label,
  value,
}: SettingsItem) {
  return (
    <div className="grid grid-cols-[32px_1fr] gap-2">
      <AppIcon
        name={icon}
        size={22}
        className="mt-1 text-purple-500"
      />

      <div className="min-w-0">
        <div className="typo-body font-bold text-grey-700">
          {label}
        </div>

        <div className="mt-2 break-words typo-small text-zinc-700">
          {value}
        </div>
      </div>
    </div>
  )
}

export function DesktopSettingsPanel() {
  const poem = usePoemStore((state) => state.poem)

  const analysisResult = usePoemStore(
    (state) => state.analysisResult,
  )

  const analysisStatus = usePoemStore(
    (state) => state.analysisStatus,
  )

  const analysisError = usePoemStore(
    (state) => state.analysisError,
  )

  const isLoading = analysisStatus === 'loading'
  const isError = analysisStatus === 'error'

  const analysis =
    analysisStatus === 'success' &&
    analysisResult?.id === poem?.id
      ? analysisResult
      : null

  const unavailable = isLoading ? 'Načítá se…' : '—'

  const showValue = (
    value: string | number | null | undefined,
  ): string => {
    if (!analysis) return unavailable

    if (value === null || value === undefined) {
      return '—'
    }

    return String(value).trim() || '—'
  }

  const author = analysis
    ? getAnalysisAuthor(analysis)
    : null

  const collection = analysis
    ? getAnalysisCollection(analysis)
    : null

  const title = analysis?.title

  const verseCount = analysis?.verses?.length

  const stanzaCount = analysis
    ? getAnalysisStanzaCount(analysis)
    : null

  const rhymeScheme = analysis
    ? getAnalysisRhymeScheme(analysis)
    : null

  const metrum = analysis
    ? getAnalysisMetre(analysis)
    : null

  const model = analysis
    ? getAnalysisModel(analysis)
    : null

  const settingsItems: SettingsItem[] = [
    {
      icon: 'feather',
      label: 'Autorský styl',
      value: (
        <>
          Autor: {showValue(author)}
          <br />
          Sbírka: {showValue(collection)}
        </>
      ),
    },
    {
      icon: 'book',
      label: 'Název a motiv',
      value: (
        <>
          Název: {showValue(title)}
          <br />
          Motiv: {unavailable}
          <br />
          Nálada: {unavailable}
        </>
      ),
    },
    {
      icon: 'geometry',
      label: 'Forma',
      value: analysis
        ? showValue(analysis.form)
        : unavailable,
    },
    {
      icon: 'verseList',
      label: 'Počet veršů a slok',
      value: (
        <>
          Počet veršů: {showValue(verseCount)}
          <br />
          Počet slok: {showValue(stanzaCount)}
        </>
      ),
    },
    {
      icon: 'verseGroups',
      label: 'Rýmové schéma',
      value: showValue(rhymeScheme),
    },
    {
      icon: 'ruler',
      label: 'Délka prvního verše',
      value: unavailable,
    },
    {
      icon: 'metrum',
      label: 'Metrum',
      value: showValue(metrum),
    },
    {
      icon: 'thermometer',
      label: 'AI model',
      value: showValue(model),
    },
  ]

  return (
    <aside className="h-full min-h-0 overflow-hidden rounded-3xl bg-white px-8 py-6">
      <h2 className="typo-large font-bold text-grey-700">
        Automatická analýza
      </h2>

      {isLoading && (
        <p
          role="status"
          className="mt-3 typo-small text-zinc-500"
        >
          Probíhá automatická analýza básně…
        </p>
      )}

      {isError && (
        <p
          role="alert"
          className="mt-3 typo-small text-red-600"
        >
          {analysisError ??
            'Výsledky analýzy nejsou dostupné.'}
        </p>
      )}

      <div className="mt-6 flex flex-col gap-4">
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
