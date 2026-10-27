
'use client'

import { usePoemStore } from '@/stores/poem-store'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'
import {
  getPoemLines,
  PoemCardActions,
  PoemEmptyState,
} from './poem-view-utils'
import { PoemHeader } from './poem-header'
import {
  PoemVerseRow,
  POEM_VERSES_CLASS,
  POEM_VERSE_CONTENT_CLASS,
} from './poem-verse-row'

export function PoemReadingView() {
  const poem = usePoemStore((state) => state.poem)
  const lines = getPoemLines(poem)

  if (!poem) return <PoemEmptyState />

  return (
    <div className="flex grow flex-col">
      <PoemHeader poem={poem} />

      <div className={POEM_VERSES_CLASS}>
        {lines.map((line) => (
          <PoemVerseRow
            key={line.id}
            stanzaStart={line.stanzaStart}
          >
            <div
              className={`${POEM_VERSE_CONTENT_CLASS} bg-grey-50 text-grey-700`}
            >
              {line.text.trim() ? (
                <SmartWrappedVerseText
                  text={line.text}
                  className="w-full"
                />
              ) : (
                <span
                  aria-label="Prázdný verš"
                  className="block w-full"
                />
              )}
            </div>
          </PoemVerseRow>
        ))}
      </div>

      <PoemCardActions />
    </div>
  )
}
