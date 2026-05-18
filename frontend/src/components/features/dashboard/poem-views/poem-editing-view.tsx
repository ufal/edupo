'use client'

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import { MAX_POEM_LINES, usePoemStore } from '@/stores/poem-store'
import { AppIcon } from '@/components/icons/app-icon'
import { getPoemLines, PoemCardActions, PoemEmptyState } from './poem-view-utils'

export function PoemEditingView() {
  const poem = usePoemStore((state) => state.poem)
  const updatePoemLine = usePoemStore((state) => state.updatePoemLine)
  const addPoemLine = usePoemStore((state) => state.addPoemLine)
  const removePoemLine = usePoemStore((state) => state.removePoemLine)

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

  function handleAddLine() {
    const newLineId = addPoemLine()

    if (newLineId) {
      setActiveLineId(newLineId)
    }
  }

  return (
    <div className="w-full flex flex-col">
      <h2 className="typo-large text-zinc-700">
        {poem.title ?? 'Úprava textu'}
      </h2>

      <div className="mt-5 space-y-2">
        {lines.map((line) => {
          const isActive = activeLineId === line.id
          const buttonCls = 'grid size-6 place-items-center rounded-lg'

          return (
            <div
              key={line.id}
              className="grid grid-cols-[24px_1fr_32px] gap-2"
            >
              <div className="space-y-1 pt-1">
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

                <button
                  type="button"
                  aria-label="Smazat verš"
                  onClick={() => removePoemLine(line.id)}
                  className={`${buttonCls} text-zinc-700 ${
                    isActive ? 'bg-yellow-300' : 'bg-grey-50'
                  }`}
                >
                  <AppIcon name="X" size={16} />
                </button>
              </div>

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
                rows={isActive ? 3 : 2}
                className={`w-full resize-none rounded-xl px-2 py-1 typo-detail text-zinc-700 outline-none ${
                  isActive
                    ? 'border border-zinc-100 bg-white'
                    : 'border border-transparent bg-zinc-100'
                }`}
              />

              <button
                type="button"
                aria-label="Navrhnout úpravu verše"
                className="grid size-8 place-items-center rounded-xl bg-teal-700 text-white"
              >
                <AppIcon name="starsBold" size={18} />
              </button>
            </div>
          )
        })}
      </div>

      {
        lines.length < MAX_POEM_LINES && (
          <button
            type="button"
            aria-label="Přidat verš"
            onClick={handleAddLine}
            className="mx-auto mt-5 grid size-7 place-items-center rounded-xl bg-teal-700"
          >
            <Image src="/assets/icons/plus.svg" alt="" width={15} height={15} />
          </button>
        )
      }

      <PoemCardActions />
    </div>
  )
}