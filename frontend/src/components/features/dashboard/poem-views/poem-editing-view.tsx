'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { toast } from 'sonner'
import { useRouter } from 'next/navigation'

import { usePoemStore } from '@/stores/poem-store'
import { AppIcon } from '@/components/icons/app-icon'
import { SmartWrappedVerseText } from '@/components/ui/smart-wrapped-verse-text'
import { getOriginalLineText } from '@/utils/poem-lines'

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

export function PoemEditingView() {
  const router = useRouter()

  const poem = usePoemStore((state) => state.poem)
  const regeneratePoemLine = usePoemStore(
    (state) => state.regeneratePoemLine,
  )
  const updatePoemLine = usePoemStore(
    (state) => state.updatePoemLine,
  )
  const removePoemLine = usePoemStore(
    (state) => state.removePoemLine,
  )
  const restorePoemLine = usePoemStore(
    (state) => state.restorePoemLine,
  )

  const lines = getPoemLines(poem)

  const [activeLineId, setActiveLineId] = useState<
    string | null
  >(null)


  const [regeneratingLineId, setRegeneratingLineId] =
    useState<string | null>(null)

  const regenerationInProgressRef = useRef(false)

  const textareaRefs = useRef<
    Record<string, HTMLTextAreaElement | null>
  >({})

  const originalLineTexts = useMemo(() => {
    const result = new Map<string, string>()

    if (!poem?.originalText) return result

    for (const line of lines) {
      const original = getOriginalLineText(
        poem.originalText,
        line.id,
      )

      if (original !== undefined) {
        result.set(line.id, original)
      }
    }

    return result
  }, [poem?.originalText, lines])

  useEffect(() => {
    if (!activeLineId) return

    const textarea = textareaRefs.current[activeLineId]

    if (textarea) {
      textarea.focus()
      textarea.setSelectionRange(
        textarea.value.length,
        textarea.value.length,
      )
    }
  }, [activeLineId])

  if (!poem) return <PoemEmptyState />

  function commitLine(lineId: string, text: string) {
    updatePoemLine(lineId, text.trim())
    setActiveLineId(null)
  }

  function handleRemoveLine(lineId: string) {
    removePoemLine(lineId)

    if (activeLineId === lineId) {
      setActiveLineId(null)
    }
  }

  function handleRestoreLine(lineId: string) {
    restorePoemLine(lineId)
    setActiveLineId(null)
  }

  async function handleRegenerateLine(lineId: string) {
    if (regenerationInProgressRef.current) return

    regenerationInProgressRef.current = true
    setRegeneratingLineId(lineId)
    setActiveLineId(null)

    try {
      const regeneratedPoem =
        await regeneratePoemLine(lineId)

      const base =
        process.env.NEXT_PUBLIC_LINK_BASE || '/'

      router.replace(
        `${base}dashboard?poemId=${encodeURIComponent(
          regeneratedPoem.id,
        )}&viewMode=editing`,
      )
    } catch (error) {
      console.error(error)

      toast.error(
        'Nepodařilo se navrhnout úpravu verše. Zkuste to prosím znovu.',
      )
    } finally {
      regenerationInProgressRef.current = false
      setRegeneratingLineId(null)
    }
  }

  const buttonCls =
    'grid size-8 shrink-0 place-items-center rounded-xl cursor-pointer disabled:cursor-not-allowed'

  return (
    <div className="flex w-full grow flex-col">
      <PoemHeader poem={poem} />

      <div className={POEM_VERSES_CLASS}>
        {lines.map((line) => {
          const isActive = activeLineId === line.id
          const isRegenerating = regeneratingLineId === line.id
          const isAnyRegenerating = regeneratingLineId !== null

          const originalText = originalLineTexts.get(
            line.id,
          )

          const isModified =
            originalText !== undefined &&
            originalText !== line.text

          return (
            <PoemVerseRow
              key={line.id}
              stanzaStart={line.stanzaStart}
              left={
                <>
                  <button
                    type="button"
                    aria-label="Upravit verš"
                    aria-pressed={isActive}
                    onClick={() =>
                      setActiveLineId(line.id)
                    }
                    disabled={isAnyRegenerating}
                    className={[
                      buttonCls,
                      isActive
                        ? 'bg-teal-100 text-teal-700'
                        : 'bg-grey-50 text-zinc-700',
                    ].join(' ')}
                  >
                    <AppIcon name="pencil" size={16} />
                  </button>

                  <button
                    type="button"
                    aria-label="Vymazat obsah verše"
                    title="Vymazat obsah verše"
                    onClick={() =>
                      handleRemoveLine(line.id)
                    }
                    disabled={isAnyRegenerating}
                    className={`${buttonCls} bg-grey-50 text-zinc-700`}
                  >
                    <AppIcon name="trash" size={16} />
                  </button>

                  {isModified && (
                    <button
                      type="button"
                      aria-label="Obnovit původní verš"
                      title="Obnovit původní verš"
                      onClick={() =>
                        handleRestoreLine(line.id)
                      }
                      disabled={isAnyRegenerating}
                      className={`${buttonCls} bg-grey-50 text-zinc-700`}
                    >
                      <AppIcon name="undo" size={16} />
                    </button>
                  )}
                </>
              }

              right={
                <button
                  type="button"
                  aria-label={
                    isRegenerating
                      ? 'Probíhá regenerování verše'
                      : 'Navrhnout úpravu verše'
                  }
                  aria-busy={isRegenerating}
                  disabled={
                    !line.text.trim() || isAnyRegenerating
                  }
                  title={
                    isRegenerating
                      ? 'Verš se právě regeneruje…'
                      : line.text.trim()
                        ? 'Navrhnout úpravu verše'
                        : 'Prázdný verš nelze regenerovat'
                  }
                  onClick={() =>
                    void handleRegenerateLine(line.id)
                  }
                  className={[
                    buttonCls,
                    isRegenerating
                      ? 'bg-purple-400 text-white'
                      : 'bg-yellow-400 text-zinc-900',
                    'disabled:cursor-not-allowed',
                    !isRegenerating
                      ? 'disabled:opacity-40'
                      : '',
                  ].join(' ')}
                >
                  <AppIcon name="starsBold" size={18} />
                </button>
              }
            >
            <div className="min-w-0 flex-1">
              {isRegenerating ? (
                <div
                  role="status"
                  aria-label="Probíhá regenerování verše"
                  className={[
                    POEM_VERSE_CONTENT_CLASS,
                    'flex w-full items-center',
                    'bg-purple-100',
                  ].join(' ')}
                >
                  <div
                    aria-hidden="true"
                    className="h-3 w-[72%] animate-pulse rounded-full bg-purple-300"
                  />
                </div>
              ) : isActive ? (
                <textarea
                  ref={(element) => {
                    textareaRefs.current[line.id] = element
                  }}
                  value={line.text}
                  onChange={(event) => {
                    updatePoemLine(
                      line.id,
                      event.target.value,
                    )
                  }}
                  onBlur={(event) => {
                    commitLine(
                      line.id,
                      event.target.value,
                    )
                  }}
                  onKeyDown={(event) => {
                    if (
                      event.key === 'Enter' &&
                      !event.shiftKey
                    ) {
                      event.preventDefault()

                      commitLine(
                        line.id,
                        event.currentTarget.value,
                      )
                    }
                  }}
                  rows={1}
                  className={`${POEM_VERSE_CONTENT_CLASS} block w-full resize-none appearance-none bg-white text-zinc-700 outline-none border-zinc-300`}
                />
              ) : (
                <button
                  type="button"
                  onClick={() =>
                    setActiveLineId(line.id)
                  }
                  className={`${POEM_VERSE_CONTENT_CLASS} flex w-full items-center bg-zinc-100 text-left text-zinc-700`}
                >
                  <SmartWrappedVerseText
                    text={line.text}
                    className="w-full"
                  />
                </button>
              )}
            </div>
            </PoemVerseRow>
          )
        })}
      </div>

      <PoemCardActions />
    </div>
  )
}
