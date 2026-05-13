'use client'

import { useEffect } from 'react'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { LockedParamOverlay } from './locked-param-overlay'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'

const title = 'Počet veršů'
const infoText = 'Kolik má mít báseň veršů?'

const MIN_VERSES = 2
const MAX_VERSES = 10
const STEP = 2
const DEFAULT_VERSES = 6

export function SettingVerseCountOverlay({ onClose }: { onClose: () => void }) {
  const storedVerseCount = usePoemStore((state) => state.params.verseCount)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedVerseCount !== 'number') {
      updateParams({ verseCount: DEFAULT_VERSES })
    }
  }, [storedVerseCount, updateParams])

  const verseCount = storedVerseCount ?? DEFAULT_VERSES

  const form = usePoemStore((state) => state.params.form)
  const isEditable = !form || form === 'free' || form === 'epigram'

  if (!isEditable) {
    return (
      <LockedParamOverlay
        iconName="verseList"
        title={title}
        infoText={infoText}
        onClose={onClose}
        messageTitle="Počet veršů je určen zvolenou formou"
        messageBody="U sonetu, limeriku a haiku nastavuje počet veršů automaticky generátor."
      />
    )
  }

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="verseList"
        title={title}
        onClose={onClose}
        infoText={infoText}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-700">
          Nastavte počet veršů
        </p>

        <div className="mt-8 flex items-center gap-5">
          <label className="typo-body font-semibold text-grey-900">
            Počet veršů
          </label>

          <Input
            readOnly
            value={String(verseCount)}
            className="flex-1"
          />
        </div>

        <Slider
          className="mt-7"
          min={MIN_VERSES}
          max={MAX_VERSES}
          step={STEP}
          value={[verseCount]}
          onValueChange={(value) => {
            updateParams({
              verseCount: value[0] ?? verseCount,
            })
          }}
        />

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            const random = Math.floor(Math.random() * (MAX_VERSES - MIN_VERSES + 1)) + MIN_VERSES
            updateParams({ verseCount: random })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}