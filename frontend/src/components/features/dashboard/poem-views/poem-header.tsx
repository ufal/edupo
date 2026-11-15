
'use client'

import { Avatar } from '@/components/ui/avatar'
import { getAllAuthorStyles } from '@/services/author-styles-service'
import type { Poem } from '@/types/poem'

type PoemHeaderProps = {
  poem: Poem
}

function cleanAuthorName(name: string): string {
  return name
    .replace(/\s*\[(?:vygenerováno|vloženo uživatelem)\]\s*$/i, '')
    .trim()
}

function normalizeAuthorName(name: string): string {
  return cleanAuthorName(name)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .toLowerCase()
}

export function PoemHeader({ poem }: PoemHeaderProps) {
  const authorName = cleanAuthorName(poem.authorName ?? '')

  const author = getAllAuthorStyles().find(
    (style) =>
      normalizeAuthorName(style.label) ===
      normalizeAuthorName(authorName),
  )

  const origin =
    poem.origin ??
    (/\[vygenerováno\]\s*$/i.test(poem.authorName ?? '')
      ? 'generated'
      : /\[vloženo uživatelem\]\s*$/i.test(poem.authorName ?? '')
        ? 'user'
        : 'unknown')

  let authorDescription: string

  if (origin === 'generated') {
    authorDescription = author
      ? `Vygenerováno ve stylu ${author.genitive}`
      : 'Vygenerováno umělou inteligencí'
  } else if (origin === 'user') {
    authorDescription = 'Vloženo uživatelem'
  } else {
    authorDescription = authorName || 'Autor neuveden'
  }

  return (
    <>
      {/* Původní mobilní hlavička – beze změny */}
      <h2 className="pl-[10px] typo-large text-grey-700 desktop:hidden">
        {poem.title ?? 'Vygenerovaná báseň'}
      </h2>

      {/* Společná desktopová hlavička */}
      <div className="hidden desktop:flex desktop:items-center desktop:gap-8">
        <div className="shrink-0">
          <Avatar
            src={author?.avatarSrc}
            alt={authorName || 'Autor'}
            size={92}
          />
        </div>

        <div className="flex min-w-0 flex-col gap-2">
          <h2 className="typo-large font-bold text-grey-700">
            {poem.title ?? 'Vygenerovaná báseň'}
          </h2>

          <p className="typo-body text-grey-700">
            {authorDescription}
          </p>
        </div>
      </div>
    </>
  )
}
