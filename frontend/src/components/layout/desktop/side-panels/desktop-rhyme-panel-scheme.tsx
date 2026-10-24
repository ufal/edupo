'use client'

import { useState } from 'react'
import { PlainSelect } from '@/components/ui/plain-select'
import {
  RhymeSlotSelect,
  type RhymeDisplayValue,
  type RhymeValue,
} from '@/components/ui/rhyme-slot-select'
import { usePoemStore } from '@/stores/poem-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  MAX_RHYME_SCHEME_VERSES,
  RHYME_VALUES,
  getFavoriteRhymeSchemes,
  FAVORITE_RHYME_SCHEMES
} from '@/config/poem-param-rhyme-scheme'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopParamSetting } from './desktop-param-setting'

type DesktopRhymeSchemePanelProps = {
  onClose: () => void
}

export function DesktopRhymeSchemePanel({
  onClose,
}: DesktopRhymeSchemePanelProps) {
  const storedVerseCount = usePoemStore(
    (state) => state.params.verseCount,
  )
  const rhymeScheme = usePoemStore(
    (state) => state.params.rhymeScheme,
  )
  const updateParams = usePoemStore((state) => state.updateParams)

  const rhymeUnset = useDesktopSettingsUiStore(
    (state) => state.unset.rhymeScheme,
  )
  const verseCountUnset = useDesktopSettingsUiStore(
    (state) => state.unset.verseCount,
  )

  const [openSlotIndex, setOpenSlotIndex] = useState<number | null>(
    null,
  )

  const verseCount =
    !verseCountUnset && typeof storedVerseCount === 'number'
      ? Math.min(storedVerseCount, MAX_RHYME_SCHEME_VERSES)
      : MAX_RHYME_SCHEME_VERSES

  const values: RhymeDisplayValue[] = Array.from(
    { length: MAX_RHYME_SCHEME_VERSES },
    (_, index) => {
      const char = rhymeScheme?.[index]?.toUpperCase()

      return char && RHYME_VALUES.includes(char as RhymeValue)
        ? (char as RhymeValue)
        : '-'
    },
  )

  const currentScheme = rhymeUnset
    ? '-'.repeat(verseCount)
    : values.slice(0, verseCount).join('')

  const hasVerseCount = !verseCountUnset && typeof storedVerseCount === 'number'

  const favoriteSchemes = hasVerseCount
    ? getFavoriteRhymeSchemes(verseCount)
    : FAVORITE_RHYME_SCHEMES

  const favoriteOptions = favoriteSchemes.map((scheme) => ({
    value: scheme,
    label: scheme,
  }))

  function updateSlot(index: number, value: RhymeValue) {
    if (rhymeUnset) return

    const nextValues = [...values]
    nextValues[index] = value

    // Zachováme i dříve vyplněné pozice mimo aktuální počet veršů.
    // Odstraníme pouze koncové prázdné pozice.
    const nextScheme = nextValues.join('').replace(/-+$/, '')

    updateParams({
      rhymeScheme: nextScheme || undefined,
    })
  }

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.rhymeScheme.title}
      infoText={poemParamInfoTexts.rhymeScheme.text}
      onClose={onClose}
    >
      <DesktopParamSetting
        param="rhymeScheme"
        label="Rýmové schéma"
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
              value={
                rhymeUnset || index >= verseCount
                  ? '-'
                  : value
              }
              allowEmptySelection
              disabled={rhymeUnset || index >= verseCount}
              isOpen={
                !rhymeUnset &&
                index < verseCount &&
                openSlotIndex === index
              }
              onOpenChange={(open) =>
                setOpenSlotIndex(open ? index : null)
              }
              onChange={(nextValue) => updateSlot(index, nextValue)}
            />
          ))}
        </div>

        <PlainSelect
          className="mt-14"
          value={
            !rhymeUnset &&
            rhymeScheme &&
            favoriteSchemes.includes(rhymeScheme)
              ? rhymeScheme
              : undefined
          }
          placeholder="Další oblíbená schémata"
          options={favoriteOptions}
          onChange={(scheme) => {
            if (rhymeUnset) return

            updateParams({ rhymeScheme: scheme })
            setOpenSlotIndex(null)
          }}
        />
      </DesktopParamSetting>
    </DesktopSidePanelShell>
  )
}