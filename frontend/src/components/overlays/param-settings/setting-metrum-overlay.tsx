'use client'

import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { useEffect } from 'react'

const title = 'Metrum'
const infoText = 'Chcete, aby báseň měla nějakou pevnou formu, např. sonet?'

type MetrumOption = 'trochej' | 'jamb' | 'daktyl' | 'volný'

const DEFAULT_METRUM: MetrumOption = 'trochej'

const options: { value: MetrumOption; label: string }[] = [
  { value: 'trochej', label: 'Trochej' },
  { value: 'jamb', label: 'Jamb' },
  { value: 'daktyl', label: 'Daktyl' },
  { value: 'volný', label: 'Volný' },
]

export function SettingMetrumOverlay({ onClose }: { onClose: () => void }) {

  const storedMetrum = usePoemStore((state) => state.params.metrum)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedMetrum !== 'string') {
      updateParams({ metrum: DEFAULT_METRUM })
    }
  }, [storedMetrum, updateParams])

  const metrum = storedMetrum ?? DEFAULT_METRUM

  const selected = metrum ?? 'trochej'

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="metrum"
        title={title}
        onClose={onClose}
        infoText={infoText}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-700">Vyberte variantu</p>

        <RadioGroup
          value={selected}
          onValueChange={(value) =>
            updateParams({ metrum: value as MetrumOption })
          }
          className="mt-7"
        >
          {options.map((opt) => (
            <label
              key={opt.value}
              className="flex cursor-pointer items-center gap-3"
            >
              <RadioGroupItem value={opt.value} />

              <span className="typo-body text-grey-900">
                {opt.label}
              </span>
            </label>
          ))}
        </RadioGroup>
      </div>
    </ShellOverlay>
  )
}