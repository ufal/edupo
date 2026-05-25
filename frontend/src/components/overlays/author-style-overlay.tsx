'use client'

import { useRouter } from 'next/navigation'
import { useMemo, useState } from 'react'
import { Search, X } from 'lucide-react'
import { ShellOverlay } from './shell-overlay'
import { getAllAuthorStyles } from '@/services/author-styles-service'
import { usePoemStore } from '@/stores/poem-store'

type AuthorStyleOverlayProps = {
  onClose: () => void
}

export function AuthorStyleOverlay({ onClose }: AuthorStyleOverlayProps) {
  const router = useRouter()

  const [query, setQuery] = useState('')
  const authorStyles = getAllAuthorStyles()

  const selectedAuthorStyleId = usePoemStore(
    (state) => state.selectedAuthorStyleId,
  )
  const setSelectedAuthorStyleId = usePoemStore(
    (state) => state.setSelectedAuthorStyleId,
  )

  const filteredAuthorStyles = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()

    if (!normalizedQuery) return authorStyles

    return authorStyles.filter((author) =>
      [author.label, author.description]
        .join(' ')
        .toLowerCase()
        .includes(normalizedQuery),
    )
  }, [query, authorStyles])

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <header className="flex h-20 items-center justify-between bg-purple-700 px-5 text-white">
        <h2 className="text-lg font-medium">
          Styl podle autora
        </h2>

        <button
          type="button"
          aria-label="Zavřít"
          onClick={onClose}
          className="grid size-9 place-items-center"
        >
          <X size={26} strokeWidth={2.2} />
        </button>
      </header>

      <section className="px-5 pt-5">
        <div className="rounded-3xl bg-white px-3 py-4">
          <div className="flex items-center gap-2 border-b border-zinc-200 px-2 pb-2 text-zinc-400">
            <Search size={18} strokeWidth={2.2} />

            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Hledat autora"
              className="h-8 min-w-0 flex-1 bg-transparent text-sm outline-none placeholder:text-zinc-400"
            />
          </div>

          <div className="mt-2 space-y-1">
            {filteredAuthorStyles.map((author) => {
              const selected = author.id === selectedAuthorStyleId

              return (
                <button
                  key={author.id}
                  type="button"
                  onClick={() => {
                    setSelectedAuthorStyleId(author.id)
                    onClose()
                    router.push((process.env.NEXT_PUBLIC_LINK_BASE || "/") + "dashboard")
                  }}
                  className={[
                    'block w-full rounded-md px-2 py-2 text-left leading-6 text-zinc-700',
                    'transition-colors',
                    selected
                      ? 'bg-teal-100'
                      : 'hover:bg-teal-50 active:bg-teal-100',
                  ].join(' ')}
                >
                  <span className="block text-base">
                    {author.label}
                  </span>
                </button>
              )
            })}

            {filteredAuthorStyles.length === 0 && (
              <p className="px-2 py-6 text-center text-sm text-zinc-400">
                Nic jsme nenašli.
              </p>
            )}
          </div>
        </div>
      </section>
    </ShellOverlay>
  )
}