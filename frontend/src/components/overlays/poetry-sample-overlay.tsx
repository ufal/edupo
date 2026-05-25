'use client'

import { useRouter } from 'next/navigation'
import { useMemo, useState } from 'react'
import { Search, X } from 'lucide-react'
import { ShellOverlay } from './shell-overlay'
import { getAllPoetrySamples } from '@/services/poetry-samples-service'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'

type PoetrySampleOverlayProps = {
  onClose: () => void
}

export function PoetrySampleOverlay({ onClose }: PoetrySampleOverlayProps) {
  const router = useRouter()
  const samples = getAllPoetrySamples()
  const loadPoetrySample = usePoemStore((s) => s.loadPoetrySample)
  const openOverlay = useUiStore((s) => s.openOverlay)
  const closeOverlay = useUiStore((s) => s.closeOverlay)

  const [query, setQuery] = useState('')
  
  const filteredSamples = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()

    if (!normalizedQuery) return samples

    return samples.filter((sample) => {
        return [
        sample.label,
        sample.collectionTitle,
        sample.author,
        sample.poem.title,
        ]
        .join(' ')
        .toLowerCase()
        .includes(normalizedQuery)
    })},
    [query, samples])

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <header className="flex h-20 items-center justify-between bg-purple-700 px-5 text-white">
        <h2 className="text-lg font-medium">
          Ukázka poezie
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
            {
                filteredSamples.map((sample, index) => (
                    <button
                        key={sample.id}
                        type="button"
                        onClick={async () => {
                          closeOverlay()
                          openOverlay('generation')

                          await loadPoetrySample(sample.id)

                          closeOverlay()
                          router.push((process.env.NEXT_PUBLIC_LINK_BASE || "/") + "dashboard")
                        }}
                        className={[
                          'block w-full rounded-md px-2 py-2 text-left text-base leading-6 text-zinc-700',
                          'transition-colors',
                          'hover:bg-teal-50',
                          'active:bg-teal-100',
                        ].join(' ')}
                    >
                        {sample.label}
                    </button>
                ))
            }
            {
                filteredSamples.length === 0 && (
                    <p className="px-2 py-6 text-center text-sm text-zinc-400">
                        Nic jsme nenašli.
                    </p>
                )
            }
          </div>
        </div>
      </section>
    </ShellOverlay>
  )
}