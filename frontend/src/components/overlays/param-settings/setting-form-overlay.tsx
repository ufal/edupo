'use client'

import { useEffect } from 'react'
import { ShellOverlay } from './../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { usePoemStore } from '@/stores/poem-store'
import { PoemForm } from '@/types/poem'

const title = 'Forma'
const infoText = 'Chcete, aby báseň měla nějakou pevnou formu, např. sonet?'

const DEFAULT_FORM: FormOption = 'free'

type FormOption = PoemForm

const options: { value: FormOption; label: string }[] = [
  { value: 'free', label: 'Volná forma' },
  { value: 'sonet', label: 'Sonet' },
  { value: 'limerik', label: 'Limerik' },
  { value: 'haiku', label: 'Haiku' },
  { value: 'epigram', label: 'Epigram' },
]

export function SettingFormOverlay({ onClose }: { onClose: () => void }) {

  const form = usePoemStore((state) => state.params.form)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (!form) {
      updateParams({ form: DEFAULT_FORM })
    }
  }, [form, updateParams])

  const selected = form ?? DEFAULT_FORM

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="geometry"
        title={title}
        onClose={onClose}
        infoText={infoText}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-700">Vyberte variantu</p>

        <RadioGroup
          value={selected}
          onValueChange={(value) =>
            updateParams({ form: value as FormOption })
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

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-10 px-10"
          onClick={() => {
            const random = options[Math.floor(Math.random() * options.length)]
            updateParams({ form: random.value })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}