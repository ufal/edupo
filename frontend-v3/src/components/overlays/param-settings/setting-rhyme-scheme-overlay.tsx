'use client'

import { useEffect, useMemo, useState } from 'react'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { RhymeSlotSelect, RhymeValue } from '@/components/ui/rhyme-slot-select'

import { PlainSelect } from '@/components/ui/plain-select'
import { usePoemStore } from '@/stores/poem-store'
import { LockedParamOverlay } from './locked-param-overlay'

const MAX_VERSES = 10

const FAVORITE_SCHEMES = [
  'AABB',
  'ABAB',
  'ABBA',
  'XAXA',
  'AAXX',
  'XXXX',
  'AABBCC',
  'ABABCC',
  'ABABXX',
  'XXXXXX',
]

const title = 'Rýmové schéma'
const infoText =
  'Rýmové schéma určuje, které verše se mají rýmovat. Stejná písmena označují verše se stejným rýmem, X označuje verš bez rýmu.'

function normalizeScheme(scheme: string | undefined, verseCount: number) {
  const chars = (scheme ?? '')
    .toUpperCase()
    .split('')
    .filter((char): char is RhymeValue =>
      ['A', 'B', 'C', 'X'].includes(char),
    )

  return Array.from({ length: MAX_VERSES }, (_, index) => {
    if (index >= verseCount) return 'X'
    return chars[index] ?? 'X'
  })
}

function schemeToString(values: RhymeValue[], verseCount: number) {
  return values.slice(0, verseCount).join('')
}

function getDefaultScheme(verseCount: number) {
  return 'X'.repeat(verseCount)
}

function getRandomScheme(verseCount: number) {
  const matching = FAVORITE_SCHEMES.filter(
    (scheme) => scheme.length === verseCount,
  )

  if (matching.length > 0) {
    return matching[Math.floor(Math.random() * matching.length)]
  }

  const randomValues: RhymeValue[] = ['A', 'B', 'C', 'X']

  return Array.from({ length: verseCount }, () => {
    return randomValues[Math.floor(Math.random() * randomValues.length)]
  }).join('')
}

export function SettingRhymeSchemeOverlay({
  onClose,
}: {
  onClose: () => void
}) {
  const form = usePoemStore((state) => state.params.form)
  const isEditable = true // !form || form === 'free' || form === 'epigram'

  const verseCount = usePoemStore((state) =>
    Math.min(state.params.verseCount ?? 6, MAX_VERSES),
  )
  const rhymeScheme = usePoemStore((state) => state.params.rhymeScheme)
  const updateParams = usePoemStore((state) => state.updateParams)

  const defaultScheme = getDefaultScheme(verseCount)

  useEffect(() => {
    if (!isEditable || rhymeScheme) return

    updateParams({
      rhymeScheme: defaultScheme,
    })
  }, [isEditable, rhymeScheme, defaultScheme, updateParams])

  const [openSlotIndex, setOpenSlotIndex] = useState<number | null>(null)

  const values = useMemo(
    () => normalizeScheme(rhymeScheme ?? defaultScheme, verseCount),
    [rhymeScheme, defaultScheme, verseCount],
  )

  const currentScheme = schemeToString(values, verseCount)

  const favoriteSchemes = FAVORITE_SCHEMES.filter(
    (scheme) => scheme.length === verseCount,
  )

  const favoriteOptions = favoriteSchemes.map((scheme) => ({
    value: scheme,
    label: scheme,
  }))

  const updateSlot = (index: number, value: RhymeValue) => {
    const nextValues = [...values]
    nextValues[index] = value

    updateParams({
      rhymeScheme: schemeToString(nextValues, verseCount),
    })
  }

  if (!isEditable) {
    return (
      <LockedParamOverlay
        iconName="verseGroups"
        title={title}
        infoText={infoText}
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
        title={title}
        onClose={onClose}
        infoText={infoText}
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
              rhymeScheme: getRandomScheme(verseCount),
            })
          }}
        >
          Vyplnit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}