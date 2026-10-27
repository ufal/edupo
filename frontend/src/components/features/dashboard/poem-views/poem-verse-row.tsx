import type { ReactNode } from 'react'

type PoemVerseRowProps = {
  stanzaStart?: boolean
  left?: ReactNode
  right?: ReactNode
  children: ReactNode
}

export const POEM_VERSES_CLASS =
  'mt-5 flex flex-col gap-2 desktop:mt-6 desktop:gap-[10px]'

export const POEM_VERSE_CONTENT_CLASS =
  'box-border min-h-8 min-w-0 rounded-xl border border-transparent px-3 py-[7px] typo-detail leading-4'
  
export function PoemVerseRow({
  stanzaStart = false,
  left,
  right,
  children,
}: PoemVerseRowProps) {
  return (
    <div
      className={[
        'flex min-w-0 items-start gap-2',
        stanzaStart
          ? 'mt-3 desktop:mt-[14px]'
          : '',
      ].join(' ')}
    >
      {left != null && (
        <div className="flex shrink-0 items-start gap-2">
          {left}
        </div>
      )}

      <div className="min-w-0 flex-1">
        {children}
      </div>

      {right != null && (
        <div className="flex shrink-0 items-start">
          {right}
        </div>
      )}
    </div>
  )
}
