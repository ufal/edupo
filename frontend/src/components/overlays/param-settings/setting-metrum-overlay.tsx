'use client'

import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { useEffect } from 'react'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { MetrumOption, options, DEFAULT_METRUM } from '@/config/poem-param-metrum'

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
        title={poemParamInfoTexts.metrum.title}
        onClose={onClose}
        infoText={poemParamInfoTexts.metrum.text}
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