'use client'

import { useEffect, useState } from 'react'
import {
  DEFAULT_MAX_STROPHES,
  MAX_STROPHES,
  MIN_STROPHES,
  STROPHE_COUNT_STEP,
  isValidMaxStrophes,
  getRandomMaxStrophes
} from '@/config/poem-param-max-strophes'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { LockedParamOverlay } from './locked-param-overlay'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'

const MIN_VERSES = 2
const MAX_VERSES = 10
const STEP = 2
const DEFAULT_VERSES = 6

function isValidVerseCount(value: number) {
  return (
    Number.isInteger(value) &&
    value >= MIN_VERSES &&
    value <= MAX_VERSES &&
    (value - MIN_VERSES) % STEP === 0
  )
}

function getRandomVerseCount() {
  const allowedValues = Array.from(
    { length: Math.floor((MAX_VERSES - MIN_VERSES) / STEP) + 1 },
    (_, index) => MIN_VERSES + index * STEP,
  )

  return allowedValues[Math.floor(Math.random() * allowedValues.length)]
}

export function SettingVerseCountOverlay({ onClose }: { onClose: () => void }) {
  const storedVerseCount = usePoemStore((state) => state.params.verseCount)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedVerseCount !== 'number') {
      updateParams({ verseCount: DEFAULT_VERSES })
    }
  }, [storedVerseCount, updateParams])

  const verseCount = storedVerseCount ?? DEFAULT_VERSES
  const [inputValue, setInputValue] = useState(String(verseCount))

  useEffect(() => {
    setInputValue(String(verseCount))
  }, [verseCount])

  const form = usePoemStore((state) => state.params.form)
  const isEditable = true //!form || form === 'free' || form === 'epigram'

  const storedMaxStrophes = usePoemStore(
    (state) => state.params.maxStrophes,
  )

  useEffect(() => {
    if (typeof storedMaxStrophes !== 'number') {
      updateParams({
        maxStrophes: DEFAULT_MAX_STROPHES,
      })
    }
  }, [storedMaxStrophes, updateParams])

  const maxStrophes =
    storedMaxStrophes ?? DEFAULT_MAX_STROPHES

  const [maxStrophesInputValue, setMaxStrophesInputValue] = useState(
    String(maxStrophes),
  )

  useEffect(() => {
    setMaxStrophesInputValue(String(maxStrophes))
  }, [maxStrophes])

  if (!isEditable) {
    return (
      <LockedParamOverlay
        iconName="verseList"
        title={poemParamInfoTexts.verseCount.title}
        infoText={poemParamInfoTexts.verseCount.text}
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
        title={poemParamInfoTexts.verseCount.title}
        onClose={onClose}
        infoText={poemParamInfoTexts.verseCount.text}
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
          type="number"
          min={MIN_VERSES}
          max={MAX_VERSES}
          step={STEP}
          value={inputValue}
          className="flex-1"
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
          colorTheme="green"
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

        <section className="mt-12 border-t border-grey-200 pt-8">
          <p className="typo-large text-grey-700">
            Nastavte maximální počet slok
          </p>

          <div className="mt-8 flex items-center gap-5">
            <label className="typo-body font-semibold text-grey-900">
              Maximální počet slok
            </label>

            <Input
              type="number"
              min={MIN_STROPHES}
              max={MAX_STROPHES}
              step={STROPHE_COUNT_STEP}
              value={maxStrophesInputValue}
              className="min-w-0 flex-1"
              onChange={(event) => {
                const nextInputValue = event.target.value
                setMaxStrophesInputValue(nextInputValue)

                const nextValue = Number(nextInputValue)

                if (!isValidMaxStrophes(nextValue)) return

                updateParams({ maxStrophes: nextValue })
              }}
              onBlur={() => {
                setMaxStrophesInputValue(String(maxStrophes))
              }}
            />
          </div>

          <Slider
            colorTheme="green"
            className="mt-7"
            min={MIN_STROPHES}
            max={MAX_STROPHES}
            step={STROPHE_COUNT_STEP}
            value={[maxStrophes]}
            onValueChange={(value) => {
              updateParams({
                maxStrophes: value[0] ?? maxStrophes,
              })
            }}
          />
        </section>

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            const maxStrophes = getRandomMaxStrophes();
            console.log('Random maxStrophes:', maxStrophes);

            updateParams({
              verseCount: getRandomVerseCount(),
              maxStrophes: maxStrophes
            })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>

    </ShellOverlay>
  )
}