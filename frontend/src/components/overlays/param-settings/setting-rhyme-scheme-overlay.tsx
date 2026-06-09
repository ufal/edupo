'use client'

import { useEffect, useMemo, useState } from 'react'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { RhymeSlotSelect, RhymeValue } from '@/components/ui/rhyme-slot-select'

import { PlainSelect } from '@/components/ui/plain-select'
import { usePoemStore } from '@/stores/poem-store'
import { LockedParamOverlay } from './locked-param-overlay'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  MAX_RHYME_SCHEME_VERSES,
  normalizeRhymeScheme,
  rhymeSchemeToString,
  getDefaultRhymeScheme,
  getFavoriteRhymeSchemes,
  getRandomRhymeScheme,
  getRhymeSchemeOptions,
} from '@/config/poem-param-rhyme-scheme'

export function SettingRhymeSchemeOverlay({
  onClose,
}: {
  onClose: () => void
}) {
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
  const favoriteOptions = getRhymeSchemeOptions(verseCount)

  const updateSlot = (index: number, value: RhymeValue) => {
    const nextValues = [...values]
    nextValues[index] = value

    updateParams({
      rhymeScheme: rhymeSchemeToString(nextValues, verseCount)
    })
  }

  if (!isEditable) {
    return (
      <LockedParamOverlay
        iconName="verseGroups"
        title={poemParamInfoTexts.rhymeScheme.title}
        infoText={poemParamInfoTexts.rhymeScheme.text}
        onClose={onClose}
        messageTitle="Rýmové schéma je určeno zvolenou formou"
        messageBody="U sonetu, limeriku a haiku nastavuje rýmové schéma automaticky generátor."
      />
    )
  }

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="verseGroups"
        title={poemParamInfoTexts.rhymeScheme.title}
        onClose={onClose}
        infoText={poemParamInfoTexts.rhymeScheme.text}
      />

      <div className="px-5 pt-8">
        <div>
          <p className="typo-large text-grey-900">
            Aktuální nastavené schéma
          </p>

          <p className="mt-1 typo-body font-medium text-grey-900">
            {currentScheme}
          </p>
        </div>

        <div className="mt-6 flex flex-wrap gap-x-4 gap-y-4">
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
          className="mt-10"
          value={favoriteSchemes.includes(currentScheme) ? currentScheme : undefined}
          placeholder="Další oblíbená schémata"
          options={favoriteOptions}
          onChange={(scheme) => updateParams({ rhymeScheme: scheme })}
        />

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            updateParams({
              rhymeScheme: getRandomRhymeScheme(verseCount)
            })
          }}
        >
          Vyplnit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}