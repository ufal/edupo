'use client'

import { useEffect, useMemo, useState } from 'react'
import { Button } from '@/components/ui/button'
import { PlainSelect } from '@/components/ui/plain-select'
import { RhymeSlotSelect, RhymeValue } from '@/components/ui/rhyme-slot-select'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import {
  MAX_RHYME_SCHEME_VERSES,
  normalizeRhymeScheme,
  rhymeSchemeToString,
  getDefaultRhymeScheme,
  getFavoriteRhymeSchemes,
  getRandomRhymeScheme,
  getRhymeSchemeOptions,
} from '@/config/poem-param-rhyme-scheme'

type DesktopRhymeSchemePanelProps = {
  onClose: () => void
}

export function DesktopRhymeSchemePanel({
  onClose,
}: DesktopRhymeSchemePanelProps) {
  const form = usePoemStore((state) => state.params.form)
  const isEditable = true // !form || form === 'free' || form === 'epigram'

  const verseCount = usePoemStore((state) =>
    Math.min(state.params.verseCount ?? 6, MAX_RHYME_SCHEME_VERSES),
  )
  const rhymeScheme = usePoemStore((state) => state.params.rhymeScheme)
  const updateParams = usePoemStore((state) => state.updateParams)

  const defaultScheme = getDefaultRhymeScheme(verseCount)

  useEffect(() => {
    if (!isEditable || rhymeScheme) return

    updateParams({
      rhymeScheme: defaultScheme,
    })
  }, [isEditable, rhymeScheme, defaultScheme, updateParams])

  const [openSlotIndex, setOpenSlotIndex] = useState<number | null>(null)

  const values = useMemo(
    () => normalizeRhymeScheme(rhymeScheme ?? defaultScheme, verseCount),
    [rhymeScheme, defaultScheme, verseCount],
  )

  const currentScheme = rhymeSchemeToString(values, verseCount)

  const favoriteSchemes = getFavoriteRhymeSchemes(verseCount)

  const favoriteOptions = favoriteSchemes.map((scheme) => ({
    value: scheme,
    label: scheme,
  }))

  const updateSlot = (index: number, value: RhymeValue) => {
    const nextValues = [...values]
    nextValues[index] = value

    updateParams({
      rhymeScheme: rhymeSchemeToString(nextValues, verseCount),
    })
  }

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.rhymeScheme.title}
      onClose={onClose}
      infoText={poemParamInfoTexts.rhymeScheme.text}
    >
      <div>
        <p className="typo-large font-bold">
          Aktuální nastavené schéma
        </p>

        <p className="mt-1 typo-body font-bold">
          {currentScheme}
        </p>
      </div>

      <div className="mt-7 flex flex-wrap gap-x-4 gap-y-4">
        {values.map((value, index) => (
          <RhymeSlotSelect
            key={index}
            value={index < verseCount ? value : '-'}
            disabled={index >= verseCount}
            isOpen={openSlotIndex === index}
            onOpenChange={(open) => setOpenSlotIndex(open ? index : null)}
            onChange={(nextValue) => updateSlot(index, nextValue)}
          />
        ))}
      </div>

      <PlainSelect
        className="mt-14"
        value={favoriteSchemes.includes(currentScheme) ? currentScheme : undefined}
        placeholder="Další oblíbená schémata"
        options={favoriteOptions}
        onChange={(scheme) => updateParams({ rhymeScheme: scheme })}
      />

      <Button
        type="button"
        variant="subtle"
        size="md"
        className="mt-6 w-full"
        onClick={() => {
          updateParams({
            rhymeScheme: getRandomRhymeScheme(verseCount),
          })
        }}
      >
        Vyplnit náhodně
      </Button>
    </DesktopSidePanelShell>
  )
}