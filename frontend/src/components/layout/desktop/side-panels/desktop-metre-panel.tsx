'use client'

import { useEffect } from 'react'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { MetrumOption, options, DEFAULT_METRUM } from '@/config/poem-param-metrum'

type DesktopMetrePanelProps = {
  onClose: () => void
}

export function DesktopMetrePanel({ onClose }: DesktopMetrePanelProps) {
  const metrum = usePoemStore((state) => state.params.metrum)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (!metrum) {
      updateParams({ metrum: DEFAULT_METRUM })
    }
  }, [metrum, updateParams])

  const selected = metrum ?? DEFAULT_METRUM

  return (
    <DesktopSidePanelShell onClose={onClose} title={poemParamInfoTexts.metrum.title} infoText={poemParamInfoTexts.metrum.text}>
      <p className="typo-body font-bold">
        Zvolte rytmus básně
      </p>

      <RadioGroup
        value={selected}
        onValueChange={(value) => updateParams({ metrum: value as MetrumOption })}
        className="mt-7"
      >
        {options.map((option) => (
          <label
            key={option.value}
            className="flex cursor-pointer items-center gap-3"
          >
            <RadioGroupItem value={option.value} />

            <span className="typo-body text-primary-foreground">
              {option.label}
            </span>
          </label>
        ))}
      </RadioGroup>
    </DesktopSidePanelShell>
  )
}