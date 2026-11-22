
'use client'

import type { ReactNode } from 'react'
import { AppIcon, type IconName } from '@/components/icons/app-icon'
import { usePoemStore } from '@/stores/poem-store'
import {
  formatAnalysisMetre,
  formatPercentage,
  getAnalysisRhymeScheme,
  getAnalysisVerseCounts,
  getAnalysisVerseLengths,
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
  const semanticAnalysis = usePoemStore(
    (state) => state.semanticAnalysis,
  )

  const analysisResult = usePoemStore(
    (state) => state.analysisResult,
  )

  const analysisStatus = usePoemStore(
    (state) => state.analysisStatus,
  )

  const analysisError = usePoemStore(
    (state) => state.analysisError,
  )

  const analysis =
    analysisStatus === 'success'
      ? analysisResult
      : null

  const measures = analysis?.measures

  const unavailable =
    analysisStatus === 'loading' ? 'Načítá se…' : '—'

  const motives = semanticAnalysis?.motives ?? []
  const mood = semanticAnalysis?.mood

  const motivesUnavailable =
    semanticAnalysis?.motivesStatus === 'loading'
      ? 'Načítá se…'
      : semanticAnalysis?.motivesStatus === 'error'
        ? 'Nepodařilo se načíst motivy.'
        : '—'

  const moodUnavailable =
    semanticAnalysis?.moodStatus === 'loading'
      ? 'Načítá se…'
      : semanticAnalysis?.moodStatus === 'error'
        ? 'Nepodařilo se určit náladu.'
        : '—'

  const settingsItems: SettingsItem[] = [
    {
      icon: 'bookAngle',
      label: 'Motivy',
      value: motives.length ? (
        <div className="flex flex-col">
          {motives.map((motive, index) => (
            <div key={`${motive}-${index}`}>
              {motive}
            </div>
          ))}
        </div>
      ) : motivesUnavailable,
    },
    {
      icon: 'face',
      label: 'Nálada',
      value: mood || moodUnavailable,
    },
    {
      icon: 'verseList',
      label: 'Počet veršů ve slokách',
      value: analysis
        ? getAnalysisVerseCounts(analysis)
        : unavailable,
    },
    {
      icon: 'ruler',
      label: 'Délky veršů',
      value: analysis ? (
        <div className="flex flex-col">
          {getAnalysisVerseLengths(analysis).map(
            (stanza, index) => (
              <div key={index}>
                {stanza || '—'}
              </div>
            ),
          )}
        </div>
      ) : unavailable,
    },
    {
      icon: 'verseGroups',
      label: 'Rýmování',
      value: measures ? (
        <div>
          <div>
            {getAnalysisRhymeScheme(analysis!)}
          </div>
          <div>
            {formatPercentage(measures.rhyming)} veršů se rýmuje
          </div>
          <div>
            {formatPercentage(measures.rhyming_consistency)} slok má shodné schéma
          </div>
        </div>
      ) : unavailable,
    },
    {
      icon: 'metrum',
      label: 'Metrum',
      value: measures ? (
        <div>
          <div>
            {formatAnalysisMetre(measures.poem_metre)}
          </div>
          <div>
            {formatPercentage(measures.metre_consistency)} konzistence metra
          </div>
        </div>
      ) : unavailable,
    },
    {
      icon: 'docSearch',
      label: 'Neznámá slova',
      value: measures
        ? `${formatPercentage(measures.unknown_words)} slov nejsou ve slovníku`
        : unavailable,
    },
  ]

  return (
    <aside className="h-full min-h-0 overflow-y-auto rounded-3xl bg-white px-8 py-6">
      <h2 className="typo-large font-bold text-grey-700">
        Automatická analýza
      </h2>

      {analysisStatus === 'loading' && (
        <p
          role="status"
          className="mt-3 typo-small text-zinc-500"
        >
          Probíhá automatická analýza básně…
        </p>
      )}

      {analysisStatus === 'error' && (
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
