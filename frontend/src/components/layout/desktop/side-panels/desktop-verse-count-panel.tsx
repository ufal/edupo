'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Slider } from '@/components/ui/slider'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  DEFAULT_VERSE_COUNT,
  MAX_VERSES,
  MIN_VERSES,
  VERSE_COUNT_STEP,
  getRandomVerseCount,
  isValidVerseCount,
} from '@/config/poem-param-verse-count'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'

type DesktopVerseCountPanelProps = {
  onClose: () => void
}

export function DesktopVerseCountPanel({
  onClose,
}: DesktopVerseCountPanelProps) {
  const storedVerseCount = usePoemStore((state) => state.params.verseCount)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedVerseCount !== 'number') {
      updateParams({ verseCount: DEFAULT_VERSE_COUNT })
    }
  }, [storedVerseCount, updateParams])

  const verseCount =
    typeof storedVerseCount === 'number'
      ? storedVerseCount
      : DEFAULT_VERSE_COUNT

  const [inputValue, setInputValue] = useState(String(verseCount))

  useEffect(() => {
    setInputValue(String(verseCount))
  }, [verseCount])

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.verseCount.title}
      onClose={onClose}
      infoText={poemParamInfoTexts.verseCount.text}
    >
      <p className="typo-body font-bold">
        Nastavte počet veršů
      </p>

      <div className="mt-8 flex items-center gap-5">
        <label className="typo-body font-medium">
          Počet veršů
        </label>

        <Input
          type="number"
          min={MIN_VERSES}
          max={MAX_VERSES}
          step={VERSE_COUNT_STEP}
          value={inputValue}
          className="min-w-0 flex-1"
          onChange={(event) => {
            const nextInputValue = event.target.value
            setInputValue(nextInputValue)

            const nextValue = Number(nextInputValue)

            if (!isValidVerseCount(nextValue)) return

            updateParams({ verseCount: nextValue })
          }}
          onBlur={() => {
            setInputValue(String(verseCount))
          }}
        />
      </div>

      <Slider
        colorTheme="yellow"
        className="mt-7"
        min={MIN_VERSES}
        max={MAX_VERSES}
        step={VERSE_COUNT_STEP}
        value={[verseCount]}
        onValueChange={(value) => {
          updateParams({
            verseCount: value[0] ?? verseCount,
          })
        }}
      />

      <Button
        type="button"
        variant="subtle"
        size="md"
        className="mt-7 w-full"
        onClick={() => {
          updateParams({ verseCount: getRandomVerseCount() })
        }}
      >
        Nastavit náhodně
      </Button>
    </DesktopSidePanelShell>
  )
}