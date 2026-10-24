'use client'

import { usePoemStore } from '@/stores/poem-store'
import { usePoemModels } from '@/hooks/use-poem-models'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopParamSetting } from './desktop-param-setting'
import { DesktopNumberSetting } from './desktop-number-setting'
import {
  RadioGroup,
  RadioGroupItem,
} from '@/components/ui/radio-group'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  MAX_TEMPERATURE,
  MIN_TEMPERATURE,
  TEMPERATURE_STEP,
  isValidTemperature,
  normalizeTemperature,
} from '@/config/poem-param-temperature'

type DesktopTemperaturePanelProps = {
  onClose: () => void
}

export function DesktopTemperaturePanel({
  onClose,
}: DesktopTemperaturePanelProps) {
  const updateParams = usePoemStore((state) => state.updateParams)

  const {
    models,
    status,
    error,
    modelSpec,
    retryModels,
  } = usePoemModels()

  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.temperature.title}
      infoText={poemParamInfoTexts.temperature.text}
      onClose={onClose}
    >
      <p className="typo-body font-bold">
        AI model
      </p>

      {(status === 'idle' || status === 'loading') && (
        <p className="mt-4 typo-small" role="status">
          Načítání modelů…
        </p>
      )}

      {status === 'error' && (
        <div className="mt-4" role="alert">
          <p className="typo-small">
            {error}
          </p>

          <button
            type="button"
            onClick={retryModels}
            className="mt-3 cursor-pointer typo-small underline"
          >
            Zkusit znovu
          </button>
        </div>
      )}

      <DesktopParamSetting param="modelSpec" label="AI model">
        <RadioGroup
          className="mt-4"
          value={modelSpec}
          disabled={status !== 'success'}
          onValueChange={(value) =>
            updateParams({ modelSpec: value })
          }
        >
          {models.map((model) => (
            <label
              key={model.generic_identifier}
              className="flex cursor-pointer items-start gap-3"
            >
              <RadioGroupItem
                value={model.generic_identifier}
                className="mt-[2px]"
              />

              <span className="min-w-0">
                <span className="block break-words typo-body text-white">
                  {model.human_readable_identifier}
                </span>

                <span className="mt-1 block break-all typo-small text-white/70">
                  {model.precise_identifier}
                </span>
              </span>
            </label>
          ))}
        </RadioGroup>
      </DesktopParamSetting>

      <section className="mt-12 pt-8">
        <p className="typo-body font-bold">
          Temperature
        </p>

        <DesktopNumberSetting
          param="temperature"
          label="Temperature"
          placeholder="Temperature"
          min={MIN_TEMPERATURE}
          max={MAX_TEMPERATURE}
          step={TEMPERATURE_STEP}
          isValid={isValidTemperature}
          normalize={normalizeTemperature}
          decimal
        />
      </section>
    </DesktopSidePanelShell>
  )
}