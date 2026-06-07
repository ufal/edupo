'use client'

import { useEffect } from 'react'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { PoemForm } from '@/types/poem'
import { DEFAULT_FORM, options } from '@/config/poem-param-form'

type DesktopFormPanelProps = {
  onClose: () => void
}

export function DesktopFormPanel({ onClose }: DesktopFormPanelProps) {
  const form = usePoemStore((state) => state.params.form)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (!form) {
      updateParams({ form: DEFAULT_FORM })
    }
  }, [form, updateParams])

  const selected = form ?? DEFAULT_FORM

  return (
    <DesktopSidePanelShell onClose={onClose} title={poemParamInfoTexts.form.title} infoText={poemParamInfoTexts.form.text}>
      <p className="typo-body font-bold">
        Vyberte variantu
      </p>

      <RadioGroup
        value={selected}
        onValueChange={(value) => updateParams({ form: value as PoemForm })}
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