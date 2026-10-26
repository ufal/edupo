'use client'

import { useEffect, useRef, useState } from 'react'
import { toast } from 'sonner'
import { usePoemStore } from '@/stores/poem-store'
import { AppIcon } from '@/components/icons/app-icon'
import { getPoemLines, PoemCardActions, PoemEmptyState } from './poem-view-utils'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'
import { useRouter } from 'next/navigation'
import { useUiStore } from '@/stores/ui-store'

export function PoemEditingView() {
  const router = useRouter()
  const poem = usePoemStore((state) => state.poem)
  const regeneratePoemLine = usePoemStore(
    (state) => state.regeneratePoemLine,
  )
  const updatePoemLine = usePoemStore((state) => state.updatePoemLine)
  const addPoemLine = usePoemStore((state) => state.addPoemLine)
  const removePoemLine = usePoemStore((state) => state.removePoemLine)
  const openOverlay = useUiStore((state) => state.openOverlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  const lines = getPoemLines(poem)
  const [activeLineId, setActiveLineId] = useState<string | null>(null)
  const textareaRefs = useRef<Record<string, HTMLTextAreaElement | null>>({})

  useEffect(() => {
    if (!activeLineId) return

    const textarea = textareaRefs.current[activeLineId]

    if (textarea) {
      textarea.focus()
      textarea.setSelectionRange(textarea.value.length, textarea.value.length)
    }
  }, [activeLineId])

  if (!poem) return <PoemEmptyState />

  function commitLine(lineId: string, text: string) {
    const normalizedText = text.trim()

    if (!normalizedText) {
      removePoemLine(lineId)
      setActiveLineId(null)
      return
    }

    updatePoemLine(lineId, normalizedText)
    setActiveLineId(null)
  }

  async function handleRegenerateLine(lineId: string) {
    openOverlay('generation')

    try {
      const regeneratedPoem = await regeneratePoemLine(lineId)
      const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

      router.replace(
        `${base}dashboard?poemId=${encodeURIComponent(regeneratedPoem.id)}&viewMode=editing`,
      )
    } catch (error) {
      console.error(error)
      toast.error(
        'Nepodařilo se navrhnout úpravu verše. Zkuste to prosím znovu.',
      )
    } finally {
      closeOverlay()
    }
  }

  return (
    <div className="flex w-full grow flex-col">
      <h2 className="typo-large text-zinc-700 pl-[10px]">{poem.title ?? 'Úprava textu'}</h2>

      <div className="mt-5 space-y-2 desktop:mt-7 desktop:space-y-[10px]">
        {lines.map((line) => {
          const isActive = activeLineId === line.id
          const buttonCls = "grid size-8 desktop:size-8 place-items-center rounded-xl cursor-pointer"

          return (
            <div
              key={line.id}
              className={[
                'grid grid-cols-[32px_minmax(0,1fr)_32px] items-start gap-2',
                line.stanzaStart ? '!mt-5 desktop:!mt-6' : '',
              ].join(' ')}
            >
              <button
                type="button"
                aria-label="Upravit verš"
                onClick={() => setActiveLineId(line.id)}
                className={`${buttonCls} ${
                  isActive
                    ? 'bg-teal-100 text-teal-700'
                    : 'bg-grey-50 text-zinc-700'
                }`}
              >
                <AppIcon name="pencil" size={16} />
              </button>

              {isActive ? (
                <textarea
                  ref={(element) => {
                    textareaRefs.current[line.id] = element
                  }}
                  value={line.text}
                  onFocus={() => setActiveLineId(line.id)}
                  onChange={(event) => {
                    updatePoemLine(line.id, event.target.value)
                  }}
                  onBlur={(event) => {
                    commitLine(line.id, event.target.value)
                  }}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter' && !event.shiftKey) {
                      event.preventDefault()
                      commitLine(line.id, event.currentTarget.value)
                    }
                  }}
                  rows={1}
                  className="min-h-8 w-full resize-none rounded-xl border border-zinc-100 bg-white px-3 py-2 typo-detail text-zinc-700 outline-none"
                />
              ) : (
                <button
                  type="button"
                  onClick={() => setActiveLineId(line.id)}
                  className="flex min-h-8 w-full items-start rounded-xl border border-transparent bg-zinc-100 px-3 py-2 text-left typo-detail text-zinc-700"
                >
                  <SmartWrappedVerseText text={line.text} className="w-full" />
                </button>
              )}

              <button
                type="button"
                aria-label="Navrhnout úpravu verše"
                onClick={() => void handleRegenerateLine(line.id)}
                className="grid size-8 place-items-center rounded-xl bg-yellow-300 cursor-pointer"
              >
                <AppIcon name="stars" size={22} />
              </button>
            </div>
          )
        })}
      </div>

      <PoemCardActions />
    </div>
  )
}