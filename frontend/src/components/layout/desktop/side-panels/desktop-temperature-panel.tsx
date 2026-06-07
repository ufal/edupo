'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Slider } from '@/components/ui/slider'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  DEFAULT_TEMPERATURE,
  MAX_TEMPERATURE,
  MIN_TEMPERATURE,
  TEMPERATURE_STEP,
  getRandomTemperature,
  isValidTemperature,
  normalizeTemperature,
} from '@/config/poem-param-temperature'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'

type DesktopTemperaturePanelProps = {
  onClose: () => void
}

export function DesktopTemperaturePanel({
  onClose,
}: DesktopTemperaturePanelProps) {
  const storedTemperature = usePoemStore((state) => state.params.temperature)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedTemperature !== 'number') {
      updateParams({ temperature: DEFAULT_TEMPERATURE })
    }
  }, [storedTemperature, updateParams])

  const temperature =
    typeof storedTemperature === 'number'
      ? storedTemperature
      : DEFAULT_TEMPERATURE

  const [inputValue, setInputValue] = useState(temperature.toFixed(1))

  useEffect(() => {
    setInputValue(temperature.toFixed(1))
  }, [temperature])

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.temperature.title}
      onClose={onClose}
      infoText={poemParamInfoTexts.temperature.text}
    >
      <p className="typo-body font-bold">
        Nastavte míru kreativity
      </p>

      <div className="mt-8 flex items-center gap-5">
        <label className="typo-body font-medium">
          Temperature
        </label>

        <Input
          type="text"
          inputMode="decimal"
          value={inputValue}
          className="min-w-0 flex-1"
          onChange={(event) => {
            const nextInputValue = event.target.value

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
        colorTheme="yellow"
        className="mt-7"
        min={MIN_TEMPERATURE}
        max={MAX_TEMPERATURE}
        step={TEMPERATURE_STEP}
        value={[temperature]}
        onValueChange={(value) => {
          updateParams({
            temperature: normalizeTemperature(value[0] ?? temperature),
          })
        }}
      />

      <Button
        type="button"
        variant="subtle"
        size="md"
        className="mt-7 w-full"
        onClick={() => {
          updateParams({ temperature: getRandomTemperature() })
        }}
      >
        Nastavit náhodně
      </Button>
    </DesktopSidePanelShell>
  )
}