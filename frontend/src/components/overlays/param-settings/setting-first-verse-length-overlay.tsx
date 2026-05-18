'use client'

import { useEffect } from 'react'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Button } from '@/components/ui/button'
import { Slider } from '@/components/ui/slider'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { LockedParamOverlay } from './locked-param-overlay'

const title = 'Délka prvního verše'
const infoText = 'Kolik slabik má mít první verš?'

const MIN_LENGTH = 1
const MAX_LENGTH = 20
const STEP = 1
const DEFAULT_LENGTH = 16

export function SettingFirstVerseLengthOverlay({ onClose }: { onClose: () => void }) {
  const form = usePoemStore((state) => state.params.form)
  const storedFirstVerseLength = usePoemStore((state) => state.params.firstVerseLength)
  const updateParams = usePoemStore((state) => state.updateParams)

  useEffect(() => {
    if (typeof storedFirstVerseLength !== 'number') {
      updateParams({ firstVerseLength: DEFAULT_LENGTH })
    }
  }, [storedFirstVerseLength, updateParams])

  const firstVerseLength = storedFirstVerseLength ?? DEFAULT_LENGTH

  if (form === 'haiku') {
    return (
      <LockedParamOverlay
        iconName="ruler"
        title={title}
        infoText={infoText}
        onClose={onClose}
        messageTitle="Délka veršů je určena zvolenou formou"
        messageBody="U haiku nastavuje délku jednotlivých veršů automaticky generátor podle schématu 5–7–5 slabik."
      />
    )
  }

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="ruler"
        title={title}
        onClose={onClose}
        infoText={infoText}
      />

      <div className="px-5 pt-8">
        <p className="typo-large text-grey-700">
          Nastavte délku prvního verše
        </p>

        <div className="mt-8 flex items-center gap-5">
          <label className="typo-body font-semibold text-grey-900">
            Délka prvního verše
          </label>

          <Input
            readOnly
            value={String(firstVerseLength)}
            className="flex-1"
          />
        </div>

        <Slider
          className="mt-7"
          min={MIN_LENGTH}
          max={MAX_LENGTH}
          step={STEP}
          value={[firstVerseLength]}
          onValueChange={(value) => {
            updateParams({
              firstVerseLength: value[0] ?? firstVerseLength,
            })
          }}
        />

        <Button
          type="button"
          variant="primary"
          size="md"
          className="mt-7 px-10"
          onClick={() => {
            const random = Math.floor(Math.random() * (MAX_LENGTH - MIN_LENGTH + 1)) + MIN_LENGTH
            updateParams({ firstVerseLength: random })
          }}
        >
          Nastavit náhodně
        </Button>
      </div>
    </ShellOverlay>
  )
}