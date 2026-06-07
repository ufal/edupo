'use client'

import { usePoemStore } from '@/stores/poem-store'
import type { PoemLineGroup } from '@/types/poem'
import { getPoemLines, PoemCardActions, PoemEmptyState } from './poem-view-utils'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'

const groupClasses: Record<PoemLineGroup, { badge: string; line: string }> = {
  A: {
    badge: 'bg-purple-100 text-purple-700',
    line: 'bg-purple-100 text-grey-700',
  },
  B: {
    badge: 'bg-cyan-200 text-cyan-800',
    line: 'bg-cyan-200 text-grey-700',
  },
  C: {
    badge: 'bg-teal-100 text-teal-800',
    line: 'bg-teal-100 text-grey-700',
  },
  D: {
    badge: 'bg-orange-100 text-orange-800',
    line: 'bg-orange-100 text-grey-700',
  },
  E: {
    badge: 'bg-indigo-200 text-indigo-800',
    line: 'bg-indigo-200 text-grey-700',
  },
  F: {
    badge: 'bg-pink-200 text-pink-800',
    line: 'bg-pink-200 text-grey-700',
  },
  G: {
    badge: 'bg-lime-100 text-teal-800',
    line: 'bg-lime-100 text-grey-700',
  },
  X: {
    badge: 'bg-yellow-200 text-yellow-700',
    line: 'bg-yellow-100 text-grey-700',
  },
}

const pendingClasses = {
  badge: 'bg-grey-100 text-grey-500',
  line: 'bg-grey-50 text-grey-700',
}

export function PoemAnalysisView() {
  const poem = usePoemStore((state) => state.poem)
  const analysisStatus = usePoemStore((state) => state.analysisStatus)
  const analysisError = usePoemStore((state) => state.analysisError)
  const lines = getPoemLines(poem)

  if (!poem) return <PoemEmptyState />

  const hasMissingGroups = lines.some((line) => !line.group)

  return (
    <div className="flex w-full grow flex-col">
      <h2 className="typo-large text-grey-700 pl-[10px]">{poem.title ?? 'Analýza básně'}</h2>

      {analysisStatus === 'loading' && hasMissingGroups && (
        <p className="mt-3 typo-detail text-grey-600">
          Analýza rýmového schématu se načítá…
        </p>
      )}

      {analysisStatus === 'error' && hasMissingGroups && (
        <p className="mt-3 typo-detail text-grey-600">
          {analysisError ?? 'Analýzu rýmového schématu se nepodařilo načíst.'}
        </p>
      )}

      <div className="mt-5 space-y-2 desktop:mt-7 desktop:space-y-[10px]">
        {lines.map((line) => {
          const group = line.group
          const classes = group ? groupClasses[group] : pendingClasses

          return (
            <div
              key={line.id}
              className="grid grid-cols-[32px_minmax(0,1fr)] items-start gap-2"
            >
              <span
                className={`grid size-8 shrink-0 place-items-center rounded-xl font-medium leading-none ${classes.badge}`}
              >
                {group ?? '?'}
              </span>

              <div
                className={`flex min-h-8 items-center rounded-xl px-3 py-2 typo-detail ${classes.line}`}
              >
                <SmartWrappedVerseText text={line.text} />
              </div>
            </div>
          )
        })}
      </div>

      <PoemCardActions />
    </div>
  )
}