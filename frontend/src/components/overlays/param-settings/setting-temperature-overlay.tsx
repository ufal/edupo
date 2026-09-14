'use client'

import { useEffect, useState } from 'react'
import { ShellOverlay } from './../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { PlainSelect } from '@/components/ui/plain-select'
import {
  DEFAULT_MODEL_SPEC,
  MODEL_OPTIONS,
  getRandomModelSpec,
} from '@/config/poem-param-model'
import type { PoemModelSpec } from '@/types/poem'

const MIN_TEMPERATURE = 0.1
const MAX_TEMPERATURE = 1
const STEP = 0.1
const DEFAULT_TEMPERATURE = 0.7

function isValidTemperature(value: number) {
  return (
    Number.isFinite(value) &&
    value >= MIN_TEMPERATURE &&
    value <= MAX_TEMPERATURE
  )
}

function normalizeTemperature(value: number) {
  return Number(value.toFixed(1))
}

export function SettingTemperatureOverlay({ onClose }: { onClose: () => void }) {
  const storedTemperature = usePoemStore((state) => state.params.temperature)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedTemperature !== 'number') {
      updateParams({ temperature: DEFAULT_TEMPERATURE })
    }
  }, [storedTemperature, updateParams])

  const temperature = storedTemperature ?? DEFAULT_TEMPERATURE
  const [inputValue, setInputValue] = useState(temperature.toFixed(1))

  useEffect(() => {
    setInputValue(temperature.toFixed(1))
  }, [temperature])

  const storedModelSpec = usePoemStore(
    (state) => state.params.modelSpec,
  )

  useEffect(() => {
    if (!storedModelSpec) {
      updateParams({
        modelSpec: DEFAULT_MODEL_SPEC,
      })
    }
  }, [storedModelSpec, updateParams])

  const modelSpec =
    storedModelSpec ?? DEFAULT_MODEL_SPEC

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="thermometer"
        title={poemParamInfoTexts.temperature.title}
        onClose={onClose}
        infoText={poemParamInfoTexts.temperature.text}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-700">
          Nastavte míru kreativity
        </p>

        <div className="mt-8 flex items-center gap-5">
          <label className="typo-body font-semibold text-grey-900">
            Temperature
          </label>

        <Input
          type="text"
          inputMode="decimal"
          value={inputValue}
          className="flex-1"
          onChange={(event) => {
            const nextInputValue = event.target.value

            // povolíme jen čísla a tečku
            if (!/^\d*\.?\d*$/.test(nextInputValue)) {
              return
            }

            setInputValue(nextInputValue)

            const nextValue = Number(nextInputValue)

            if (!isValidTemperature(nextValue)) return

            updateParams({
              temperature: normalizeTemperature(nextValue),
            })
          }}
          onBlur={() => {
            setInputValue(temperature.toFixed(1))
          }}
        />
        </div>

        <Slider
          colorTheme="green"
          className="mt-7"
          min={MIN_TEMPERATURE}
          max={MAX_TEMPERATURE}
          step={STEP}
          value={[temperature]}
          onValueChange={(value) => {
            updateParams({
              temperature: value[0] ?? temperature,
            })
          }}
        />

        <section className="mt-12 border-t border-grey-200 pt-8">
          <p className="typo-large text-grey-700">
            Vyberte model
          </p>

          <PlainSelect
            className="mt-7"
            value={modelSpec}
            options={MODEL_OPTIONS}
            onChange={(value) => {
              updateParams({ modelSpec: value as PoemModelSpec })
            }}
          />
        </section>

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            const random = Math.random() * (MAX_TEMPERATURE - MIN_TEMPERATURE) + MIN_TEMPERATURE

            updateParams({
              temperature: Number(random.toFixed(1)),
              modelSpec: getRandomModelSpec(),
            })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>

    </ShellOverlay>
  )
}