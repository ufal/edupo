'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Slider } from '@/components/ui/slider'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  DEFAULT_FIRST_VERSE_LENGTH,
  FIRST_VERSE_LENGTH_STEP,
  MAX_FIRST_VERSE_LENGTH,
  MIN_FIRST_VERSE_LENGTH,
  getRandomFirstVerseLength,
  isValidFirstVerseLength,
} from '@/config/poem-param-first-verse-length'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'

type DesktopFirstVerseLengthPanelProps = {
  onClose: () => void
}

export function DesktopFirstVerseLengthPanel({
  onClose,
}: DesktopFirstVerseLengthPanelProps) {
  const storedFirstVerseLength = usePoemStore(
    (state) => state.params.firstVerseLength,
  )
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedFirstVerseLength !== 'number') {
      updateParams({ firstVerseLength: DEFAULT_FIRST_VERSE_LENGTH })
    }
  }, [storedFirstVerseLength, updateParams])

  const firstVerseLength =
    typeof storedFirstVerseLength === 'number'
      ? storedFirstVerseLength
      : DEFAULT_FIRST_VERSE_LENGTH

  const [inputValue, setInputValue] = useState(String(firstVerseLength))

  useEffect(() => {
    setInputValue(String(firstVerseLength))
  }, [firstVerseLength])

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.firstVerseLength.title}
      onClose={onClose}
      infoText={poemParamInfoTexts.firstVerseLength.text}
    >
      <p className="typo-body font-bold">
        Nastavte počet slabik
      </p>

      <div className="mt-8 flex items-center gap-5">
        <label className="typo-body font-medium">
          Délka prvního verše
        </label>

        <Input
          type="number"
          min={MIN_FIRST_VERSE_LENGTH}
          max={MAX_FIRST_VERSE_LENGTH}
          step={FIRST_VERSE_LENGTH_STEP}
          value={inputValue}
          className="min-w-0 flex-1"
          onChange={(event) => {
            const nextInputValue = event.target.value
            setInputValue(nextInputValue)

            const nextValue = Number(nextInputValue)

            if (!isValidFirstVerseLength(nextValue)) return

            updateParams({ firstVerseLength: nextValue })
          }}
          onBlur={() => {
            setInputValue(String(firstVerseLength))
          }}
        />
      </div>

      <Slider
        colorTheme="yellow"
        className="mt-7"
        min={MIN_FIRST_VERSE_LENGTH}
        max={MAX_FIRST_VERSE_LENGTH}
        step={FIRST_VERSE_LENGTH_STEP}
        value={[firstVerseLength]}
        onValueChange={(value) => {
          updateParams({
            firstVerseLength: value[0] ?? firstVerseLength,
          })
        }}
      />

      <Button
        type="button"
        variant="subtle"
        size="md"
        className="mt-7 w-full"
        onClick={() => {
          updateParams({
            firstVerseLength: getRandomFirstVerseLength(),
          })
        }}
      >
        Nastavit náhodně
      </Button>
    </DesktopSidePanelShell>
  )
}