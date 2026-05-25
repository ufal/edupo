'use client'

import { usePoemStore } from '@/stores/poem-store'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'
import { getPoemLines, PoemCardActions, PoemEmptyState } from './poem-view-utils'

export function PoemReadingView() {
  const poem = usePoemStore((state) => state.poem)
  const lines = getPoemLines(poem)

  if (!poem) return <PoemEmptyState />

  return (
    <div className="flex flex-col grow">
      <h2 className="typo-large text-grey-700">{poem.title ?? 'Vygenerovaná báseň'}</h2>

      <div className="flex flex-col grow mt-5 space-y-2">
        {lines.map((line) => (
          <div
            key={line.id}
            className="rounded-xl bg-grey-50 px-3 py-2 typo-detail text-grey-700"
          >
            <SmartWrappedVerseText text={line.text} />
          </div>
        ))}
      </div>

      <PoemCardActions />
    </div>
  )
}