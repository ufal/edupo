'use client'

import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { PoemForm } from '@/types/poem'
import { options } from '@/config/poem-param-form'
import { DesktopParamSetting } from './desktop-param-setting'

type DesktopFormPanelProps = {
  onClose: () => void
}

export function DesktopFormPanel({ onClose }: DesktopFormPanelProps) {
  const form = usePoemStore((state) => state.params.form)
  const updateParams = usePoemStore((state) => state.updateParams)

  return (
    <DesktopSidePanelShell onClose={onClose} title={poemParamInfoTexts.form.title} infoText={poemParamInfoTexts.form.text}>
      <p className="typo-body font-bold">
        Vyberte variantu
      </p>
      
      <DesktopParamSetting param="form" label="Pevná forma">
        <RadioGroup
          value={form ?? ''}
          onValueChange={(value) =>
            updateParams({ form: value as PoemForm })
          }
          className="mt-4"
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
      </DesktopParamSetting>
    </DesktopSidePanelShell>
  )
}