'use client'

import { ShellOverlay } from './../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { useEffect } from 'react'

const title = 'Temperature'
const infoText = 'Teplota - říká AI, jak moc má být kreativní: nízká teplota sází na jistotu, vysoká zkouší divoké nápady.'

const MIN_TEMPERATURE = 0
const MAX_TEMPERATURE = 1
const STEP = 0.1
const DEFAULT_TEMPERATURE = 0.7

export function SettingTemperatureOverlay({ onClose }: { onClose: () => void }) {
  const storedTemperature = usePoemStore((state) => state.params.temperature)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedTemperature !== 'number') {
      updateParams({ temperature: DEFAULT_TEMPERATURE })
    }
  }, [storedTemperature, updateParams])

  const temperature = storedTemperature ?? DEFAULT_TEMPERATURE

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="thermometer"
        title={title}
        onClose={onClose}
        infoText={infoText}
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
            readOnly
            value={temperature.toFixed(1)}
            className="flex-1"
          />
        </div>

        <Slider
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

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            const random = Number((Math.random() * (MAX_TEMPERATURE - MIN_TEMPERATURE) + MIN_TEMPERATURE).toFixed(1))
            updateParams({ temperature: random })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}