'use client'

import { useEffect, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Slider } from '@/components/ui/slider'
import { usePoemStore } from '@/stores/poem-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import { DesktopParamSetting } from './desktop-param-setting'

type NumericParam =
  | 'verseCount'
  | 'maxStrophes'
  | 'firstVerseLength'
  | 'temperature'

type DesktopNumberSettingProps = {
  param: NumericParam
  label: string
  placeholder: string
  min: number
  max: number
  step: number
  isValid: (value: number) => boolean
  normalize?: (value: number) => number
  decimal?: boolean
}

export function DesktopNumberSetting({
  param,
  label,
  placeholder,
  min,
  max,
  step,
  isValid,
  normalize,
  decimal = false,
}: DesktopNumberSettingProps) {
  const value = usePoemStore((state) => state.params[param])
  const updateParams = usePoemStore((state) => state.updateParams)
  const unset = useDesktopSettingsUiStore(
    (state) => state.unset[param],
  )

  function formatValue(nextValue: number | undefined) {
    if (typeof nextValue !== 'number') return ''
    return decimal ? nextValue.toFixed(1) : String(nextValue)
  }

  const [inputValue, setInputValue] = useState(() =>
    formatValue(value),
  )

  useEffect(() => {
    setInputValue(
      typeof value === 'number'
        ? decimal
          ? value.toFixed(1)
          : String(value)
        : '',
    )
  }, [value, decimal])

  function saveValue(nextValue: number | undefined) {
    updateParams({ [param]: nextValue })
  }

  function handleInputChange(nextInput: string) {
    if (decimal && !/^\d*\.?\d*$/.test(nextInput)) return

    setInputValue(nextInput)

    if (nextInput.trim() === '') {
      saveValue(undefined)
      return
    }

    const nextValue = Number(nextInput)

    if (!isValid(nextValue)) return

    saveValue(normalize ? normalize(nextValue) : nextValue)
  }

  return (
    <DesktopParamSetting param={param} label={label}>
      <div className="mt-4 flex items-center gap-5">
        <Input
          type={decimal ? 'text' : 'number'}
          inputMode={decimal ? 'decimal' : 'numeric'}
          aria-label={label}
          placeholder={placeholder}
          min={min}
          max={max}
          step={step}
          value={inputValue}
          className="min-w-0 flex-1"
          onChange={(event) =>
            handleInputChange(event.target.value)
          }
          onBlur={() => setInputValue(formatValue(value))}
        />
      </div>

      <Slider
        colorTheme="yellow"
        className="mt-6"
        min={min}
        max={max}
        step={step}
        value={[value ?? min]}
        empty={unset || typeof value !== 'number'}
        disabled={unset}
        aria-label={label}
        onPointerDownCapture={() => {
          // I první kliknutí přesně na minimum musí zapsat hodnotu.
          if (!unset && typeof value !== 'number') {
            saveValue(min)
          }
        }}
        onValueChange={(values) => {
          const nextValue = values[0]

          if (
            unset ||
            typeof nextValue !== 'number' ||
            !isValid(nextValue)
          ) {
            return
          }

          saveValue(normalize ? normalize(nextValue) : nextValue)
        }}
      />
    </DesktopParamSetting>
  )
}