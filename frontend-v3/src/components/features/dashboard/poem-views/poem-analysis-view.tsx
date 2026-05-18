'use client'

import { usePoemStore } from '@/stores/poem-store'
import type { PoemLineGroup } from '@/types/poem'
import { getPoemLines, PoemCardActions, PoemEmptyState } from './poem-view-utils'

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
    badge: 'bg-yellow-100 text-yellow-700',
    line: 'bg-yellow-100 text-grey-700',
  },
  E: {
    badge: 'bg-purple-200 text-purple-800',
    line: 'bg-purple-200 text-grey-700',
  },
  F: {
    badge: 'bg-cyan-100 text-cyan-700',
    line: 'bg-cyan-100 text-grey-700',
  },
  G: {
    badge: 'bg-teal-200 text-teal-800',
    line: 'bg-teal-200 text-grey-700',
  },
  X: {
    badge: 'bg-grey-200 text-grey-700',
    line: 'bg-grey-100 text-grey-700',
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
    <div className="w-full flex flex-col">
      <h2 className="typo-large text-grey-700">{poem.title ?? 'Analýza básně'}</h2>

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

      <div className="mt-5 space-y-2">
        {lines.map((line) => {
          const group = line.group
          const classes = group ? groupClasses[group] : pendingClasses

          return (
            <div key={line.id} className="flex items-start gap-2">
              <span
                className={`grid size-7 shrink-0 place-items-center rounded-xl font-bold leading-none ${classes.badge}`}
              >
                {group ?? '?'}
              </span>

              <p className={`min-h-9 flex-1 rounded-xl px-3 py-2 typo-detail ${classes.line}`}>
                {line.text}
              </p>
            </div>
          )
        })}
      </div>

      <PoemCardActions />
    </div>
  )
}