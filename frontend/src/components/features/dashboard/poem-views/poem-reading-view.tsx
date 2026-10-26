
'use client'

import { usePoemStore } from '@/stores/poem-store'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'
import {
  getPoemLines,
  PoemCardActions,
  PoemEmptyState,
} from './poem-view-utils'
import { PoemHeader } from './poem-header'

export function PoemReadingView() {
  const poem = usePoemStore((state) => state.poem)
  const lines = getPoemLines(poem)

  if (!poem) return <PoemEmptyState />

  return (
    <div className="flex grow flex-col">
      <PoemHeader poem={poem} />

      {/* Verše básně */}
      <div className="mt-5 flex grow flex-col space-y-2 desktop:mt-6 desktop:space-y-[10px]">
        {lines.map((line) => (
            <div
              key={line.id}
              className={[
                'rounded-xl bg-grey-50 px-3 py-2 typo-detail text-grey-700 desktop:min-h-8',
                line.stanzaStart ? '!mt-5 desktop:!mt-6' : '',
              ].join(' ')}
            >
            <SmartWrappedVerseText text={line.text} />
          </div>
        ))}
      </div>

      {/* Akce pod básní */}
      <PoemCardActions />
    </div>
  )
}
